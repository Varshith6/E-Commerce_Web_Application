# Generated by Django 3.0.2 on 2020-05-10 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailupdates', '0002_auto_20200508_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailupdate',
            name='update_field',
            field=models.EmailField(max_length=254),
        ),
    ]
