# Generated by Django 3.0.8 on 2020-10-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_auto_20201006_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
