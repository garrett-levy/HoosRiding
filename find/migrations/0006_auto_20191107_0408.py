# Generated by Django 2.2.5 on 2019-11-07 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0005_posting_posting_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='posting_id',
            field=models.CharField(max_length=200),
        ),
    ]
