# Generated by Django 4.2.13 on 2024-06-30 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0016_remove_box_is_empty_box_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='owner',
        ),
    ]