from django.contrib import admin

from storage.models import Storage, Box, StorageImage, Rent, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StorageImageAdminInline(admin.TabularInline):
    model = StorageImage
    extra = 3


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address')
    search_fields = ('city',)
    list_per_page = 20

    inlines = (StorageImageAdminInline,)


@admin.register(StorageImage)
class StorageImageAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 20


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'price')
    autocomplete_fields = ('owner',)
    list_per_page = 20


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 20
