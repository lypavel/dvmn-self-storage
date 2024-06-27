from django.contrib import admin
from django.utils.html import mark_safe

from storage.models import Storage, Box, StorageImage, Rent, City, Consultation


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StorageImageAdminInline(admin.TabularInline):
    model = StorageImage
    extra = 3

    readonly_fields = ('image_view',)

    def image_view(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return 'Загрузите картинку'

    image_view.short_description = 'Картинка'


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


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('email', 'status')
    list_per_page = 20
