# Generated by Django 4.2.8 on 2023-12-18 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pibNewsChannel', '0005_remove_yourmodelname_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='yourmodelname',
            name='date',
            field=models.DateField(default='2023-01-01'),
        ),
    ]
