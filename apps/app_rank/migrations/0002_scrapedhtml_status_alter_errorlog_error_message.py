# Generated by Django 4.0.7 on 2022-08-14 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_rank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapedhtml',
            name='status',
            field=models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('processed', 'Processed'), ('failed', 'Failed')], default='not_started', max_length=32),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='error_message',
            field=models.CharField(max_length=1000),
        ),
    ]