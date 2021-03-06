from mainapp.models import BookCategory, Books
from csv import DictReader


def load_books():
    """ Загрузка CSV-файла с данными для базы. """
    
    fields = ['topic','tags','number','author','title','comment','serial','number_serial','folder','file']
    with open('books.csv', 'r', encoding='utf-8') as book_file:
        dw = DictReader(book_file, fields, dialect='excel-tab')
        return list(dw)

def populate_db():
    """Заполнение БД. """

    data = load_books()

    for d in data:
        new_book = Books()
        new_book.name=d['title']
        new_book.author = d['author']
        new_book.annotation = d['comment']
        if not len(BookCategory.objects.filter(name=d['topic'])):
            new_cat = BookCategory()
            new_cat.name=d['topic']
            new_cat.save()

        new_book.cat_fk = BookCategory.objects.filter(name=d['topic']).first()
        new_book.save()
        