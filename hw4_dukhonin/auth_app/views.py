from django import http
from django.http import request
from django.shortcuts import render, HttpResponseRedirect
from auth_app.forms import BookLoginUserForm, BookUserEditForm
from django.contrib import auth
from django.urls import reverse

# Create your views here.

def login(request):
    title = 'Вход'
    login_form = BookLoginUserForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))
    content = {'title': title, 'login_form':login_form}
    return render(request, 'auth_app/login.html', context=content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def profile(request, action='view'):
    title = 'Профиль'

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('main'))

    if action == 'edit':
        title = 'редактирование профиля пользователя'
        if request.method == 'POST':
            edit_form = BookUserEditForm(request.POST, request.FILES, instance=request.user)
            if edit_form.is_valid():
                edit_form.save()
                return render(request, 'auth_app/profile_view.html', {'title':'профиль пользователя'})
        else:
            edit_form = BookUserEditForm(instance=request.user)
        return render(request, 'auth_app/profile_editor.html', context={'title':title, 'edit_form':edit_form})
    return render(request, 'auth_app/profile_view.html', {'title':title})
