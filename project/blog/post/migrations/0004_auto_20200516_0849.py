# Generated by Django 3.0.6 on 2020-05-16 08:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_number_of_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='number_of_comments',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50)]),
        ),
    ]
