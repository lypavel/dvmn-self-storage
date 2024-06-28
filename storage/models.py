from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Min, Q
from django.utils import timezone
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


class StorageQuerySet(models.QuerySet):
    def annotate_min_price(self):
        return self.annotate(min_price=Min('boxes__price'))

    def annotate_boxes_available(self):
        return self.annotate(
            boxes_available=Count(
                'boxes', filter=Q(boxes__owner=None)
            )
        )


class Storage(BaseModel):
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
    max_boxes = models.IntegerField(
        default=1,
        verbose_name='макс кол-во ячеек'
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
    feature = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='особенность'
    )

    objects = StorageQuerySet.as_manager()

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
    class BoxType(models.TextChoices):
        below_3_meters = ('3', 'До 3м²')
        below_10_meters = ('10', 'До 10м²')
        above_10_meters = ('10+', 'От 10м²')

    type = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='тип',
        choices=BoxType.choices
    )
    number = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='номер'
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
        verbose_name='объем в м³'
    )
    sizes = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='размеры'
    )
    price = models.IntegerField(
        verbose_name='цена в месяц'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='владелец',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'

    def __str__(self):
        return self.number


class Rent(BaseModel):
    class PaymentStatus(models.TextChoices):
        paid = ('paid', 'Оплачено')
        not_paid = ('not_paid', 'Не оплачено')

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
        verbose_name='Ячейка'
    )
    start_date = models.DateField(
        verbose_name='дата начала'
    )
    end_date = models.DateField(
        verbose_name='дата окончания'
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    payment_status = models.CharField(
        verbose_name='Статус оплаты',
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.not_paid,
        db_index=True
    )
    is_empty = models.BooleanField(
        verbose_name='Пустая',
        db_index=True,
        default=True
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'


class Consultation(models.Model):
    class ConsultationStatus(models.TextChoices):
        new = ('new', 'Новая')
        completed = ('completed', 'Обработана')

    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        db_index=True
    )
    status = models.CharField(
        max_length=255,
        verbose_name='статус',
        choices=ConsultationStatus.choices,
        default=ConsultationStatus.new,
        db_index=True
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        default=timezone.now
    )
    completed_at = models.DateTimeField(
        verbose_name='дата обработки',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'заказ консультации'
        verbose_name_plural = 'заказы консультаций'

    def __str__(self):
        return self.email
