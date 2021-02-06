from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя организации")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Adress(models.Model):
    name = models.CharField(max_length=150, verbose_name="Адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=False, verbose_name="Организация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class CalcManager(models.Manager): # Наш менеджер, который нам дает возможность менять поведение модели
    def get_query_set(self):
        result=super(CalcManager, self).get_query_set().extra(select={'total': "first+second"})
        #то место где надо задавать алгоритм по которому вычисляется поле total
        return result


class Otoplenie(models.Model):
    adress = models.ForeignKey('Adress', on_delete=models.PROTECT, null=False, verbose_name="Адрес")
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
    fact = models.FloatField(default=0, verbose_name='Фактическое потребление')
    limit = models.FloatField(default=0, verbose_name='Лимит потребления') # Временно
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    total = CalcManager()
    objects = models.Manager()

    def __str__(self):
        return str(self.adress)

    class Meta:
        verbose_name = "Отопление"
        verbose_name_plural = "Отопление"


# class Otoplenie(models.Model):
#     adress = models.ForeignKey('Adress', on_delete=models.PROTECT, null=False, verbose_name="Адрес")
#     organization = models.ForeignKey('Organization', on_delete=models.PROTECT, null=True, verbose_name="Организация")
#     fact_jan = models.FloatField(default=0, verbose_name='Факт - январь')
#     limit_jan = models.FloatField(default=0, verbose_name='Лимит - январь') # Временно
#
#     fact_feb = models.FloatField(default=0, verbose_name='Факт - февраль')
#     limit_feb = models.FloatField(default=0, verbose_name='Лимит - февраль')
#
#     fact_mar = models.FloatField(default=0, verbose_name='Факт - март')
#     limit_mar = models.FloatField(default=0, verbose_name='Лимит - март')
#
#     fact_apr = models.FloatField(default=0, verbose_name='Факт - апрель')
#     limit_apr = models.FloatField(default=0, verbose_name='Лимит - апрель')
#
#     fact_may = models.FloatField(default=0, verbose_name='Факт - май')
#     limit_may = models.FloatField(default=0, verbose_name='Лимит - май')
#
#     fact_jun = models.FloatField(default=0, verbose_name='Факт - июнь')
#     limit_jun = models.FloatField(default=0, verbose_name='Лимит - июнь')
#
#     fact_jul = models.FloatField(default=0, verbose_name='Факт - июль')
#     limit_jul = models.FloatField(default=0, verbose_name='Лимит - июль')
#
#     fact_aug = models.FloatField(default=0, verbose_name='Факт - август')
#     limit_aug = models.FloatField(default=0, verbose_name='Лимит - август')
#
#     fact_sep = models.FloatField(default=0, verbose_name='Факт - сентябрь')
#     limit_sep = models.FloatField(default=0, verbose_name='Лимит - сентябрь')
#
#     fact_oct = models.FloatField(default=0, verbose_name='Факт - октябрь')
#     limit_oct = models.FloatField(default=0, verbose_name='Лимит - октябрь')
#
#     fact_nov = models.FloatField(default=0, verbose_name='Факт - ноябрь')
#     limit_nov = models.FloatField(default=0, verbose_name='Лимит - ноябрь')
#
#     fact_dec = models.FloatField(default=0, verbose_name='Факт - декабрь')
#     limit_dec = models.FloatField(default=0, verbose_name='Лимит - декабрь')
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
#
#     total = CalcManager()
#     objects = models.Manager()
#
#     def __str__(self):
#         return str(self.adress)
#
#     class Meta:
#         verbose_name = "Отопление"
#         verbose_name_plural = "Отопление"
