# Generated by Django 2.2.5 on 2019-11-07 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='rides_declined',
            field=models.TextField(default='none'),
        ),
        migrations.AddField(
            model_name='rider',
            name='rides_pending',
            field=models.TextField(default='none'),
        ),
    ]