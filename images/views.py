from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Image
from ast import literal_eval
from random import shuffle

# Create your views here.
def images(request):
    tag = request.GET.get('q')
    is_random = False # randomize results, should be actionable in UI
    if tag:
        images = Image.objects.filter(tags__contains=tag).values()
        is_search = True
    else:
        images = list(Image.objects.all().values())
        if is_random:
            shuffle(images)
        is_search = False
    # print(q)
    template = loader.get_template('images_list.html')
    context = {
        'images': images,
        'is_search': is_search

    }
    return HttpResponse(template.render(context, request))

def image(request, id):
    image = Image.objects.get(id=id)
    tags = Image.objects.filter(id=id).values('tags')
    template = loader.get_template('image.html')
    get_tags = format_tags(tags)
    context = {
        'image': image,
        'tags' : get_tags
    }
    return HttpResponse(template.render(context, request))

def format_tags(tags):
    tags_list = tags
    for i in tags_list:
        list = literal_eval(i['tags'])
        return list
