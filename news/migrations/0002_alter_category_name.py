# Generated by Django 3.2.8 on 2021-12-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Подписаться'),
        ),
    ]