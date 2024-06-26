from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, password: str = None, **kwargs) -> 'User':
        user = self.model(**kwargs)
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
    phone_number = PhoneNumberField(
        verbose_name='номер телефона'
    )
    image = models.ImageField(
        upload_to='user',
        verbose_name='аватарка'
    )

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
