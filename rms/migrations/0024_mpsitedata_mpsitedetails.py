# Generated by Django 3.1.1 on 2021-09-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0023_auto_20210924_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPSiteData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID_No', models.CharField(blank=True, help_text='Claro ID', max_length=10, null=True)),
                ('Date', models.DateField(blank=True, help_text='Date of Data', null=True)),
                ('Time', models.TimeField(blank=True, help_text='Date of Data', null=True)),
                ('Voltage', models.IntegerField(blank=True, help_text='Running PV Voltage in Volts', null=True)),
                ('Current', models.FloatField(blank=True, help_text='Running PV Current in Amps', null=True)),
                ('Power', models.FloatField(blank=True, help_text='Power in Kw', null=True)),
                ('Frequency', models.FloatField(blank=True, help_text='Running Motor Frequency in Hz', null=True)),
                ('Energy', models.FloatField(blank=True, help_text='Running Energy in Kwh', null=True)),
                ('GrossEnergy', models.FloatField(blank=True, help_text='Total Gross Energy in Kwh', null=True)),
                ('LPD', models.IntegerField(blank=True, help_text='Total Day Flow in Liters', null=True)),
                ('GrossLPD', models.IntegerField(blank=True, help_text='Total Gross Flow in Liters', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MPSiteDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID_No', models.CharField(blank=True, help_text='Claro ID', max_length=10, null=True)),
                ('VFD_Make', models.CharField(blank=True, help_text='Controller Make', max_length=50, null=True)),
                ('Pump_Make', models.CharField(blank=True, help_text='Pump Make', max_length=100, null=True)),
                ('VFD_No', models.CharField(blank=True, help_text='VFD Serial No', max_length=50, null=True)),
                ('Capacity', models.CharField(blank=True, help_text='Pump Capacity in HP', max_length=10, null=True)),
                ('Cust_Name', models.CharField(blank=True, help_text='Customer Name', max_length=50, null=True)),
                ('Cust_Mob', models.CharField(blank=True, max_length=10, null=True)),
                ('Village', models.CharField(blank=True, help_text='Village', max_length=50, null=True)),
                ('Block', models.CharField(blank=True, help_text='Block', max_length=50, null=True)),
                ('District', models.CharField(blank=True, help_text='District', max_length=50, null=True)),
                ('Date_Inst', models.DateField(blank=True, help_text='Installation Date', null=True)),
                ('D1', models.DateField(blank=True, null=True)),
                ('D2', models.DateField(blank=True, null=True)),
                ('D3', models.DateField(blank=True, null=True)),
                ('D4', models.DateField(blank=True, null=True)),
                ('D5', models.DateField(blank=True, null=True)),
                ('D6', models.DateField(blank=True, null=True)),
                ('D7', models.DateField(blank=True, null=True)),
                ('D8', models.DateField(blank=True, null=True)),
                ('D9', models.DateField(blank=True, null=True)),
                ('D10', models.DateField(blank=True, null=True)),
            ],
        ),
    ]