from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post as PostModel

UserModel = get_user_model()


@login_required(login_url='/login/')
def blog_home(request, *args, **kwargs):
    context = {}
    if PostModel.objects.all().count() > 0:
        posts = []
        for post in PostModel.objects.all():
            posts.append(post)
        context['posts'] = posts
    return render(request, 'blog_post/home.html', context)


def create_post(request):
    context = {}
    if request.method == 'POST':
        return redirect('/')
    return render(request, '', context=context)
