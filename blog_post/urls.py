from django.urls import path
from .views import create_post, blog_home, update_post, delete_post, detail_post

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('create/', create_post, name='create_post'),
    path('<int:post_id>/update/', update_post, name='update_post'),
    path('<int:post_id>/', detail_post, name='detail_post'),
    path('delete/', delete_post, name='delete_post'),
]
