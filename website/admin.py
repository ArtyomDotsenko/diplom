from django.contrib import admin
from .models import *


class OtoplenieAdmin(admin.ModelAdmin):
    list_display = ('adress', 'organization', 'fact', 'limit', 'created_at', 'updated_at')
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
