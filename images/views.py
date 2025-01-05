from django.shortcuts import render
from os import listdir, remove
from os.path import isfile, join, getctime, getmtime, splitext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.template import loader
from .models import Image
from ast import literal_eval
from random import shuffle
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.db.models import Q
import collections
import operator
import re
from functools import reduce
from .forms import TagsForm, NameForm

from var_dump import var_dump


data_folder='/Users/patjennings/Documents/pinboard_manager/data'
data_thumbnails_folder='/Users/patjennings/Documents/pinboard_manager/data/thumbnails'

# Create your views here.
def images(request):
    search = request.GET.get('q')
    sort_by_creation = request.GET.get('sort_by_creation')
    random = request.GET.get('random')
    action = request.GET.get('action')
    items = []

    is_random = False
    is_sorted_by_creation = False
    is_search = False

    if random == '1':
        is_random = True
    if sort_by_creation == '1':
        is_sorted_by_creation = True
    if search:
        spl_search = search.split(" ")

        tags_terms = []
        str_terms = []

        # find tags, and fill the t_tags list
        str_spl = re.findall(':[a-zA-Z0-9éàèùûôî\ \-_]+:', search)
        for t in str_spl:
            tags_terms.append(t.strip(':'))

        # remove tags from original string
        clean_str = search
        for u in str_spl:
            clean_str = clean_str.replace(u, '')
            print(clean_str)

        # now, with the new string, get terms
        spl_str = clean_str.split(' ')
        for s in spl_str:
            if s != '':
                str_terms.append(s.strip())

        q_list = []
        for qt in tags_terms:
            q_list.append(Q(tags__contains=qt))
        for qs in str_terms:
            q_list.append(Q(name__contains=qs))
        images = list(Image.objects.filter(reduce(operator.and_, q_list)))

        images_qty = len(images)
        is_search = True
    else:
        images = list(Image.objects.all())
        images_qty = len(images)
        is_search = False

    if is_sorted_by_creation:
        def img_date(elem):
            return elem.date_created
        images.sort(reverse=True, key=img_date)
        
    if is_random:
        shuffle(images)
        
    if request.method == "POST":
        items = request.POST.getlist('image-item')
        print(items)

    template = loader.get_template('images_list.html')
    context = {
        'images': images,
        'images_qty': images_qty,
        'is_search': is_search,
        'search' : search,
        'sort_by_creation': sort_by_creation,
        'random': random,
        'action' : action,
        'items' : items
    }
    return HttpResponse(template.render(context, request))

def bulk_tags_update(request):
    search = request.GET.get('q')
    print(request)
    
    template = loader.get_template('images_list.html')
    context = {
        'search' : search,
    }
    return HttpResponse(template.render(context, request))
    # prendre les éléments issus de la modale de /images, et les écrire dans les entrées indiquées 

def bulk_names_update(request):
    search = request.GET.get('q')
    print(request)
    template = loader.get_template('images_list.html')
    context = {
        'search' : search,
    }
    return HttpResponseRedirect("/?q="+search)
    # prendre les éléments issus de la modale de /images, et les écrire dans les entrées indiquées 

def tags_update(request, id):
    search = request.GET.get('q')
    sort_by_creation = request.GET.get('sort_by_creation')
    random = request.GET.get('random')
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TagsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_record = Image.objects.get(id=id)
            tags_record = format_tags_update(form.cleaned_data['tags'])

            new_record.tags  = tags_record
            print('----------------')
            print(new_record)
            print(new_record.tags)
            print(tags_record)
            print('----------------')
            new_record.save()

            # redirect to a new URL:
            return HttpResponseRedirect("/image/"+str(id)+"?q="+search+"&sort_by_creation="+sort_by_creation+"&random="+random)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TagsForm()

    return render(request, "image.html", {
        "form": form,
        'search' : search,
        'sort_by_creation': sort_by_creation,
        'random': random
    })

def tags(request):
    sort = request.GET.get('sort') # name or value
    all_tags = Image.objects.values().values('tags')
    tags = {}
    for t in all_tags:
        list = literal_eval(t['tags'])
        for i in list:
            if i in tags:
                # find and increment
                tags[i] = tags.get(i)+1
            else :
                # add it and set to zero
                tags[i] = 1

    if sort == 'name':
        # tags = collections.OrderedDict(sorted(tags.items()))
        tags = dict(sorted(tags.items()))
    elif sort == 'value':
        tags = dict(sorted(tags.items(), key=lambda item: item[1], reverse=True))
    template = loader.get_template('tags_list.html')
    context = {
        'tags': tags
    }
    return HttpResponse(template.render(context, request))

def image(request, id):
    search = request.GET.get('q')
    sort_by_creation = request.GET.get('sort_by_creation')
    random = request.GET.get('random')
    tag_edit = request.GET.get('tag_edit') # name or value
    action = request.GET.get('action')
    is_tag_edit = False
    if tag_edit == '1':
        is_tag_edit = True

    image = Image.objects.get(id=id)
    tags = Image.objects.filter(id=id).values('tags')
    get_tags = format_tags(tags)
    tags_list_for_edit = get_tags_for_input(get_tags)

    template = loader.get_template('image.html')
    context = {
        'image': image,
        'tags' : get_tags,
        'tags_list_for_edit': tags_list_for_edit,
        'tag_edit' : is_tag_edit,
        'action' : action,
        'search' : search,
        'sort_by_creation': sort_by_creation,
        'random': random
    }
    return HttpResponse(template.render(context, request))

def image_delete(request,id):
    print(str(id)+' will be deleted')
    image = Image.objects.get(id=id)
    # delete image
    remove(join(data_folder, image.file))
    # delete thumbnail
    remove(join(data_thumbnails_folder, image.thumb))
    # remove from base with id
    image.delete()
    print(str(id)+' deleted')
    return HttpResponseRedirect("/images?")

def format_tags_update(tags_in):
    f_tags = tags_in.split(",")
    result = '['
    t=0
    while t < len(f_tags):
        u = f_tags[t]
        u_nospace = u.strip()
        result+='\''+u_nospace+'\''
        if t != len(f_tags)-1:
            result+=','
        t+=1
    result+= ']'
    return result

def get_tags_for_input(tags_list):
    result = ''
    x=0
    for t in tags_list:
        if x<len(tags_list)-1:
            result+=t+','
        else:
            result+=t
        x+=1
    return result

def format_tags(tags):
    tags_list = tags
    for i in tags_list:
        list = literal_eval(i['tags'])
        return list
