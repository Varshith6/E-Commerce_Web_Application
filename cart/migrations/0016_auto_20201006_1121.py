# Generated by Django 3.0.8 on 2020-10-06 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_auto_20200908_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, choices=[('Nighties-Regular', 'Nighties-Regular'), ('Nighties-XL', 'Nighties-XL'), ('Nighties-XXL', 'Nighties-XXL'), ('Top-S', 'Top-S'), ('Top-M', 'Top-M'), ('Top-L', 'Top-L'), ('Top-XL', 'Top-XL'), ('Top-XXL', 'Top-XXL'), ('Top-XXXL', 'Top-XXXL')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Sarees', 'Sarees'), ('Nighties', 'Nighties'), ('Dresses', 'Dresses'), ('Tops', 'Tops')], max_length=50),
        ),
    ]
