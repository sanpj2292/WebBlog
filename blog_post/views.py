from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest, JsonResponse
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


@login_required(login_url='/login/')
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        post_model_form = PostModelForm(request.POST)
        if post_model_form.is_valid():
            post_obj = post_model_form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            return redirect('blog_home')
        else:
            messages.error(request, 'Something went wrong, kindly please try again!')
    context = {'options': dict(PUBLISH_CHOICES), }
    return render(request, 'blog_post/create_post.html', context=context)


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post_obj = PostModel.objects.get(pk=post_id)
            post_obj.delete()
            return JsonResponse({'success': 'Blog Post Deleted Successfully'})
        except:
            return JsonResponse({'error': 'Error Occurred in Deletion'}, status_code=500)
    else:
        return HttpResponseBadRequest(content='GET Request not allowed', content_type="application/json")


@login_required(login_url='user_login')
def detail_post(request, *args, **kwargs):
    if kwargs.get('post_id'):
        post_id = kwargs.get('post_id')
        post_obj = PostModel.objects.get(id=post_id)
        return render(request, 'blog_post/detail_post.html', context={'post': post_obj})
    else:
        raise HttpResponseBadRequest('Bad Request, please try requesting in a valid manner')
