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


class RentAdminInline(admin.TabularInline):
    model = Rent
    extra = 0


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address')
    search_fields = ('city__name',)
    list_per_page = 20

    inlines = (StorageImageAdminInline,)


@admin.register(StorageImage)
class StorageImageAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 20


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'is_available',
        'volume',
        'price',
        'storage'
    )

    list_editable = ('is_available',)
    list_filter = ('is_available',)
    list_per_page = 20

    search_fields = ('number',)

    inlines = (RentAdminInline,)


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'phone_number',
        'rent_status',
        'start_date',
        'end_date',
        'promo_code'
    )
    list_filter = ('rent_status', 'end_date',)
    list_per_page = 20

    search_fields = ('promo_code', 'rent_status', 'end_date')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'created_at', 'completed_at')
    list_filter = ('status',)
    list_editable = ('status', 'completed_at')
    list_per_page = 20

    search_fields = ('email',)
