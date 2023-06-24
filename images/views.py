# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Image

# Create your views here.
def images(request):
    images = Image.objects.all().values()
    template = loader.get_template('images_list.html')
    context = {
        'images': images,
    }
    return HttpResponse(template.render(context, request))

def image(request, id):
    image = Image.objects.get(id=id)
    template = loader.get_template('image.html')
    context = {
        'image': image,
    }
    return HttpResponse(template.render(context, request))
