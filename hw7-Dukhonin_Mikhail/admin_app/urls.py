from django.urls.conf import path
import admin_app.views as my_admin

app_name = 'admin_app'

urlpatterns = [
    path('', my_admin.users),
    path('users/', my_admin.users, name='users'),
    path('user_info/<int:pk>/', my_admin.user_info, name='user_info'),
    path('cats/', my_admin.cats, name='cats'),
    path('cat_info/<int:pk>/', my_admin.cat_info, name='cat_info'),
    path('books/', my_admin.books, name='books'),
    path('books/<int:cat>/', my_admin.books, name='books'),
    path('book_info/<int:pk>/', my_admin.book_info, name='book_info')
]
