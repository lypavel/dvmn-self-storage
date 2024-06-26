# Generated by Django 4.2.13 on 2024-06-28 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0011_remove_rent_is_active_rent_is_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='promo_code',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_date',
            field=models.DateField(db_index=True, verbose_name='дата окончания'),
        ),
    ]
