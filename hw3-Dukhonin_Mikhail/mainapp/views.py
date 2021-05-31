from django.shortcuts import render
from csv import DictReader
from .models import BookCategory, Books

# Create your views here.

def main(request):
    content = {
        'bc':BookCategory.objects.order_by('name')
    }
    return render(request, 'mainapp/index.html', context=content)


def catalog(request, pk=None):
    if pk:
        book_list = Books.objects.all().filter(cat_fk=pk)
        topic = BookCategory.objects.filter(id=pk)
    else:
        book_list = Books.objects.all()
        topic = None

    cat_menu = [(c.id, c.name) for c in BookCategory.objects.order_by('name')]
    """ Срачала хотел: {c.id: c.name for c in BookCategory.objects.order_by('name')}, Но почему-то не заработало в шаблоне. {{ cat_menu.m }} где m - ключ словаря cat_menu, возвратило ничего. """
    
    content = {
        'books':book_list,
        'topic_name': topic[0].name if topic else None,
        'cat_menu':cat_menu
        }
    return render(request, 'mainapp/catalog.html', context=content)


def show_book_info(request, book_id):
    
    book_info = Books.objects.get(id=book_id)
    context = {
        'bookinfo':book_info
    }
    
    return render(request, 'mainapp/book.html', context=context)


def contacts(request):
    return render(request, 'mainapp/contacts.html')

def test(request):
    return render(request, 'mainapp/test.html', {'title':'Тестовая страница'})
