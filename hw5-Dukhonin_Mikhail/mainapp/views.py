from django.shortcuts import render
from csv import DictReader
from mainapp.models import BookCategory, Books
from userlibrapp.models import PersonLib

# Create your views here.

def main(request):
    """ Отображает главную страницу. 
    На странице выводится меню категорий.  """

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
    else:
        user_books = None

    content = {
        'cat_menu':BookCategory.objects.order_by('name'),
        'user_books':user_books,
    }
    return render(request, 'mainapp/index.html', context=content)


def catalog(request, pk=None):
    """ Отображение каталога. Если указан ID категории, то только книг из этой категории. """

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
    else:
        user_books = None

    if pk:
        book_list = Books.objects.all().filter(cat_fk=pk)
        topic = BookCategory.objects.get(pk=pk).name
    else:
        book_list = Books.objects.all()
        topic = None

    cat_menu = BookCategory.objects.all().order_by('name')
    
    content = {
        'books':book_list,
        'topic_name': topic,
        'cat_menu':cat_menu,
        'user_books':user_books,
    }

    return render(request, 'mainapp/catalog.html', context=content)


def show_book_info(request, book_id):
    """ Вывод информации о книге. """

    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
        user_book = PersonLib.objects.filter(book__id=book_id, user=request.user)
        if len(user_book) == 1:
            url_view = 'libr:rm_book'
            url_id = user_book.first().id
            url_text = 'Удалить из библиотеки'
        else:
            url_view = 'libr:add_book'
            url_id = book_id
            url_text = 'Добавить в библиотеку'
    else:
        user_books = None
        url_text = None
        url_id = None
        url_view = None

    book_info = Books.objects.get(id=book_id)
    book_count = len(PersonLib.objects.filter(book__id=book_id) ) # В подробных данных о книге покажем, сколько читателей её себе добавили.

    context = {
        'bookinfo':book_info,
        'user_books':user_books,
        'book_count':book_count,
        'url_data':(url_view, url_id, url_text),
    }
    print(context['url_data'])
    return render(request, 'mainapp/book.html', context=context)


def contacts(request):
    """ Страница контактов.  """
    if request.user.is_authenticated:
        user_books = PersonLib.objects.filter(user=request.user)
    else:
        user_books = None
    
    context = {
        'user_books':user_books
    }

    return render(request, 'mainapp/contacts.html', context=context)

def test(request):
    return render(request, 'mainapp/test.html', {'title':'Тестовая страница'})
