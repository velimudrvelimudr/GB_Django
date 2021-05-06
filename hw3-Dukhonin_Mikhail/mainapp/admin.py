from django.contrib import admin
from .models import books, book_category

# Register your models here.

admin.site.register(book_category)
admin.site.register(books)
