# Generated by Django 2.2.5 on 2019-12-01 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_auto_20191201_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='cellphone',
            field=models.CharField(max_length=10),
        ),
    ]