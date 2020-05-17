# Generated by Django 3.0.6 on 2020-05-16 09:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20200516_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(regex='/[$-/:-?{-~!"^_`\\[\\]]{,2}/')]),
        ),
    ]