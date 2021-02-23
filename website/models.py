from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Organization(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя организации")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class MainAdress(models.Model):
    name = models.CharField(max_length=150, verbose_name="Главный адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Главный адрес"
        verbose_name_plural = "Главные адреса"


class Adress(models.Model):
    name = models.CharField(max_length=150, verbose_name="Адрес")
    main_adress = models.ForeignKey('MainAdress', on_delete=models.PROTECT, null=True, verbose_name="Главный адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


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


class Consumption(models.Model):
    adress = models.ForeignKey('Adress', on_delete=models.PROTECT, null=False, verbose_name="Адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
    fact = models.FloatField(default=0, verbose_name='Фактическое потребление')
    limit = models.FloatField(default=0, verbose_name='Лимит потребления') # Временно
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория услуги')
    otklonenie = models.FloatField(max_length=30, editable=False)
    otklonenie_percent = models.FloatField(max_length=30, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def get_otklonenie(self):
        result = self.limit - self.fact
        return result

    def get_otklonenie_percent(self):
        result = self.otklonenie - self.limit
        return result

    def save(self, *args, **kwargs):
        self.otklonenie = self.get_otklonenie()
        self.otklonenie_percent = self.get_otklonenie_percent()
        super(Consumption, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.adress)

    class Meta:
        verbose_name = "Отопление"
        verbose_name_plural = "Отопление"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE, null=True, verbose_name="Адрес")
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, verbose_name="Организация")

    class Meta:
        ordering = ['user']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



