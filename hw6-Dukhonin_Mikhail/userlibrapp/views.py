from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from mainapp.models import Books
from userlibrapp.models import PersonLib

# Create your views here.

def perslib(request):
    """ Просмотр библиотеки пользователя. """

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('main')) # У анонима библиотеки не бывает.

    user_books = PersonLib.objects.filter(user=request.user)
    title = 'Библиотека пользователя'
    lib_data = PersonLib.objects.filter(user=request.user)

    context = {
        'title':title,
        'user_books':user_books,
        'lib_data':lib_data,
    }

    return render(request, 'userlibrapp/userlibr.html', context=context)


def add_book(request, pk):
    """ Добавление книги в библиотеку. """

    book = get_object_or_404(Books, pk=pk)

    user_book = PersonLib.objects.filter(user=request.user, book=book).first()

    if not user_book:
        user_book = PersonLib(user=request.user, book=book)
        user_book.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def rm_book(request, pk):
    """ Удаление книги из библиотеки.  """

    user_book = get_object_or_404(PersonLib, pk=pk, user=request.user)

    if user_book:
        user_book.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

