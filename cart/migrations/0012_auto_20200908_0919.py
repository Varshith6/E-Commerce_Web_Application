# Generated by Django 3.0.8 on 2020-09-08 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_auto_20200908_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
