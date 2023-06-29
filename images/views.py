from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.template import loader
from .models import Image
from ast import literal_eval
from random import shuffle
from urllib.parse import urlparse
from urllib.parse import parse_qs
import collections
from .forms import TagsForm

# Create your views here.
def images(request):
    tag = request.GET.get('q')
    sort_by_creation = request.GET.get('sort_by_creation')
    random = request.GET.get('random')

    is_random = False
    is_sorted_by_creation = False

    if random == '1':
        is_random = True
    if sort_by_creation == '1':
        is_sorted_by_creation = True
    if tag:
        print('hasTag')
        images = list(Image.objects.filter(tags__contains=tag).values())
        images_qty = len(images)
        is_search = True
    else:
        images = list(Image.objects.all().values())
        images_qty = len(images)
        is_search = False

    if is_sorted_by_creation:
        images = list(Image.objects.order_by('-date_created'))
    if is_random:
        shuffle(images)

    template = loader.get_template('images_list.html')
    context = {
        'images': images,
        'images_qty': images_qty,
        'is_search': is_search
    }
    # tags_list()
    return HttpResponse(template.render(context, request))

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

def tags_update(request, id):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TagsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # print(form.cleaned_data['tags'])
            new_record = Image.objects.get(id=id)
            tags_record = format_tags_update(form.cleaned_data['tags'])

            new_record.tags  = tags_record
            print('----------------')
            # print(Image.objects.all().values())
            print(new_record)
            print(new_record.tags)
            print(tags_record)
            print('----------------')
            new_record.save()

            # print(new_record)
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/images/image/"+str(id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TagsForm()

    return render(request, "image.html", {"form": form})

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
    tag_edit = request.GET.get('tag_edit') # name or value
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
        'tag_edit' : is_tag_edit
    }
    return HttpResponse(template.render(context, request))

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
