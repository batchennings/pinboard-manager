from django.urls import path
from . import views

urlpatterns = [
    path('', views.images, name='images'),
    path('tags', views.tags, name='tags'),
    path('image/<int:id>', views.image, name='image'),
    path('image/<int:id>/tags_update', views.tags_update, name='tags_update'),
    path('image/<int:id>/delete', views.image_delete, name='image_delete'),
]
