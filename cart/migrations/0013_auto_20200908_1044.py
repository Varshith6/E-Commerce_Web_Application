# Generated by Django 3.0.8 on 2020-09-08 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_auto_20200908_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]