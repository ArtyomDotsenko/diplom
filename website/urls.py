from django.urls import path
from .views import *

urlpatterns = [
    path('', AdressList.as_view(), name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
