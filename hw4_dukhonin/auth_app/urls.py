import auth_app
from django.urls import path
from django.urls.resolvers import URLPattern
import auth_app.views as     authapp

app_name = 'auth_app'


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('profile/<str:action>/', authapp.profile, name='profile'),
]

