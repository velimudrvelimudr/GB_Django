from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from auth_app.models import BookUser
from mainapp.models import BookCategory, Books


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    """ Список пользователей. """

    users = BookUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    title = 'Список пользователей'

    context ={
        'users': users,
        'title': title,
    }

    return render(request, 'admin_app/users.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_info(request, pk):
    """ Информация о пользователе. """

    user = get_object_or_404(BookUser, pk=pk)
    title = 'Данные пользователя.'

    context = {
        'user': user,
        'title': title,
    }

    return render(request, 'admin_app/user_info.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def cats(request):
    """ Список категорий.  """

    cats = BookCategory.objects.all().order_by('name')
    title = 'Список категорий'

    context = {
        'cats': cats,
        'title': title,
    }

    return render(request, 'admin_app/cats.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def cat_info(request, pk):
    """ Информация о категории. """

    cat = get_object_or_404(BookCategory, pk=pk)
    title = 'Информация о категории'

    context = {
        'cat': cat,
        'title': title
    }

    return render(request, 'admin_app/cat_info.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def books(request, cat=None):
    """ Список книг. """

    title = 'Список книг'
    cat_menu = BookCategory.objects.all().order_by('name')

    if cat:
        books = Books.objects.filter(cat_fk=cat).order_by('author', 'name')
        cat_name = get_object_or_404(BookCategory, pk=cat).name
    else:
        books = Books.objects.all().order_by('author', 'name')
        cat_name = None

    context = {
        'books': books,
        'title': title,
        'cat_name': cat_name,
        'cat_menu': cat_menu,
    }

    return render(request, 'admin_app/books.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def book_info(request, pk):
    """ Информация о книге. """

    title = 'Информация о книге'
    book = get_object_or_404(Books, pk=pk)

    context = {
        'title': title,
        'book': book,
    }

    return render(request, 'admin_app/book_info.html', context=context)

