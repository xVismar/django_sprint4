# Generated by Django 3.2.16 on 2024-07-26 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240726_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации'),
        ),
    ]