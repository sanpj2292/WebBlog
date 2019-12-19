from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

UserModel = get_user_model()


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('/login')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pwd = request.POST.get('password')
        if (not un or un == '') or (not pwd or pwd == ''):
            messages.error(request, message='Empty Username/Password Not Allowed')
            return render(request, 'user_login/login.html', {})
        user_qs = UserModel.objects.filter(username__iexact=un)
        if not user_qs and user_qs.count() != 1:
            messages.error(request, message='Invalid Credentials')
            return render(request, 'user_login/login.html', {})
        user_obj = user_qs.first()
        if not user_obj.check_password(pwd):
            messages.error(request, message='Invalid Credentials')
            return render(request, 'user_login/login.html', {})
        login(request, user=user_obj)
        return redirect('blog_home')
    return render(request, 'user_login/login.html', {})
