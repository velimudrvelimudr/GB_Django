from django import forms
from django.forms import fields
from auth_app import models
from auth_app.models import BookUser
from auth_app.forms import BookUserEditForm
from mainapp.models import BookCategory


class BookUserAdminEditForm(BookUserEditForm):
    class Meta:
        model = BookUser
        fields = '__all__'


class CatEditForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = '__all__'

