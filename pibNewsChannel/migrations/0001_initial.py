# Generated by Django 4.2.8 on 2023-12-18 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YourModelName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('caption', models.TextField()),
                ('description', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('video', models.FileField(upload_to='videos/')),
            ],
        ),
    ]
