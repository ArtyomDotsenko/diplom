from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from .models import Consumption, Category, God, Polugodie, Month, \
    AddressOfTheMunicipalOrganizations, AddressGroup, Address, MunicipalOrganizations
from website.forms import UserRegisterForm, UserLoginForm, AddDataForm, MonthYear, OrganizationsForm

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
    adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization__title=request.user.profile.organization.title)
    str_adress_list = []
    for i in adress_list:
        str_adress_list.append(str(i))

    x = len(adress_list)
    FS = formset_factory(AddDataForm, extra=x)
    category_for_post = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = FS(request.POST)
        m_y_form = MonthYear(request.POST)
        zip_list = zip(adress_list, form)
        if all([form.is_valid(), m_y_form.is_valid()]):
            i = 0
            month = m_y_form.cleaned_data['month']
            god = m_y_form.cleaned_data['god']
            for form in form:
                if form.cleaned_data:
                    fact = form.cleaned_data['fact']
                    adress = adress_list[i]
                    limit = form.cleaned_data['limit']
                    data = Consumption(address_of_the_municipal_organization=adress, fact=fact, limit=limit,
                                       category=category_for_post, month=month, god=god)
                    data.save()
                    i = i + 1
            return redirect('index')
    else:
        form = FS()
        m_y_form = MonthYear()
        zip_list = zip(adress_list, form)
    context = {'form': form, 'm_y_form': m_y_form, 'adress_list': str_adress_list, 'category': category_for_post,
               'zip_list': zip_list}
    return render(request, 'website/add_data_adress.html', context)


def view_data_adress(request, category_id, year_id, month_id):
    year = God.objects.get(pk=year_id)
    month = Month.objects.get(pk=month_id)

    category = Category.objects.get(pk=category_id)
    adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization__title=request.user.profile.organization.title)

    # if request.user.profile.organization.title == "admin":
    #     all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.all()
    #     filtered_group_data = AddressGroup.objects.all().distinct()
    # else:
    #     all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
    #         municipalOrganization=request.user.profile.organization)
    #     filtered_group_data = AddressGroup.objects.filter(
    #         TheAddressGroup__consumption__address_of_the_municipal_organization__municipalOrganization__title=request.user.
    #             profile.organization.title).distinct()
    # print("Муниципальные организации", all_address_of_the_municipal_organizations)

    all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization=request.user.profile.organization)
    table = Consumption.objects.all()

    filtered_group_data = AddressGroup.objects.filter(
        TheAddressGroup__consumption__address_of_the_municipal_organization__municipalOrganization__title=request.user.
            profile.organization.title).distinct()
    group_data_filtered = filtered_group_data.annotate(
        fact=Sum('TheAddressGroup__consumption__fact',
                 filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                          TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                          TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
        limit=Sum('TheAddressGroup__consumption__limit',
                  filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                           TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                           TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
        otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
                       filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
        otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
                               filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                        TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                        TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
        sum=Sum('TheAddressGroup__consumption__sum',
                filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                         TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                         TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)))).order_by()
    print(group_data_filtered)

    # group_data = AddressGroup.objects.annotate(
    #     fact=Sum('TheAddressGroup__consumption__fact', filter=Q(TheAddressGroup__consumption__month__name='Январь', TheAddressGroup__consumption__god=God.objects.get(pk=1), TheAddressGroup__consumption__category=Category.objects.get(pk=1))),
    #     limit=Sum('TheAddressGroup__consumption__limit', filter=Q(TheAddressGroup__consumption__month__name='Январь', TheAddressGroup__consumption__god=God.objects.get(pk=1), TheAddressGroup__consumption__category=Category.objects.get(pk=1))),
    #     otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
    #                    filter=Q(TheAddressGroup__consumption__month__name='Январь', TheAddressGroup__consumption__god=God.objects.get(pk=1), TheAddressGroup__consumption__category=Category.objects.get(pk=1))),
    #     otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
    #                            filter=Q(TheAddressGroup__consumption__month__name='Январь', TheAddressGroup__consumption__god=God.objects.get(pk=1), TheAddressGroup__consumption__category=Category.objects.get(pk=1))),
    #     sum=Sum('TheAddressGroup__consumption__sum',
    #             filter=Q(TheAddressGroup__consumption__month__name='Январь', TheAddressGroup__consumption__god=God.objects.get(pk=1), TheAddressGroup__consumption__category=Category.objects.get(pk=1)))) #.filter(TheAddressGroup__consumption__address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title).distinct()
    # print(group_data, "group data")

    list_group_data = []
    for one_address in all_address_of_the_municipal_organizations:
        if (one_address.group is None):
            table_address_without_group_data = Consumption.objects.filter(
                address_of_the_municipal_organization=one_address).filter(god=God.objects.get(pk=year_id)).filter(
                month=Month.objects.get(
                    pk=month_id)).filter(category=Category.objects.get(pk=category_id))
            for one_table_address_without_group_data in table_address_without_group_data:
                list_group_data.append(one_table_address_without_group_data)
        elif one_address.group not in list_group_data:
            for one_group_data in group_data_filtered:
                list_group_data.append(one_group_data)
                table_address_with_group_data = Consumption.objects.filter(
                    address_of_the_municipal_organization__group=one_group_data).filter(
                    god=God.objects.get(pk=year_id)).filter(month=Month.objects.get(
                    pk=month_id)).filter(category=Category.objects.get(pk=category_id))
                for one_table_address_with_group_data in table_address_with_group_data:
                    list_group_data.append(one_table_address_with_group_data)
    print(list_group_data, 444)

    return render(request, 'website/view_consumption.html',
                  {'all_address': all_address_of_the_municipal_organizations,
                   'all_table': table, 'list_group_data': list_group_data, 'category': category,
                   'year': year, 'month': month})


def view_data_adress_admin(request, category_id, year_id, month_id):
    year = God.objects.get(pk=year_id)
    month = Month.objects.get(pk=month_id)
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        form = OrganizationsForm(request.POST)
        if form.is_valid():
            organization = form.cleaned_data['organizations']
            all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
                municipalOrganization=organization)
            filtered_group_data = AddressGroup.objects.filter(
                TheAddressGroup__consumption__address_of_the_municipal_organization__municipalOrganization__title=organization).distinct()
            group_data_filtered = filtered_group_data.annotate(
                fact=Sum('TheAddressGroup__consumption__fact',
                         filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                  TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                  TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                limit=Sum('TheAddressGroup__consumption__limit',
                          filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                   TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                   TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
                               filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                        TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                        TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
                                       filter=Q(
                                           TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                           TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                           TheAddressGroup__consumption__category=Category.objects.get(
                                               pk=category_id))),
                sum=Sum('TheAddressGroup__consumption__sum',
                        filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                 TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                 TheAddressGroup__consumption__category=Category.objects.get(
                                     pk=category_id)))).order_by()
            print(group_data_filtered)

            list_group_data = []
            for one_address in all_address_of_the_municipal_organizations:
                if (one_address.group is None):
                    table_address_without_group_data = Consumption.objects.filter(
                        address_of_the_municipal_organization=one_address).filter(
                        god=God.objects.get(pk=year_id)).filter(
                        month=Month.objects.get(
                            pk=month_id)).filter(category=Category.objects.get(pk=category_id))
                    for one_table_address_without_group_data in table_address_without_group_data:
                        list_group_data.append(one_table_address_without_group_data)
                elif one_address.group not in list_group_data:
                    for one_group_data in group_data_filtered:
                        list_group_data.append(one_group_data)
                        table_address_with_group_data = Consumption.objects.filter(
                            address_of_the_municipal_organization__group=one_group_data).filter(
                            god=God.objects.get(pk=year_id)).filter(month=Month.objects.get(
                            pk=month_id)).filter(category=Category.objects.get(pk=category_id))
                        for one_table_address_with_group_data in table_address_with_group_data:
                            list_group_data.append(one_table_address_with_group_data)
            print(list_group_data, 444)

            return render(request, 'website/view_consumption.html',
                          {'all_address': all_address_of_the_municipal_organizations,
                           'list_group_data': list_group_data, 'category': category,
                           'year': year, 'month': month, 'form': form})
    else:
        form = OrganizationsForm()
        all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.all()
        filtered_group_data = AddressGroup.objects.all().distinct()
        group_data_filtered = filtered_group_data.annotate(
            fact=Sum('TheAddressGroup__consumption__fact',
                     filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                              TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                              TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            limit=Sum('TheAddressGroup__consumption__limit',
                      filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                               TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                               TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
                           filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                    TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                    TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
                                   filter=Q(
                                       TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                                       TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                       TheAddressGroup__consumption__category=Category.objects.get(
                                           pk=category_id))),
            sum=Sum('TheAddressGroup__consumption__sum',
                    filter=Q(TheAddressGroup__consumption__month__name=Month.objects.get(pk=month_id),
                             TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                             TheAddressGroup__consumption__category=Category.objects.get(
                                 pk=category_id)))).order_by()
        print(group_data_filtered)

        list_group_data = []
        for one_address in all_address_of_the_municipal_organizations:
            if (one_address.group is None):
                table_address_without_group_data = Consumption.objects.filter(
                    address_of_the_municipal_organization=one_address).filter(
                    god=God.objects.get(pk=year_id)).filter(
                    month=Month.objects.get(
                        pk=month_id)).filter(category=Category.objects.get(pk=category_id))
                for one_table_address_without_group_data in table_address_without_group_data:
                    list_group_data.append(one_table_address_without_group_data)
            elif one_address.group not in list_group_data:
                for one_group_data in group_data_filtered:
                    list_group_data.append(one_group_data)
                    table_address_with_group_data = Consumption.objects.filter(
                        address_of_the_municipal_organization__group=one_group_data).filter(
                        god=God.objects.get(pk=year_id)).filter(month=Month.objects.get(
                        pk=month_id)).filter(category=Category.objects.get(pk=category_id))
                    for one_table_address_with_group_data in table_address_with_group_data:
                        list_group_data.append(one_table_address_with_group_data)
        print(list_group_data, 444)

        return render(request, 'website/view_consumption.html',
                      {'all_address': all_address_of_the_municipal_organizations,
                       'list_group_data': list_group_data, 'category': category,
                       'year': year, 'month': month, 'form': form})



# def view_data_adress(request, category_id):
#     adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
#         municipalOrganization__title=request.user.profile.organization.title)
#     for item in adress_list:
#         print(item.municipalOrganization, item.address)
#
#     all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
#         municipalOrganization__title=request.user.profile.organization.title)
#     table = Consumption.objects.all()
#     # AddressData = Table.objects.order_by('address').values('address__group').filter(address__group_id__isnull=False).annotate(fact=Sum('fact'), limit=Sum('limit'))
#     group_data_january = AddressGroup.objects.annotate(
#         fact=Sum('TheAddressGroup__consumption__fact', filter=Q(TheAddressGroup__consumption__month__name='Январь')),
#         limit=Sum('TheAddressGroup__consumption__limit', filter=Q(TheAddressGroup__consumption__month__name='Январь')),
#         otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
#                        filter=Q(TheAddressGroup__consumption__month__name='Январь')),
#         otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
#                                filter=Q(TheAddressGroup__consumption__month__name='Январь')),
#         sum=Sum('TheAddressGroup__consumption__sum',
#                 filter=Q(TheAddressGroup__consumption__month__name='Январь')))
#
#     group_data_february = AddressGroup.objects.annotate(
#         fact=Sum('TheAddressGroup__consumption__fact', filter=Q(TheAddressGroup__consumption__month__name='Февраль')),
#         limit=Sum('TheAddressGroup__consumption__limit', filter=Q(TheAddressGroup__consumption__month__name='Февраль')),
#         otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
#                        filter=Q(TheAddressGroup__consumption__month__name='Февраль')),
#         otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
#                                filter=Q(TheAddressGroup__consumption__month__name='Февраль')),
#         sum=Sum('TheAddressGroup__consumption__sum',
#                 filter=Q(TheAddressGroup__consumption__month__name='Январь')))
#
#     list_group_data_january = []
#     for one_address in all_address_of_the_municipal_organizations:
#         if (one_address.group is None):
#             table_address_without_group_data = Consumption.objects.filter(
#                 address_of_the_municipal_organization=one_address).filter(god=God.objects.get(pk=1)).filter(
#                 month=Month.objects.get(
#                     pk=1))  # .filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#             for one_table_address_without_group_data in table_address_without_group_data:
#                 list_group_data_january.append(one_table_address_without_group_data)
#         elif one_address.group not in list_group_data_january:
#             for one_group_data in group_data_january:
#                 list_group_data_january.append(one_group_data)
#                 table_address_with_group_data = Consumption.objects.filter(
#                     address_of_the_municipal_organization__group=one_group_data).filter(
#                     god=God.objects.get(pk=1)).filter(month=Month.objects.get(
#                     pk=1))  # .filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#                 for one_table_address_with_group_data in table_address_with_group_data:
#                     list_group_data_january.append(one_table_address_with_group_data)
#     print(list_group_data_january)
#
#     list_group_data_february = []
#     for one_address in all_address_of_the_municipal_organizations:
#         if (one_address.group is None):
#             table_address_without_group_data = Consumption.objects.filter(
#                 address_of_the_municipal_organization=one_address).filter(god=God.objects.get(pk=1)).filter(
#                 month=Month.objects.get(
#                     pk=2))  # .filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#             for one_table_address_without_group_data in table_address_without_group_data:
#                 list_group_data_february.append(one_table_address_without_group_data)
#         elif one_address.group not in list_group_data_february:
#             for one_group_data in group_data_february:
#                 list_group_data_february.append(one_group_data)
#                 table_address_with_group_data = Consumption.objects.filter(
#                     address_of_the_municipal_organization__group=one_group_data).filter(
#                     god=God.objects.get(pk=1)).filter(month=Month.objects.get(
#                     pk=2))  # .filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#                 for one_table_address_with_group_data in table_address_with_group_data:
#                     list_group_data_february.append(one_table_address_with_group_data)
#     print(list_group_data_february)
#     super_list = zip(list_group_data_january, list_group_data_february)
#     return render(request, 'website/view_consumption_new.html',
#                   {'all_address': all_address_of_the_municipal_organizations,
#                    'all_table': table, 'list_group_data_january': list_group_data_january,
#                    'list_group_data_february': list_group_data_february,
#                    'super_list': super_list})

# def view_data_adress(request, category_id):
#     adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
#         municipalOrganization__title=request.user.profile.organization.title)
#     for item in adress_list:
#         print(item.municipalOrganization, item.address)
#
#     all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
#         municipalOrganization__title=request.user.profile.organization.title)
#     table = Consumption.objects.all()
#     # AddressData = Table.objects.order_by('address').values('address__group').filter(address__group_id__isnull=False).annotate(fact=Sum('fact'), limit=Sum('limit'))
#     group_data = AddressGroup.objects.annotate(fact=Sum('TheAddressGroup__consumption__fact'),
#                                                limit=Sum('TheAddressGroup__consumption__limit'),
#                                                otklonenie=Sum('TheAddressGroup__consumption__otklonenie'),
#                                                otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent'),
#                                                sum=Sum('TheAddressGroup__consumption__sum'))
#
#     list_group_data = []
#     for one_address in all_address_of_the_municipal_organizations:
#         if(one_address.group is None):
#             table_address_without_group_data = Consumption.objects.filter(address_of_the_municipal_organization=one_address).filter(god=God.objects.get(pk=1)).filter(month=Month.objects.get(pk=1)) #.filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#             for one_table_address_without_group_data in table_address_without_group_data:
#                 list_group_data.append(one_table_address_without_group_data)
#         elif one_address.group not in list_group_data:
#             for one_group_data in group_data:
#                 list_group_data.append(one_group_data)
#                 table_address_with_group_data = Consumption.objects.filter(address_of_the_municipal_organization__group=one_group_data).filter(god=God.objects.get(pk=1)).filter(month=Month.objects.get(pk=1)) #.filter(address_of_the_municipal_organization__municipalOrganization__title=request.user.profile.organization.title)
#                 for one_table_address_with_group_data in table_address_with_group_data:
#                     list_group_data.append(one_table_address_with_group_data)
#
#     return render(request, 'website/view_consumption.html', {'all_address': all_address_of_the_municipal_organizations,
#                                                           'all_table': table, 'list_group_data': list_group_data})


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
