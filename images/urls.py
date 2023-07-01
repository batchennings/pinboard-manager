from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.images, name='images'),
    path('images/tags', views.tags, name='tags'),
    path('images/image/<int:id>', views.image, name='image'),
    path('images/image/<int:id>/tags_update', views.tags_update, name='tags_update'),
    path('images/image/<int:id>/delete', views.image_delete, name='image_delete'),
]
