from django.urls import path
from .views import *

urlpatterns = [
    path('', AdressList.as_view(), name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category_add/<int:category_id>/', add_data_adress, name="category_add"),
    path('category_view/<int:category_id>/<int:year_id>/<int:month_id>', view_data_adress, name="category_view"),
    path('category_view_admin/<int:category_id>/<int:year_id>/<int:month_id>', view_data_adress_admin, name="category_view_admin"),
]
