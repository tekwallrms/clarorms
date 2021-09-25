from django.db import models

# Create your models here.

#Bihar Projects Models
class BHSiteDetails(models.Model):
	CID_No = models.CharField(max_length=10,null=True,blank=True, help_text='Claro ID')
	Project_Code = models.CharField(max_length=50,null=True,blank=True, help_text='Project Code')
	Work_Order_No = models.CharField(max_length=50,null=True,blank=True, help_text='Work Order No')
	Work_Order_Date = models.DateField(null=True,blank=True, help_text='Work Order Date')
	VFD_Make = models.CharField(max_length=50,null=True,blank=True, help_text='Controller Make')
	Pump_Make = models.CharField(max_length=100,null=True,blank=True, help_text='Pump Make')
	VFD_No = models.CharField(max_length=50,null=True,blank=True, help_text='VFD Serial No')
	Pump_No = models.CharField(max_length=50,null=True,blank=True, help_text='VFD Serial No')
	Capacity = models.CharField(max_length=10,null=True,blank=True, help_text='Pump Capacity in HP')
	Type = models.CharField(max_length=20,null=True,blank=True, choices = [('Submersible', 'Submersible'), ('Surface', 'Surface')], help_text='Pump Capacity in HP')
	Cust_Name = models.CharField(max_length=50,null=True,blank=True, help_text='Customer Name')
	Fath_Name = models.CharField(max_length=50,null=True,blank=True, help_text='Customer Father Name')
	Cust_Mob = models.CharField(max_length=10,null=True,blank=True)
	Village = models.CharField(max_length=50,null=True,blank=True, help_text='Village')
	Block = models.CharField(max_length=50,null=True,blank=True, help_text='Block')
	District = models.CharField(max_length=50,null=True,blank=True, help_text='District')
	State = models.CharField(max_length=50,null=True,blank=True, help_text='State')
	Date_Inst = models.DateField(null=True,blank=True, help_text='Installation Date')
	Is_Active	= models.BooleanField(default=True, help_text='Active Status')
			
	def __str__(self):   
		return self.CID_No+'-'+self.Capacity+'-'+self.Cust_Name

class BHData(models.Model):
	CID_No = models.CharField(max_length=50,null=True,blank=True, help_text='Serial No-1, 2 etc or RMS ID')
	Date = models.DateField(null=True,blank=True, help_text='Date of Data')
	LPH = models.IntegerField(null=True,blank=True, help_text='Flow Rate in LPH')
	LPD = models.IntegerField(null=True,blank=True, help_text='Total Day Flow in Liters')
	GrossLPD = models.IntegerField(null=True,blank=True, help_text='Total Gross Flow in Liters')
	Power = models.FloatField(null=True,blank=True, help_text='Power in Kw')
	Energy = models.FloatField(null=True,blank=True, help_text='Running Energy in Kwh')
	DayEnergy = models.FloatField(null=True,blank=True, help_text='Day Energy in Kwh')
	GrossEnergy = models.FloatField(null=True,blank=True, help_text='Total Gross Energy in Kwh')
	Voltage = models.IntegerField(null=True,blank=True, help_text='Running PV Voltage in Volts')
	Current = models.FloatField(null=True,blank=True, help_text='Running PV Current in Amps')
	MotorVoltage = models.IntegerField(null=True,blank=True, help_text='Running Motor Voltage in Volts')
	MotorCurrent = models.FloatField(null=True,blank=True, help_text='Running Motor Current in Amps')
	Frequency = models.FloatField(null=True,blank=True, help_text='Running Motor Frequency in Hz')
	Temp = models.FloatField(null=True,blank=True, help_text='Temperature in Degree Cent')
	PumpRunHours = models.FloatField(null=True,blank=True, help_text='Pump Running Hours')

	def __str__(self):   
		return self.CID_No+'-'+str(self.Date)+'-'+str(self.LPD)

class BHInstData(models.Model):
	faultchoice = [('Dry Run', 'Dry Run'), ('Motor Jam', 'Motor Jam'), ('Open CKT', 'Open CKT'), ('Short CKT', 'Short CKT'), ('Over Currents', 'Over Currents'), ('Over Heat', 'Over Heat')]
	CID_No = models.CharField(max_length=10,null=True,blank=True, help_text='Claro ID')
	Date = models.DateField(null=True,blank=True, help_text='Date of Data')
	Time = models.TimeField(null=True,blank=True, help_text='Date of Data')
	Voltage = models.IntegerField(null=True,blank=True, help_text='Running PV Voltage in Volts')
	Current = models.FloatField(null=True,blank=True, help_text='Running PV Current in Amps')
	Power = models.FloatField(null=True,blank=True, help_text='Power in Kw')
	Frequency = models.FloatField(null=True,blank=True, help_text='Running Motor Frequency in Hz')
	Energy = models.FloatField(null=True,blank=True, help_text='Running Energy in Kwh')
	GrossEnergy = models.FloatField(null=True,blank=True, help_text='Total Gross Energy in Kwh')
	LPD = models.IntegerField(null=True,blank=True, help_text='Total Day Flow in Liters')
	GrossLPD = models.IntegerField(null=True,blank=True, help_text='Total Gross Flow in Liters')
	PumpRunHours = models.FloatField(null=True,blank=True, help_text='Gross Pump Running Hours')
	Fault = models.CharField(max_length=50,null=True,blank=True, choices=faultchoice, help_text='Name of the Fault')
	RunStatus = models.BooleanField(default=False, help_text='Running Status')

	def __str__(self):   
		return self.CID_No+'-'+str(self.Date)+'-'+str(self.Time)

class DBData(models.Model):
	"""docstring for ClassName"""
	Date = models.DateField(null=True,blank=True, help_text='Date of Last Updte')
	CID_No = models.CharField(max_length=50,null=True,blank=True, help_text='Serial No-1, 2 etc or RMS ID')
	GrossLPD = models.IntegerField(null=True,blank=True, help_text='Total Gross Flow in Liters')
	GrossEnergy = models.IntegerField(null=True,blank=True, help_text='Total Gross Energy in Kwh')
	PumpRunHours = models.IntegerField(null=True,blank=True, help_text='Pump Running Hours')
	Faults = models.IntegerField(null=True,blank=True, help_text='Total Faults')

	def __str__(self):   
		return self.CID_No+'-'+str(self.GrossEnergy)

class BHdb(models.Model):
	"""docstring for ClassName"""
	Date = models.DateField(null=True,blank=True, help_text='Date of Data')
	Count = models.IntegerField(null=True,blank=True, help_text='Total Under Warranty Systems')
	GrossLPD = models.IntegerField(null=True,blank=True, help_text='Total Gross Flow in Liters')
	GrossEnergy = models.IntegerField(null=True,blank=True, help_text='Total Gross Energy in Kwh')
	PumpRunHours = models.IntegerField(null=True,blank=True, help_text='Pump Running Hours')
	Faults = models.IntegerField(null=True,blank=True, help_text='Total Faults')

	def __str__(self):   
		return str(self.Date)+'-'+str(self.GrossEnergy)


class homeid(models.Model):
	"""docstring for ClassName"""
	CID_No = models.CharField(max_length=40,null=True,blank=True)
	Date = models.DateField(null=True,blank=True, help_text='Date of Data')
	Status = models.IntegerField(null=True,blank=True)
	sTime =  models.IntegerField(null=True,blank=True)
	eTime =  models.IntegerField(null=True,blank=True)
	dtm = models.IntegerField(null=True,blank=True)
	step = models.IntegerField(null=True,blank=True)

	def __str__(self):   
		return self.CID_No

#MP Project Models

class MPSiteDetails(models.Model):
	CID_No = models.CharField(max_length=10,null=True,blank=True, help_text='Claro ID')
	VFD_Make = models.CharField(max_length=50,null=True,blank=True, help_text='Controller Make')
	Pump_Make = models.CharField(max_length=100,null=True,blank=True, help_text='Pump Make')
	VFD_No = models.CharField(max_length=50,null=True,blank=True, help_text='VFD Serial No')
	Capacity = models.CharField(max_length=10,null=True,blank=True, help_text='Pump Capacity in HP')
	Cust_Name = models.CharField(max_length=50,null=True,blank=True, help_text='Customer Name')
	Cust_Mob = models.CharField(max_length=10,null=True,blank=True)
	Village = models.CharField(max_length=50,null=True,blank=True, help_text='Village')
	Block = models.CharField(max_length=50,null=True,blank=True, help_text='Block')
	District = models.CharField(max_length=50,null=True,blank=True, help_text='District')
	Date_Inst = models.DateField(null=True,blank=True, help_text='Installation Date')
	D1 = models.DateField(null=True,blank=True)
	D2 = models.DateField(null=True,blank=True)
	D3 = models.DateField(null=True,blank=True)
	D4 = models.DateField(null=True,blank=True)
	D5 = models.DateField(null=True,blank=True)
	D6 = models.DateField(null=True,blank=True)
	D7 = models.DateField(null=True,blank=True)
	D8 = models.DateField(null=True,blank=True)
	D9 = models.DateField(null=True,blank=True)
	D10 = models.DateField(null=True,blank=True)		
	
	def __str__(self):   
		return self.CID_No+'-'+self.Capacity+'-'+self.Cust_Name

class MPSiteData(models.Model):
	CID_No = models.CharField(max_length=10,null=True,blank=True, help_text='Claro ID')
	Date = models.DateField(null=True,blank=True, help_text='Date of Data')
	Time = models.TimeField(null=True,blank=True, help_text='Date of Data')
	Voltage = models.IntegerField(null=True,blank=True, help_text='Running PV Voltage in Volts')
	Current = models.FloatField(null=True,blank=True, help_text='Running PV Current in Amps')
	Power = models.FloatField(null=True,blank=True, help_text='Power in Kw')
	Frequency = models.FloatField(null=True,blank=True, help_text='Running Motor Frequency in Hz')
	Energy = models.FloatField(null=True,blank=True, help_text='Running Energy in Kwh')
	GrossEnergy = models.FloatField(null=True,blank=True, help_text='Total Gross Energy in Kwh')
	LPD = models.IntegerField(null=True,blank=True, help_text='Total Day Flow in Liters')
	GrossLPD = models.IntegerField(null=True,blank=True, help_text='Total Gross Flow in Liters')

	def __str__(self):   
		return self.CID_No+'-'+str(self.Date)+'-'+str(self.Time)


class meta:   #for admin database actions
	verbose_name = 'BHSiteDetails'
	erbose_name_plural = 'BHSiteDetails'

class meta:   #for admin database actions
	verbose_name = 'BHData'
	erbose_name_plural = 'BHData'

class meta:   #for admin database actions
	verbose_name = 'BHInstData'
	erbose_name_plural = 'BHInstData'

class meta:   #for admin database actions
	verbose_name = 'DBData'
	erbose_name_plural = 'DBData'

class meta:   #for admin database actions
	verbose_name = 'homeid'
	erbose_name_plural = 'homeid'

class meta:   #for admin database actions
	verbose_name = 'BHdb'
	erbose_name_plural = 'BHdb'

class meta:   #for admin database actions
	verbose_name = 'MPSiteDetails'
	erbose_name_plural = 'MPSiteDetails'

class meta:   #for admin database actions
	verbose_name = ' MPSiteData'
	erbose_name_plural = ' MPSiteData'















	#def __init__(self, arg):
	#	super(ClassName, self).__init__()
	#	self.arg = arg

