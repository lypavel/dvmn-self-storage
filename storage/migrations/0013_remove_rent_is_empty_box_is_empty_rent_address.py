# Generated by Django 4.2.13 on 2024-06-29 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0012_rent_promo_code_alter_rent_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='is_empty',
        ),
        migrations.AddField(
            model_name='box',
            name='is_empty',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Пустая'),
        ),
        migrations.AddField(
            model_name='rent',
            name='address',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Адрес клиента'),
        ),
    ]