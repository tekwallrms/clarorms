# Generated by Django 3.1.1 on 2020-10-17 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dd',
            name='Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
