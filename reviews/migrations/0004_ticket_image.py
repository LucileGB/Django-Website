# Generated by Django 3.1.1 on 2021-09-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20210913_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
