# Generated by Django 4.0.7 on 2022-08-09 10:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_rank', '0006_alter_keyword_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
