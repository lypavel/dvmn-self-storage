# Generated by Django 4.2.13 on 2024-07-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0018_alter_city_name_alter_rent_rent_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='password',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Пароль'),
        ),
    ]
