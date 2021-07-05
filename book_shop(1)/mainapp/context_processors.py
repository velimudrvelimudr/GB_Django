from auth_app.models import BookUser


def  user_count(request):
    """ Передаёт в контекст размер библиотеки авторизованного пользователя. """

    if request.user.is_authenticated:
        uc = request.user.user_count()
    else:
        uc = None

    return {
        'user_count': uc,
    }
