from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from auth_app.models import BookUser, BookUserProfile
from auth_app.forms import BookLoginUserForm, BookUserEditForm, BookUserRegisterForm, EditProfileForm
from userlibrapp.models import PersonLib
from django.db import transaction


# Create your views here.


def login(request):
    """ Страница авторизации.  """

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
    }

    return render(request, 'auth_app/login.html', context=content)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def profile(request):
    """ Просмотр профиля аутентифицированного пользователя. """

    title = 'Профиль пользователя'

    context = {
        'title':title,
    }

    return render(request, 'auth_app/profile_view.html', context=context)


@login_required
@transaction.atomic
def edit(request):
    """ Редактирование профиля пользователя.  """

    title = 'Изменить профиль пользователя'

    if request.method == 'POST':
        edit_form = BookUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.bookuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        edit_form = BookUserEditForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.bookuserprofile)

    context = {
        'title':title,
        'form': edit_form,
        'id_view':'edit',
        'pform': profile_form,
    }

    return render(request, 'auth_app/profile_editor.html', context=context)


def send_verify_mail(user):
    """ Отправляет регистрирующемуся  пользователю E-Mail с кодом подтверждения регистрации.  """

    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учётной записи пользователя {user.username}.'
    message = f'Для подтверждения учётной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def register(request):
    """ Регистрация нового пользователя """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth:profile')) # Аутентифицированным пользователям здесь делать нечего.

    title = 'Регистрация нового пользователя'
    
    if request.method == 'POST':
        reg_form = BookUserRegisterForm(request.POST, request.FILES)
        if reg_form.is_valid():
            new_user = reg_form.save()
            if send_verify_mail(new_user):
                auth.login(request, new_user)
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Ошибка отправки сообщения!')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        reg_form = BookUserRegisterForm

    context = {
        'title':title,
        'form':reg_form,
        'id_view':'registr', # Чтобы отличить форму для регистрации от формы для редактирования пользователя.
        'user_count': None,
    }

    return render(request, 'auth_app/profile_editor.html', context)


def verify(request, email, activation_key):
    """ Верификация пользователя. """

    try:
        user = get_object_or_404(BookUser, email=email)

        if user.activation_key == activation_key and user.is_key_expired():
            user.is_active = True
            user.activation_key = ''
            user.save()
            auth.login(request, user)
            return render(request, 'auth_app/verification.html')
        else:
            print(f'Ошибка верификации пользователя {user}')
            return render(request, 'auth_app/verification.html')
    except Exception as e:
        print(f'Ошибка активации пользователя {user.username}: {e.args}')
        return HttpResponseRedirect(reverse('main'))


