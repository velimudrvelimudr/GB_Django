from django.shortcuts import render, HttpResponseRedirect
from auth_app.forms import BookLoginUserForm, BookUserEditForm, BookUserRegisterForm
from django.contrib import auth
from django.urls import reverse
from userlibrapp.models import PersonLib

# Create your views here.

def login(request):
    """ Страница авторизации.  """

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
    else:
        user_books = None

    title = 'Вход'
    login_form = BookLoginUserForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form':login_form,
        'user_books':user_books
    }

    return render(request, 'auth_app/login.html', context=content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def profile(request):
    """ Просмотр профиля аутентифицированного пользователя. """

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
    
    title = 'Профиль пользователя'

    context = {
        'title':title,
        'user_books':user_books,
    }

    if request.user.is_authenticated:
        return render(request, 'auth_app/profile_view.html', context=context)
    else:
        return HttpResponseRedirect(reverse('auth:login')) # Нечего анониму делать на странице профиля.

def edit(request):
    """ Редактирование профиля пользователя.  """

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('auth:login')) # Анонимного пользователя попросим залогиниться.

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)

    title = 'Изменить профиль пользователя'

    if request.method == 'POST':
        edit_form = BookUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        edit_form = BookUserEditForm(instance=request.user)

    context = {
        'title':title,
        'form': edit_form,
        'id_view':'edit',
        'user_books':user_books,
    }

    return render(request, 'auth_app/profile_editor.html', context=context)


def register(request):
    """ Регистрация нового пользователя """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth:profile')) # Аутентифицированным пользователям здесь делать нечего.

    title = 'Регистрация нового пользователя'
    
    if request.method == 'POST':
        reg_form = BookUserRegisterForm(request.POST, request.FILES)
        if reg_form.is_valid():
            reg_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        reg_form = BookUserRegisterForm

    context = {
        'title':title,
        'form':reg_form,
        'id_view':'registr',
    }

    return render(request, 'auth_app/profile_editor.html', context)


