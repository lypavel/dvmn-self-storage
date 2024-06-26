# Generated by Django 4.2.13 on 2024-06-26 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0003_city_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='owner',
        ),
        migrations.AddField(
            model_name='box',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='box',
            name='type',
            field=models.CharField(blank=True, choices=[('3', 'До 3м²'), ('10', 'До 10м²'), ('10+', 'От 10м²')], max_length=255, verbose_name='тип'),
        ),
        migrations.AlterField(
            model_name='box',
            name='volume',
            field=models.IntegerField(default=1, verbose_name='объем в м³'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='box',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='storage.box', verbose_name='Ячейка'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='max_boxes',
            field=models.IntegerField(default=1, verbose_name='макс кол-во ячеек'),
        ),
    ]
