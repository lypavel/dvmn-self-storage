# Generated by Django 4.2.13 on 2024-06-26 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, max_length=255, verbose_name='вид')),
                ('floor', models.IntegerField(default=1, verbose_name='этаж')),
                ('volume', models.IntegerField(default=1, verbose_name='объем в м3')),
                ('sizes', models.CharField(blank=True, max_length=255, verbose_name='размеры')),
                ('price', models.IntegerField(verbose_name='цена в месяц')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='название')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(verbose_name='дата начала')),
                ('end_date', models.DateField(verbose_name='дата окончания')),
            ],
            options={
                'verbose_name': 'Аренда',
                'verbose_name_plural': 'Аренды',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='адрес')),
                ('volume', models.IntegerField(default=1, verbose_name='объем в м3')),
                ('max_boxes', models.IntegerField(default=1, verbose_name='макс кол-во товаров')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('route', models.TextField(blank=True, verbose_name='маршрут')),
                ('contacts', models.CharField(blank=True, max_length=255, verbose_name='контакты')),
                ('longitude', models.FloatField(verbose_name='долгота')),
                ('latitude', models.FloatField(verbose_name='широта')),
                ('temperature', models.FloatField(blank=True, verbose_name='температура')),
                ('ceiling_height', models.FloatField(blank=True, verbose_name='высота потолка')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storages', to='storage.city', verbose_name='город')),
            ],
            options={
                'verbose_name': 'Хранилище',
                'verbose_name_plural': 'Хранилища',
            },
        ),
        migrations.CreateModel(
            name='StorageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(db_index=True, default=1, verbose_name='порядковый номер')),
                ('image', models.ImageField(upload_to='storage', verbose_name='изображение')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='storage.storage', verbose_name='хранилище')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]