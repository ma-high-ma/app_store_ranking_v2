# Generated by Django 4.0.7 on 2022-08-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_rank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankdelta',
            name='rank_delta',
            field=models.FloatField(default=0.0),
        ),
    ]
