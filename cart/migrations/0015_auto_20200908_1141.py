# Generated by Django 3.0.8 on 2020-09-08 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_auto_20200908_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='days_since_order',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
