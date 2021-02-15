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
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


class OtoplenieAdmin(admin.ModelAdmin):
    list_display = ('adress', 'organization', 'fact', 'limit', 'otklonenie', 'otklonenie_percent', 'created_at', 'updated_at')
    search_fields = ('adress', 'created_at')
    list_filter = ('adress', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class AdressAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_adress')
    # readonly_fields = ('organization',)


class MainAdressAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)


admin.site.register(Organization)
admin.site.register(Adress, AdressAdmin)
admin.site.register(Otoplenie, OtoplenieAdmin)
admin.site.register(MainAdress, MainAdressAdmin)
admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.register(User, UserAdmin)  # Register User with this inline profile
