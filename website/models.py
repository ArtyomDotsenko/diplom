from django.db import models


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


class Otoplenie(models.Model):
    adress = models.ForeignKey('Adress', on_delete=models.PROTECT, null=False, verbose_name="Адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
    fact = models.FloatField(default=0, verbose_name='Фактическое потребление')
    limit = models.FloatField(default=0, verbose_name='Лимит потребления') # Временно
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return str(self.adress)

    class Meta:
        verbose_name = "Отопление"
        verbose_name_plural = "Отопление"
