from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from pytils.translit import slugify as pytils_slugify

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='название'
    )
    slug = models.SlugField(
        blank=True,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            print(slugify(_(self.name)))
            self.slug = pytils_slugify(self.name)
        super(City, self).save(*args, **kwargs)


class Storage(BaseModel):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='владелец'
    )
    city = models.ForeignKey(
        to=City,
        on_delete=models.CASCADE,
        related_name='storages',
        verbose_name='город'
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='адрес'
    )
    volume = models.IntegerField(
        default=1,
        verbose_name='объем в м3'
    )
    max_boxes = models.IntegerField(
        default=1,
        verbose_name='макс кол-во товаров'
    )
    description = models.TextField(
        blank=True,
        verbose_name='описание'
    )
    route = models.TextField(
        blank=True,
        verbose_name='маршрут'
    )
    contacts = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='контакты'
    )
    longitude = models.FloatField(
        verbose_name='долгота'
    )
    latitude = models.FloatField(
        verbose_name='широта'
    )
    temperature = models.FloatField(
        blank=True,
        verbose_name='температура'
    )
    ceiling_height = models.FloatField(
        blank=True,
        verbose_name='высота потолка'
    )

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'

    def __str__(self):
        return self.address


class StorageImage(models.Model):
    order = models.IntegerField(
        default=1,
        verbose_name='порядковый номер',
        db_index=True
    )
    storage = models.ForeignKey(
        to=Storage,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='хранилище'
    )

    image = models.ImageField(
        upload_to='storage',
        verbose_name='изображение'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Box(BaseModel):
    type = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='вид'
    )
    storage = models.ForeignKey(
        to=Storage,
        on_delete=models.CASCADE,
        related_name='boxes',
        verbose_name='хранилище'
    )
    floor = models.IntegerField(
        default=1,
        verbose_name='этаж'
    )
    volume = models.IntegerField(
        default=1,
        verbose_name='объем в м3'
    )
    sizes = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='размеры'
    )
    price = models.IntegerField(
        verbose_name='цена в месяц'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.type


class Rent(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='rents',
        verbose_name='Клиент'
    )
    box = models.ForeignKey(
        to=Box,
        on_delete=models.CASCADE,
        related_name='rents',
        verbose_name='Товар'
    )
    start_date = models.DateField(
        verbose_name='дата начала'
    )
    end_date = models.DateField(
        verbose_name='дата окончания'
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
