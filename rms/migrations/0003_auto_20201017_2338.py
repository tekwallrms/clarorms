# Generated by Django 3.1.1 on 2020-10-17 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0002_auto_20201017_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dd',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]