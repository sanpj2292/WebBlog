from django.urls import path, include
from .views import create_post, blog_home

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('create/', create_post, name='create_post'),
]
