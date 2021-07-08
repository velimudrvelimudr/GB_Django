from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.

class BookUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', verbose_name='Аватар', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))


    def is_key_expired(self):
        return True if now() <= self.activation_key_expires else False


    def __str__(self):
        return super().__str__()


    def user_count(self):
        """ Возвращает количество книг в библиотеке пользователя.  """

        return len(self.perslib.all())


class BookUserProfile(models.Model):
    MALE = 'm'
    FEMALE = 'w'

    gender_shoices = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(
        BookUser, 
        on_delete=CASCADE,
        null=False, 
        unique=True, 
        db_index=True
    )
    
    tagline = models.CharField(
        verbose_name='Теги',
        max_length=128,
        blank=True
    )

    about_me = models.TextField(verbose_name='О себе', max_length=32767, blank=True)
    gender = models.CharField(
        verbose_name='пол',
        max_length=1,
        choices=gender_shoices,
        blank=True
    )

    @receiver(post_save, sender=BookUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            BookUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=BookUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.bookuserprofile.save()