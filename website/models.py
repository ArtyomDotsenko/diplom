from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class MunicipalOrganizations(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование муниципальной организации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'муниципальная организация'
        verbose_name_plural = 'муниципальные организации'
        ordering = ['title']


class AddressGroup(models.Model):
    titleOfTheAddressGroup = models.CharField(max_length=150, verbose_name='Наименование группы адресов')

    def __str__(self):
        return self.titleOfTheAddressGroup

    class Meta:
        verbose_name = 'группа адресов'
        verbose_name_plural = 'группы адресов'
        ordering = ['titleOfTheAddressGroup']


class Address(models.Model):
    titleOfTheAddress = models.CharField(max_length=150, verbose_name='Наименование учреждения или адрес расположение объекта')
    zona = models.ForeignKey('Zona', on_delete=models.PROTECT, null=True, verbose_name='Зона')

    def __str__(self):
        return self.titleOfTheAddress

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'
        ordering = ['titleOfTheAddress']


class AddressOfTheMunicipalOrganizations(models.Model):
    municipalOrganization = models.ForeignKey('MunicipalOrganizations', on_delete=models.CASCADE, verbose_name='Муниципальная организация', related_name='TheMunicipalOrganizations')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Учреждения или адрес расположение объекта', related_name='TheAddress')
    group = models.ForeignKey('AddressGroup', on_delete=models.CASCADE, verbose_name='Группа адресов', null=True, blank=True, related_name='TheAddressGroup')
    # addToGroup = models.BooleanField(verbose_name='Дбавить группу адресов?')
    # group2 = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Наименование группы адресов', null=True, blank=True, related_name='TheAddressGroup', )

    def __str__(self):
        if self.group:
            return '{0}:  [{1}]'.format(self.group, self.address.titleOfTheAddress)
        return self.address.titleOfTheAddress

    class Meta:
        verbose_name = 'адрес муниципальной организации'
        verbose_name_plural = 'адреса муниципальной организации'
        ordering = ['municipalOrganization', 'address', 'group']







# class Organization(models.Model):
#     name = models.CharField(max_length=150, verbose_name="Имя организации")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Организация"
#         verbose_name_plural = "Организации"


# class MainAdress(models.Model):
#     name = models.CharField(max_length=150, verbose_name="Главный адрес")
#     organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Главный адрес"
#         verbose_name_plural = "Главные адреса"


# class Adress(models.Model):
#     name = models.CharField(max_length=150, verbose_name="Адрес")
#     main_adress = models.ForeignKey('MainAdress', on_delete=models.PROTECT, null=True, verbose_name="Главный адрес")
#     organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
#     zona = models.ForeignKey('Zona', on_delete=models.PROTECT, null=True, verbose_name='Зона')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Адрес"
#         verbose_name_plural = "Адреса"


class Category(models.Model):
    title = models.CharField(max_length=120, db_index=True, verbose_name="Наименование категории")

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вид энергоресурсов"
        verbose_name_plural = "Виды энергоресурсов"
        ordering = ['title']


class Tarif(models.Model):
    value = models.FloatField(verbose_name='Тариф', max_length=20)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория услуги')
    zona = models.ForeignKey('Zona', on_delete=models.PROTECT, verbose_name='Зона')
    polugodie = models.ForeignKey('Polugodie', on_delete=models.PROTECT, verbose_name='Полугодие')
    god = models.ForeignKey('God', on_delete=models.PROTECT, verbose_name='Год')

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class Zona(models.Model):
    name = models.TextField(null=False, verbose_name='Зона')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Зона"
        verbose_name_plural = "Зоны"


class Month(models.Model):
    name = models.TextField(verbose_name='Месяц')
    polugodie = models.ForeignKey('Polugodie', on_delete=models.PROTECT, verbose_name='Полугодие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Месяц"
        verbose_name_plural = "Месяцы"


class Polugodie(models.Model):
    name = models.CharField(null=False, max_length=10, verbose_name='Полугодие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Полугодие"
        verbose_name_plural = "Полугодия"


class God(models.Model):
    name = models.IntegerField(null=False, verbose_name='Год')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Года"


class Consumption(models.Model):
    # adress = models.ForeignKey('Address', on_delete=models.PROTECT, null=False, verbose_name="Адрес")
    # main_adress = models.ForeignKey('AddressGroup', on_delete=models.PROTECT, null=False, verbose_name="Главный адрес")
    # organization = models.ForeignKey('MunicipalOrganizations', on_delete=models.PROTECT, null=True, verbose_name="Организация")
    address_of_the_municipal_organization = models.ForeignKey('AddressOfTheMunicipalOrganizations', on_delete=models.CASCADE)
    fact = models.FloatField(default=0, verbose_name='Фактическое потребление')
    limit = models.FloatField(default=0, verbose_name='Лимит потребления') # Временно
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория услуги')
    otklonenie = models.FloatField(max_length=30, editable=False)
    otklonenie_percent = models.FloatField(max_length=30, editable=False)
    month = models.ForeignKey('Month', on_delete=models.PROTECT, verbose_name='Месяц', null=True)
    god = models.ForeignKey('God', on_delete=models.PROTECT, null=True, verbose_name='Год')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    sum = models.FloatField(default=0, editable=False, verbose_name='Сумма, выставленная по счетам, тыс.руб. (с НДС)')

    def get_otklonenie(self):
        result = self.limit - self.fact
        return result

    def get_otklonenie_percent(self):
        result = self.otklonenie / self.limit
        return result

    # def get_main_adress(self):
    #     result = AddressGroup.objects.get(adress__name=self.adress)
    #     return result

    def get_sum(self):
        zona = Zona.objects.get(address__titleOfTheAddress=self.address_of_the_municipal_organization.address)
        polugodie = Polugodie.objects.get(month__name=self.month)
        result = Tarif.objects.filter(category=self.category).filter(zona=zona).filter(polugodie=polugodie).filter(god=self.god)
        x = result[0]
        x = float(str(x))
        print(x)
        sum = (self.fact * x) / 1000
        return sum

    def save(self, *args, **kwargs):
        self.otklonenie = self.get_otklonenie()
        self.otklonenie_percent = self.get_otklonenie_percent()
        self.sum = self.get_sum()
        # self.main_adress = self.get_main_adress()
        super(Consumption, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.address_of_the_municipal_organization)

    class Meta:
        verbose_name = "Отопление"
        verbose_name_plural = "Отопление"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # adress = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, verbose_name="Адрес")
    adress = models.ForeignKey('AddressOfTheMunicipalOrganizations', on_delete=models.CASCADE, null=True, verbose_name="Адрес")
    organization = models.ForeignKey('MunicipalOrganizations', on_delete=models.CASCADE, null=True, verbose_name="Организация")

    class Meta:
        ordering = ['user']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



