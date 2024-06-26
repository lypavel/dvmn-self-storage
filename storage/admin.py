from django.contrib import admin

from storage.models import Storage, Box, StorageImage, Rent, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address')
    search_fields = ('city',)
    autocomplete_fields = ('owner',)
    list_per_page = 20


@admin.register(StorageImage)
class StorageImageAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 20


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'price')
    list_per_page = 20


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 20
