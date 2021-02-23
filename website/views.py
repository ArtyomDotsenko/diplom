from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from .models import Consumption, Category
from website.forms import UserRegisterForm, UserLoginForm, AddDataForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return render(request, 'website/main.html')


class AdressList(LoginRequiredMixin, generic.ListView):
    model = Consumption
    template_name = 'website/main.html'
    context_object_name = 'adress'

    def get_queryset(self):
        return Consumption.objects.filter(adress=self.request.user.profile.adress)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # авто логин в систему
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'website/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'website/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def add_data_adress(request, category_id):
    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            fact = form.cleaned_data['fact']
            adress = request.user.profile.adress
            organization = request.user.profile.organization
            limit = 1
            category = Category.objects.get(pk=category_id)
            data = Consumption(adress=adress, organization=organization, fact=fact, limit=limit, category=category)
            data.save()
            return redirect('index')
    else:
        form = AddDataForm()
        category = Category.objects.get(pk=category_id)
    context = {'form': form, 'category': category}
    return render(request, 'website/add_data_adress.html', context)


def view_data_adress(request, category_id):
    data = Consumption.objects.filter(adress=request.user.profile.adress).filter(category=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'website/view_consumption.html', {'adress': data, 'category': category})
