# Generated by Django 4.0.2 on 2023-11-18 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texeclientapp', '0007_user_registration_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_registration',
            name='joindate',
            field=models.DateField(default=datetime.date(2023, 11, 18), null=True),
        ),
    ]
