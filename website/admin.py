from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    # filter_horizontal = ['phone']  # example: ['tlf', 'country',...]
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ('address_of_the_municipal_organization', 'fact', 'limit', 'otklonenie', 'otklonenie_percent', 'sum', 'created_at', 'updated_at', 'category')
    search_fields = ('address_of_the_municipal_organization', 'created_at')
    list_filter = ('address_of_the_municipal_organization', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class ElectrichestvoAdmin(admin.ModelAdmin):
    list_display = ('organization', 'adress', 'fact', 'limit', 'otklonenie', 'otklonenie_percent', 'created_at', 'updated_at')
    search_fields = ('adress', 'created_at')
    list_filter = ('adress', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class AdressAdmin(admin.ModelAdmin):
    list_display = ('titleOfTheAddress',)
    # readonly_fields = ('organization',)


class MainAdressAdmin(admin.ModelAdmin):
    list_display = ('titleOfTheAddressGroup',)
    # list_filter = ('organization',)


class AddressOfTheMunicipalOrganizationsAdmin(admin.ModelAdmin):
    list_display = ('municipalOrganization', 'address', 'group')

class TarifAdmin(admin.ModelAdmin):
    list_display = ('value', 'category', 'zona', 'polugodie', 'god')

admin.site.register(MunicipalOrganizations)
admin.site.register(Category)
admin.site.register(Address, AdressAdmin)
admin.site.register(Consumption, ConsumptionAdmin)
admin.site.register(AddressGroup, MainAdressAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(Zona)
admin.site.register(Month)
admin.site.register(Polugodie)
admin.site.register(God)
admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.register(User, UserAdmin)  # Register User with this inline profile
admin.site.register(AddressOfTheMunicipalOrganizations, AddressOfTheMunicipalOrganizationsAdmin)
