from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from .models import Consumption, Category, God, Polugodie, Month, \
    AddressOfTheMunicipalOrganizations, AddressGroup, Address
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
        return Consumption.objects.all()


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
    adress_list = AddressOfTheMunicipalOrganizations.objects.filter(municipalOrganization__title=request.user.profile.organization.title)
    str_adress_list = []
    for i in adress_list:
        str_adress_list.append(str(i))

    x = len(adress_list)
    FS = formset_factory(AddDataForm, extra=x)
    category_for_post = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        print('hahhah')
        form = FS(request.POST)
        m_y_form = MonthYear(request.POST)
        zip_list = zip(adress_list, form)
        if all([form.is_valid(), m_y_form.is_valid()]):
            # category_for_post = Category.objects.get(pk=category_id)
            i = 0
            month = m_y_form.cleaned_data['month']
            god = m_y_form.cleaned_data['god']
            for form in form:
                if form.cleaned_data:
                    print(1)
                    fact = form.cleaned_data['fact']
                    adress = adress_list[i]
                    print(adress)
                    # organization = request.user.profile.organization
                    limit = form.cleaned_data['limit']
                    # category_for_post = Category.objects.get(pk=category_id)
                    # month = form.cleaned_data['month']
                    # god = form.cleaned_data['god']
                    data = Consumption(address_of_the_municipal_organization=adress, fact=fact, limit=limit,
                                       category=category_for_post, month=month, god=god)
                    print(data)
                    data.save()
                    i = i + 1
            return redirect('index')
    else:
        print('hahhah')
        form = FS()
        m_y_form = MonthYear()
        # category_for_save = Category.objects.get(pk=category_id)
        zip_list = zip(adress_list, form)
    context = {'form': form, 'm_y_form': m_y_form, 'adress_list': str_adress_list, 'category': category_for_post,
               'zip_list': zip_list}
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
    adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization__title=request.user.profile.organization.title)
    for item in adress_list:
        print(item.municipalOrganization, item.address)

    all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.all()
    table = Consumption.objects.all()
    # AddressData = Table.objects.order_by('address').values('address__group').filter(address__group_id__isnull=False).annotate(fact=Sum('fact'), limit=Sum('limit'))
    group_data = AddressGroup.objects.annotate(fact=Sum('TheAddressGroup__consumption__fact'),
                                               limit=Sum('TheAddressGroup__consumption__limit'),
                                               otklonenie=Sum('TheAddressGroup__consumption__otklonenie'),
                                               otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent'),
                                               sum=Sum('TheAddressGroup__consumption__sum'))

    list_group_data = []
    for one_address in all_address_of_the_municipal_organizations:
        if(one_address.group is None):
            table_address_without_group_data = Consumption.objects.filter(address_of_the_municipal_organization=one_address)
            for one_table_address_without_group_data in table_address_without_group_data:
                list_group_data.append(one_table_address_without_group_data)
        elif one_address.group not in list_group_data:
            for one_group_data in group_data:
                list_group_data.append(one_group_data)
                table_address_with_group_data = Consumption.objects.filter(address_of_the_municipal_organization__group=one_group_data)
                for one_table_address_with_group_data in table_address_with_group_data:
                    list_group_data.append(one_table_address_with_group_data)

    return render(request, 'website/view_consumption.html', {'all_address': all_address_of_the_municipal_organizations,
                                                          'all_table': table, 'list_group_data': list_group_data})





# def view_data_adress(request, category_id):
#     adress_list = Adress.objects.filter(organization__name=request.user.profile.organization.name)
#     print(adress_list)
#     data = Consumption.objects.filter(organization=request.user.profile.organization).filter(category=category_id)
#     main_data = MainAdress.objects.filter(organization=request.user.profile.organization)
#
#     main_adress = MainAdress.objects.annotate(fact=Sum('consumption__fact'), limit=Sum('consumption__limit'),
#                                               otklonenie=Sum('consumption__otklonenie'),
#                                               otklonenie_percent=Sum('consumption__otklonenie_percent'),
#                                               sum=Sum('consumption__sum'))
#     main_adr = MainAdress.objects.all()
#     list = []
#     for main_ad in main_adress:
#         list.append(main_ad)
#         con = Consumption.objects.filter(main_adress=main_ad)
#         for item in con:
#             list.append(item)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'website/view_consumption.html', {'adress': data, 'category': category, 'list': list,
#                                                              "main_adress": main_adr})





#
# def view_data_adress(request, category_id):
#     data = Consumption.objects.filter(adress=request.user.profile.adress).filter(category=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'website/view_consumption.html', {'adress': data, 'category': category})
