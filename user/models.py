from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, password: str = None, **kwargs) -> 'User':
        user = self.model(
            **kwargs,
            is_active=False
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, password: str = None, **kwargs) -> 'User':
        user = self.model(
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_("email address"), blank=True, unique=True)

    username = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        validators=[username_validator]
    )
    phone_number = PhoneNumberField(
        verbose_name='номер телефона'
    )
    address = models.CharField(
        verbose_name='Адрес клиента',
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )
    image = models.ImageField(
        upload_to='user',
        verbose_name='аватарка',
        null=True,
        blank=True
    )

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        if self.username:
            return self.username
        return self.email