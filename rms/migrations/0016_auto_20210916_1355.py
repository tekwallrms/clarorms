# Generated by Django 3.1.1 on 2021-09-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0015_bhdata_bhinstdata_bhsitedetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bhdata',
            name='DateTime',
        ),
        migrations.RemoveField(
            model_name='bhdata',
            name='Fault',
        ),
        migrations.RemoveField(
            model_name='bhdata',
            name='RunStatus',
        ),
        migrations.AddField(
            model_name='bhinstdata',
            name='Fault',
            field=models.CharField(blank=True, choices=[('Dry Run', 'Dry Run'), ('Motor Jam', 'Motor Jam'), ('Open CKT', 'Open CKT'), ('Short CKT', 'Short CKT'), ('Over Currents', 'Over Currents'), ('Over Heat', 'Over Heat')], help_text='Name of the Fault', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bhinstdata',
            name='PumpRunHours',
            field=models.FloatField(blank=True, help_text='Gross Pump Running Hours', null=True),
        ),
        migrations.AddField(
            model_name='bhinstdata',
            name='RunStatus',
            field=models.BooleanField(default=False, help_text='Running Status'),
        ),
        migrations.AddField(
            model_name='bhsitedetails',
            name='Type',
            field=models.CharField(blank=True, choices=[('Sumersible', 'Sumersible'), ('Surface', 'Surface')], help_text='Pump Capacity in HP', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bhsitedetails',
            name='Work_Order_Date',
            field=models.DateField(blank=True, help_text='Work Order Date', null=True),
        ),
        migrations.AddField(
            model_name='bhsitedetails',
            name='Work_Order_No',
            field=models.CharField(blank=True, help_text='Work Order No', max_length=50, null=True),
        ),
    ]
