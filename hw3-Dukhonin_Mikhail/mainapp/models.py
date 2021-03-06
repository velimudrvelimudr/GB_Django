from django.db import models

# Create your models here.


class BookCategory(models.Model):
    name = models.CharField(verbose_name='Название', max_length=32, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=512, blank=True)

    def __str__(self):
        return f'{self.name}, {self.description}'


class Books(models.Model):
    cat_fk = models.ForeignKey(BookCategory, on_delete=models.    CASCADE)
    name = models.CharField(verbose_name='Заголовок', max_length=256)
    author = models.CharField(verbose_name='Автор(ы)', max_length=255, blank=True)
    annotation = models.TextField(verbose_name='Аннотация', blank=True)
    cover = models.ImageField(upload_to='covers', verbose_name='Обложка', blank=True)
    created_at = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлён', auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.author}\n{self.annotation}\n{self.cat_fk.name}'
