from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BookUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', verbose_name='Аватар', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст')