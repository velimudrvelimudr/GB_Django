from django.shortcuts import render
from csv import DictReader

# Create your views here.

def main(request):
    return render(request, 'mainapp/index.html')

def load_books():
    fields = ['topic','tags','number','author','title','comment','serial','number_serial','folder','file']
    with open('books.csv', 'r', encoding='ansi') as book_file:
        dw = DictReader(book_file, fields, dialect='excel-tab')
        return list(dw)

book_list = {'book_list':load_books()}

def catalog(request):
    return render(request, 'mainapp/catalog.html', book_list)

def contacts(request):
    return render(request, 'mainapp/contacts.html')

def test(request):
    return render(request, 'mainapp/test.html', {'title':'Тестовая страница'})
