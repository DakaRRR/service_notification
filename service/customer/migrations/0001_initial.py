# Generated by Django 4.1.3 on 2022-12-01 13:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)', regex='^7\\d{10}$')])),
                ('mobile_operator', models.CharField(max_length=5)),
                ('tag', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
        ),
    ]
