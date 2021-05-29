from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q, F
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from .models import Consumption, Category, God, Polugodie, Month, \
    AddressOfTheMunicipalOrganizations, AddressGroup, Address, MunicipalOrganizations, Quarter
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
    print(adress_list, 99)
    str_adress_list = []
    for i in adress_list:
        str_adress_list.append(str(i))


    x = len(adress_list)
    FS = formset_factory(AddDataForm, extra=x)
    category_for_post = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = FS(request.POST, request.FILES)
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
                    explanatory_note = form.cleaned_data['explanatory_note']
                    if fact > limit and not explanatory_note:
                        print(888)
                        messages.error(request,
                                       'Внимание по одному из адресов факт превышает лимит, необходимо прикрепить пояснительную записку!')
                        return redirect(request.path)
                    note = form.cleaned_data['note']
                    data = Consumption(address_of_the_municipal_organization=adress, fact=fact, limit=limit,
                                       category=category_for_post, month=month, god=god,
                                       explanatory_note=explanatory_note,
                                       note=note)
                    data.save()
                    i = i + 1
            messages.success(request, 'Данные успешно добавлены')
            return redirect(request.path)
        else:
            messages.error(request, 'Ошибка! Данные не отправлены')
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
    sum_data = Consumption.objects.filter(category=category_id).filter(
        god=year_id).filter(month=month_id).filter(
        address_of_the_municipal_organization__municipalOrganization=request.user.profile.organization)
    sum_data_final = sum_data.aggregate(fact=Sum('fact'), limit=Sum('limit'), otklonenie=Sum('otklonenie'),
                                        otklonenie_percent=Sum('otklonenie_percent'), sum=Sum('sum'))

    category = Category.objects.get(pk=category_id)
    adress_list = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization__title=request.user.profile.organization.title)

    all_address_of_the_municipal_organizations = AddressOfTheMunicipalOrganizations.objects.filter(
        municipalOrganization=request.user.profile.organization)

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
                   'list_group_data': list_group_data, 'category': category,
                   'year': year, 'month': month, 'sum_data_final': sum_data_final})


def view_data_adress_admin(request, category_id, year_id, month_id):
    year = God.objects.get(pk=year_id)
    month = Month.objects.get(pk=month_id)
    category = Category.objects.get(pk=category_id)

    sum_data = Consumption.objects.filter(category=category_id).filter(
        god=year_id).filter(month=month_id)
    print(sum_data)
    sum_data_final = sum_data.aggregate(fact=Sum('fact'), limit=Sum('limit'), otklonenie=Sum('otklonenie'),
                                        otklonenie_percent=Sum('otklonenie_percent'), sum=Sum('sum'))
    print(sum_data_final)

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
                           'year': year, 'month': month, 'form': form, 'sum_data_final': sum_data_final})
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
                       'year': year, 'month': month, 'form': form, 'sum_data_final': sum_data_final})


def view_quarter_adress_admin(request, category_id, year_id, quarter_id):
    year = God.objects.get(pk=year_id)
    month = Month.objects.get(pk=1)
    new_month = Month.objects.filter(quarter_id=quarter_id)
    one_m = new_month[0]
    two_m = new_month[1]
    three_m = new_month[2]
    quarter = Quarter.objects.get(id=quarter_id)
    category = Category.objects.get(pk=category_id)

    sum_data = Consumption.objects.filter(category=category_id).filter(
        god=year_id).filter(Q(month=one_m) | Q(month=two_m) | Q(month=three_m))
    # print(sum_data)
    sum_data_final = sum_data.aggregate(fact=Sum('fact'), limit=Sum('limit'), otklonenie=Sum('otklonenie'),
                                        otklonenie_percent=Sum('otklonenie_percent'), sum=Sum('sum'))

    if request.method == 'POST':
        form = OrganizationsForm(request.POST)
        if form.is_valid():
            organization = form.cleaned_data['organizations']
            all_address = AddressOfTheMunicipalOrganizations.objects.filter(
                municipalOrganization=organization)
            all_address_final = all_address.annotate(fact=Sum('consumption__fact',
                                                              filter=(Q(consumption__month=Month.objects.get(
                                                                  name=one_m),
                                                                        consumption__god=God.objects.get(pk=year_id),
                                                                        consumption__category=Category.objects.get(
                                                                            pk=category_id))) | Q(
                                                                  consumption__month=Month.objects.get(name=two_m),
                                                                  consumption__god=God.objects.get(pk=year_id),
                                                                  consumption__category=Category.objects.get(
                                                                      pk=category_id)
                                                              ) | Q(consumption__month=Month.objects.get(name=three_m),
                                                                    consumption__god=God.objects.get(pk=year_id),
                                                                    consumption__category=Category.objects.get(
                                                                        pk=category_id))),
                                                     limit=Sum('consumption__limit',
                                                               filter=(Q(consumption__month=Month.objects.get(
                                                                   name=one_m),
                                                                         consumption__god=God.objects.get(pk=year_id),
                                                                         consumption__category=Category.objects.get(
                                                                             pk=category_id))) | Q(
                                                                   consumption__month=Month.objects.get(name=two_m),
                                                                   consumption__god=God.objects.get(pk=year_id),
                                                                   consumption__category=Category.objects.get(
                                                                       pk=category_id)
                                                               ) | Q(consumption__month=Month.objects.get(name=three_m),
                                                                     consumption__god=God.objects.get(pk=year_id),
                                                                     consumption__category=Category.objects.get(
                                                                         pk=category_id))),
                                                     otklonenie=Sum('consumption__otklonenie',
                                                                    filter=(Q(consumption__month=Month.objects.get(
                                                                        name=one_m),
                                                                        consumption__god=God.objects.get(pk=year_id),
                                                                        consumption__category=Category.objects.get(
                                                                            pk=category_id))) | Q(
                                                                        consumption__month=Month.objects.get(
                                                                            name=two_m),
                                                                        consumption__god=God.objects.get(pk=year_id),
                                                                        consumption__category=Category.objects.get(
                                                                            pk=category_id)
                                                                    ) | Q(
                                                                        consumption__month=Month.objects.get(
                                                                            name=three_m),
                                                                        consumption__god=God.objects.get(pk=year_id),
                                                                        consumption__category=Category.objects.get(
                                                                            pk=category_id))),
                                                     otklonenie_percent=Sum('consumption__otklonenie_percent',
                                                                            filter=(
                                                                                   Q(consumption__month=Month.objects.get(
                                                                                       name=one_m),
                                                                                       consumption__god=God.objects.get(
                                                                                           pk=year_id),
                                                                                       consumption__category=Category.objects.get(
                                                                                           pk=category_id))) | Q(
                                                                                consumption__month=Month.objects.get(
                                                                                    name=two_m),
                                                                                consumption__god=God.objects.get(
                                                                                    pk=year_id),
                                                                                consumption__category=Category.objects.get(
                                                                                    pk=category_id)
                                                                            ) | Q(consumption__month=Month.objects.get(
                                                                                name=three_m),
                                                                                consumption__god=God.objects.get(
                                                                                    pk=year_id),
                                                                                consumption__category=Category.objects.get(
                                                                                    pk=category_id))),
                                                     sum=Sum('consumption__sum',
                                                             filter=(Q(consumption__month=Month.objects.get(
                                                                 name=one_m),
                                                                 consumption__god=God.objects.get(
                                                                     pk=year_id),
                                                                 consumption__category=Category.objects.get(
                                                                     pk=category_id))) | Q(
                                                                 consumption__month=Month.objects.get(
                                                                     name=two_m),
                                                                 consumption__god=God.objects.get(
                                                                     pk=year_id),
                                                                 consumption__category=Category.objects.get(
                                                                     pk=category_id)
                                                             ) | Q(consumption__month=Month.objects.get(
                                                                 name=three_m),
                                                                 consumption__god=God.objects.get(
                                                                     pk=year_id),
                                                                 consumption__category=Category.objects.get(
                                                                     pk=category_id)))).order_by('address')
            print('Адреса')
            for i in all_address_final:
                print(i, i.fact)



            filtered_group_data = AddressGroup.objects.filter(
                TheAddressGroup__consumption__address_of_the_municipal_organization__municipalOrganization__title=organization).distinct()
            group_data_filtered = filtered_group_data.annotate(
                fact=Sum('TheAddressGroup__consumption__fact',
                         filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                   TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                   TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                             TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                             TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                             TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                             TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                             TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                             TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                limit=Sum('TheAddressGroup__consumption__limit',
                          filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                    TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                    TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                              TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                              TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                              TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                              TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                              TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                              TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
                               filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                         TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                         TheAddressGroup__consumption__category=Category.objects.get(
                                             pk=category_id))) | Q(
                                   TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                                   TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                   TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                                   TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                                   TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                   TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
                                       filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(
                                           name=one_m),
                                                 TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                                 TheAddressGroup__consumption__category=Category.objects.get(
                                                     pk=category_id))) | Q(
                                           TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                                           TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                           TheAddressGroup__consumption__category=Category.objects.get(
                                               pk=category_id)) | Q(
                                           TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                                           TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                           TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
                sum=Sum('TheAddressGroup__consumption__sum',
                        filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                  TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                  TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                            TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                            TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                            TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                            TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                            TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                            TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)))).order_by()
            # for i in group_data_filtered:
            #     print(i, i.fact, i.limit)
            # print(group_data_filtered)

            list_group_data = []
            for one_address in all_address_final:
                if (one_address.group is None):
                    list_group_data.append(one_address)
                elif one_address.group not in list_group_data:
                    for one_group_data in group_data_filtered:
                        list_group_data.append(one_group_data)
                        table_address_with_group_data = all_address_final.filter(
                            group=one_group_data)
                        for k in table_address_with_group_data:
                            list_group_data.append(k)

            return render(request, 'website/view_consumption_quarter.html',
                          {'all_address': all_address_final,
                           'list_group_data': list_group_data, 'category': category,
                           'year': year, 'quarter': quarter, 'form': form, 'sum_data_final': sum_data_final})
    else:
        form = OrganizationsForm()
        filtered_group_data = AddressGroup.objects.all().distinct()

        all_address = AddressOfTheMunicipalOrganizations.objects.all()
        all_address_final = all_address.annotate(fact=Sum('consumption__fact',
                                                          filter=(Q(consumption__month=Month.objects.get(name=one_m),
                                                                    consumption__god=God.objects.get(pk=year_id),
                                                                    consumption__category=Category.objects.get(
                                                                        pk=category_id))) | Q(
                                                              consumption__month=Month.objects.get(name=two_m),
                                                              consumption__god=God.objects.get(pk=year_id),
                                                              consumption__category=Category.objects.get(
                                                                  pk=category_id)
                                                          ) | Q(consumption__month=Month.objects.get(name=three_m),
                                                                consumption__god=God.objects.get(pk=year_id),
                                                                consumption__category=Category.objects.get(
                                                                    pk=category_id))),
                                                 limit=Sum('consumption__limit',
                                                           filter=(Q(consumption__month=Month.objects.get(name=one_m),
                                                                     consumption__god=God.objects.get(pk=year_id),
                                                                     consumption__category=Category.objects.get(
                                                                         pk=category_id))) | Q(
                                                               consumption__month=Month.objects.get(name=two_m),
                                                               consumption__god=God.objects.get(pk=year_id),
                                                               consumption__category=Category.objects.get(
                                                                   pk=category_id)
                                                           ) | Q(consumption__month=Month.objects.get(name=three_m),
                                                                 consumption__god=God.objects.get(pk=year_id),
                                                                 consumption__category=Category.objects.get(
                                                                     pk=category_id))),
                                                 otklonenie=Sum('consumption__otklonenie',
                                                                filter=(Q(consumption__month=Month.objects.get(
                                                                    name=one_m),
                                                                    consumption__god=God.objects.get(pk=year_id),
                                                                    consumption__category=Category.objects.get(
                                                                        pk=category_id))) | Q(
                                                                    consumption__month=Month.objects.get(name=two_m),
                                                                    consumption__god=God.objects.get(pk=year_id),
                                                                    consumption__category=Category.objects.get(
                                                                        pk=category_id)
                                                                ) | Q(
                                                                    consumption__month=Month.objects.get(name=three_m),
                                                                    consumption__god=God.objects.get(pk=year_id),
                                                                    consumption__category=Category.objects.get(
                                                                        pk=category_id))),
                                                 otklonenie_percent=Sum('consumption__otklonenie_percent',
                                                                        filter=(Q(consumption__month=Month.objects.get(
                                                                            name=one_m),
                                                                            consumption__god=God.objects.get(
                                                                                pk=year_id),
                                                                            consumption__category=Category.objects.get(
                                                                                pk=category_id))) | Q(
                                                                            consumption__month=Month.objects.get(
                                                                                name=two_m),
                                                                            consumption__god=God.objects.get(
                                                                                pk=year_id),
                                                                            consumption__category=Category.objects.get(
                                                                                pk=category_id)
                                                                        ) | Q(consumption__month=Month.objects.get(
                                                                            name=three_m),
                                                                            consumption__god=God.objects.get(
                                                                                pk=year_id),
                                                                            consumption__category=Category.objects.get(
                                                                                pk=category_id))),
                                                 sum=Sum('consumption__sum',
                                                         filter=(Q(consumption__month=Month.objects.get(
                                                             name=one_m),
                                                             consumption__god=God.objects.get(
                                                                 pk=year_id),
                                                             consumption__category=Category.objects.get(
                                                                 pk=category_id))) | Q(
                                                             consumption__month=Month.objects.get(
                                                                 name=two_m),
                                                             consumption__god=God.objects.get(
                                                                 pk=year_id),
                                                             consumption__category=Category.objects.get(
                                                                 pk=category_id)
                                                         ) | Q(consumption__month=Month.objects.get(
                                                             name=three_m),
                                                             consumption__god=God.objects.get(
                                                                 pk=year_id),
                                                             consumption__category=Category.objects.get(
                                                                 pk=category_id)))).order_by('address')


        group_data_filtered = filtered_group_data.annotate(
            fact=Sum('TheAddressGroup__consumption__fact',
                     filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                               TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                               TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                         TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                         TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                         TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                         TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                         TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                         TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            limit=Sum('TheAddressGroup__consumption__limit',
                      filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                          TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                          TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                          TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                          TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                          TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                          TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            otklonenie=Sum('TheAddressGroup__consumption__otklonenie',
                           filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                     TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                     TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                               TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                               TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                               TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                               TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                               TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                               TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            otklonenie_percent=Sum('TheAddressGroup__consumption__otklonenie_percent',
                                   filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                                             TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                             TheAddressGroup__consumption__category=Category.objects.get(
                                                 pk=category_id))) | Q(
                                       TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                                       TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                       TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                                       TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                                       TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                                       TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))),
            sum=Sum('TheAddressGroup__consumption__sum',
                    filter=(Q(TheAddressGroup__consumption__month__name=Month.objects.get(name=one_m),
                              TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                              TheAddressGroup__consumption__category=Category.objects.get(pk=category_id))) | Q(
                        TheAddressGroup__consumption__month__name=Month.objects.get(name=two_m),
                        TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                        TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)) | Q(
                        TheAddressGroup__consumption__month__name=Month.objects.get(name=three_m),
                        TheAddressGroup__consumption__god=God.objects.get(pk=year_id),
                        TheAddressGroup__consumption__category=Category.objects.get(pk=category_id)))).order_by()

        list_group_data = []
        for one_address in all_address_final:
            if (one_address.group is None):
                list_group_data.append(one_address)
            elif one_address.group not in list_group_data:
                for one_group_data in group_data_filtered:
                    list_group_data.append(one_group_data)
                    table_address_with_group_data = all_address_final.filter(
                        group=one_group_data)
                    for k in table_address_with_group_data:
                        list_group_data.append(k)

        return render(request, 'website/view_consumption_quarter.html',
                      {'all_address': all_address_final,
                       'list_group_data': list_group_data, 'category': category,
                       'year': year, 'quarter': quarter, 'form': form, 'sum_data_final': sum_data_final})
