# Generated by Django 4.0.7 on 2022-08-09 10:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_rank', '0005_alter_keyword_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 9, 10, 55, 21, 753626, tzinfo=utc)),
        ),
    ]
