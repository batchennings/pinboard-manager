from django.urls import path
from . import views

urlpatterns = [
    path('', views.images, name='images'),
    path('tags', views.tags, name='tags'),
    path('image/<int:id>', views.image, name='image'),
    path('image/<int:id>/tags_update', views.tags_update, name='tags_update'),
    path('bulk_tags_update', views.bulk_tags_update, name='bulk_tags_update'),
    path('bulk_names_update', views.bulk_names_update, name='bulk_names_update'),
    path('image/<int:id>/delete', views.image_delete, name='image_delete'),
]
