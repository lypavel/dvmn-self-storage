from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'image')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'phone_number',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
