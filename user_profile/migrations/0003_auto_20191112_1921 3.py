# Generated by Django 2.2.5 on 2019-11-12 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_rider_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
    ]
