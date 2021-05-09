from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from .models import Consumption, Category, MainAdress, Adress, God, Polugodie, Month
from website.forms import UserRegisterForm, UserLoginForm, AddDataForm, MonthYear

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
    adress_list = Adress.objects.filter(organization__name=request.user.profile.organization.name)
    str_adress_list = []
    for i in adress_list:
        str_adress_list.append(str(i))

    x = len(adress_list)
    FS = formset_factory(AddDataForm, extra=x)

    if request.method == 'POST':
        form = FS(request.POST)
        m_y_form = MonthYear(request.POST)
        if all([form.is_valid(), m_y_form.is_valid()]):
            i = 0
            month = m_y_form.cleaned_data['month']
            god = m_y_form.cleaned_data['god']
            for form in form:
                if form.cleaned_data:
                    fact = form.cleaned_data['fact']
                    adress = adress_list[i]
                    organization = request.user.profile.organization
                    limit = form.cleaned_data['limit']
                    category = Category.objects.get(pk=category_id)
                    # month = form.cleaned_data['month']
                    # god = form.cleaned_data['god']
                    data = Consumption(adress=adress, organization=organization, fact=fact, limit=limit, category=category,
                               month=month, god=god)
                    data.save()
                    i = i + 1
            return redirect('index')
    else:
        form = FS()
        m_y_form = MonthYear()
        category = Category.objects.get(pk=category_id)
    context = {'form': form, 'm_y_form': m_y_form, 'category': category, 'adress_list': str_adress_list}
    return render(request, 'website/add_data_adress.html', context)


# def add_data_adress(request, category_id):
#     if request.method == 'POST':
#         form = AddDataForm(request.POST)
#         if form.is_valid():
#             fact = form.cleaned_data['fact']
#             adress = request.user.profile.adress
#             organization = request.user.profile.organization
#             limit = form.cleaned_data['limit']
#             category = Category.objects.get(pk=category_id)
#             month = form.cleaned_data['month']
#             god = form.cleaned_data['god']
#             data = Consumption(adress=adress, organization=organization, fact=fact, limit=limit, category=category,
#                                month=month, god=god)
#             data.save()
#             return redirect('index')
#     else:
#         form = AddDataForm()
#         category = Category.objects.get(pk=category_id)
#     context = {'form': form, 'category': category}
#     return render(request, 'website/add_data_adress.html', context)


def view_data_adress(request, category_id):
    adress_list = Adress.objects.filter(organization__name=request.user.profile.organization.name)
    print(adress_list)
    data = Consumption.objects.filter(organization=request.user.profile.organization).filter(category=category_id)
    main_data = MainAdress.objects.filter(organization=request.user.profile.organization)

    main_adress = MainAdress.objects.annotate(fact=Sum('consumption__fact'), limit=Sum('consumption__limit'),
                                              otklonenie=Sum('consumption__otklonenie'),
                                              otklonenie_percent=Sum('consumption__otklonenie_percent'),
                                              sum=Sum('consumption__sum'))
    main_adr = MainAdress.objects.all()
    list = []
    for main_ad in main_adress:
        list.append(main_ad)
        con = Consumption.objects.filter(main_adress=main_ad)
        for item in con:
            list.append(item)
    category = Category.objects.get(pk=category_id)
    return render(request, 'website/view_consumption.html', {'adress': data, 'category': category, 'list': list,
                                                             "main_adress": main_adr})

# def view_data_adress(request, category_id):
#     data = Consumption.objects.filter(organization=request.user.profile.organization).filter(category=category_id)
#     main_data = MainAdress.objects.filter(organization=request.user.profile.organization)
#
#     main_adress = MainAdress.objects.annotate(fact=Sum('consumption__fact'), limit=Sum('consumption__limit'),
#                                               otklonenie=Sum('consumption__otklonenie'),
#                                               otklonenie_percent=Sum('consumption__otklonenie_percent'))
#     main_adr = MainAdress.objects.all()
#     list = []
#     list_name = []
#     for main_ad in main_adress:
#         list.append(main_ad)
#         list_name.append(main_ad.name)
#         adr = Adress.objects.filter(main_adress=main_ad)
#         con = Consumption.objects.filter(main_adress=main_ad)
#         for item1, item2 in zip(adr, con):
#             list_name.append(item1.name)
#             list.append(item2)
#
#     xxx = zip(list_name, list)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'website/view_consumption.html', {'adress': data, 'category': category, 'Hueta': xxx,
#                                                              "main_adress": main_adr})

# def view_data_adress(request, category_id):
#     data = Consumption.objects.filter(organization=request.user.profile.organization).filter(category=category_id)
#     main_data = MainAdress.objects.filter(organization=request.user.profile.organization)
#
#     main_adress = MainAdress.objects.annotate(fact=Sum('consumption__fact'), limit=Sum('consumption__limit'),
#                                               otklonenie=Sum('consumption__otklonenie'),
#                                               otklonenie_percent=Sum('consumption__otklonenie_percent'))
#     print(main_adress)
#     list_name = []
#     list_fact = []
#     list_limit = []
#     list_otklonenie = []
#     list_otklonenie_percent = []
#     for main_ad in main_adress:
#         list_name.append(main_ad.name)
#         list_fact.append(main_ad.fact)
#         list_limit.append(main_ad.limit)
#         list_otklonenie.append(main_ad.otklonenie)
#         list_otklonenie_percent.append(main_ad.otklonenie_percent)
#         print(main_ad.name, main_ad.fact, main_ad.limit, main_ad.otklonenie)
#         adr = Adress.objects.filter(main_adress=main_ad)
#         print(adr)
#         con = Consumption.objects.filter(main_adress=main_ad)
#         for item1, item2 in zip(adr, con):
#             list_name.append(item1.name)
#             list_fact.append(item2.fact)
#             list_limit.append(item2.limit)
#             list_otklonenie.append(item2.otklonenie)
#             list_otklonenie_percent.append(item2.otklonenie_percent)
#             print(item1.name, item2.fact, item2.limit)
#     xxx = zip(list_name, list_fact, list_limit, list_otklonenie, list_otklonenie_percent)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'website/view_consumption.html', {'adress': data, 'category': category,
#                                                              'data_name': list_name, 'data_fact': list_fact,
#                                                              'Hueta': xxx})

#
# def view_data_adress(request, category_id):
#     data = Consumption.objects.filter(adress=request.user.profile.adress).filter(category=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'website/view_consumption.html', {'adress': data, 'category': category})
