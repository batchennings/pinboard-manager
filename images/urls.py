from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.images, name='images'),
    path('images/image/<int:id>', views.image, name='image'),
]
