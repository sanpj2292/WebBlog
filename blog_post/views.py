from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Post as PostModel, PUBLISH_CHOICES
from .forms import PostModelForm

UserModel = get_user_model()


@login_required(login_url='/login/')
def blog_home(request, *args, **kwargs):
    context = {}
    posts_qs = PostModel.objects.all()
    if posts_qs.count() > 0:
        posts = []
        for post_obj in posts_qs.order_by('-publish_date', '-created_at'):
            posts.append(post_obj)
        context['posts'] = posts
        context['request_user'] = request.user
    return render(request, 'blog_post/home.html', context)


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        post_model_form = PostModelForm(request.POST)
        if post_model_form.is_valid():
            post_obj = post_model_form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            return redirect('posts/')
        else:
            messages.error(request, 'Something went wrong, kindly please try again!')
    context = {'options': dict(PUBLISH_CHOICES), }
    return render(request, 'blog_post/create_post.html', context=context)


@csrf_exempt
def update_post(request, post_id=None):
    post_obj = PostModel.objects.filter(id=post_id).first()
    if request.method == 'POST':
        post_model_form = PostModelForm(request.POST, instance=post_obj)
        if post_model_form.has_changed() and post_model_form.is_valid():
            upd_post_obj = post_model_form.save(commit=False)
            upd_post_obj.author = request.user
            upd_post_obj.save()
            return redirect('blog_home')
    context = {'post': post_obj, 'options': dict(PUBLISH_CHOICES), }
    return render(request, 'blog_post/create_post.html', context=context)
