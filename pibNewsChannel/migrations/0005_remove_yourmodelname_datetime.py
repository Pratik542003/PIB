# Generated by Django 4.2.8 on 2023-12-18 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pibNewsChannel', '0004_yourmodelname_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yourmodelname',
            name='datetime',
        ),
    ]
