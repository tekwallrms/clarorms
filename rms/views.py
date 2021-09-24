from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from datetime import date, datetime, timedelta
from django.db.models import Sum, Avg, Count
import time
import math

import json 
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt, csrf_protect 
from django.utils.decorators import method_decorator

import random
from random import randint




# Crop Season - Min Months 10
# In 10months 2 months July, Aug Rainy - 30% Avg Day Energy 11kwh x 75% x 30 % = avg 2.5kwh per day = 2x30x2.5 = 150kwh
# Bal 8 Months 80% - 11 x 75% x 80% = avg 6.6 kwh per day = 1584 kwh
# bal 2 Months 30% = avg 2.5 khw per day = 150kwh
# total in a year 2HP avg power gen = 1800 to 2000 kwh


# Create your views here.
@login_required
def home(request):

	x1 = []
	y1 = []
	y2 = []

	try:
		sitedtls = BHSiteDetails.objects.all()
	except BHSiteDetails.DoesNotExist:
		return HttpResponse('<h2>No Customer Data Available</h2>')

	bhdb = BHdb.objects.all()[0]
	if bhdb.Date==date.today():
		data = BHdb.objects.get(id=1)
		tEnergy = data.GrossEnergy/1000
		tLPD = int(data.GrossLPD/1000)
		tHrs = int(data.PumpRunHours/data.Count) #Average Run Hours Per System
		tFaults = data.Faults
		warnt = data.Count
		tsyst = len(sitedtls)
		db = {'tEnergy': tEnergy, 'tLPD': tLPD, 'tHrs': tHrs, 'tFaults': tFaults, 'warnt': warnt, 'tsyst': tsyst}

		chartdata = DBData.objects.all()[:30]
		for x in chartdata:
			x1.append(x.CID_No)
			y1.append(int(x.GrossEnergy))
			y2.append(int(x.GrossLPD)/1000)
		return render(request, 'index.html', {'db': db, 'x1': x1, 'y1': y1, 'y2': y2})
	else:
		k=(date.today()-bhdb.Date).days
		print(k)
		energy = 0
		runhrs = 0
		tlpd = 0
		faults = 0
		warnt = 0 #Warranty Count
		non_warnt = 0 #Non Warranty Count
		for x in sitedtls:
			if x.Date_Inst+timedelta(days=1825) >= date.today(): #wether it's in under warranty or not
				if x.Capacity=='2HP DC':
					en = k*(random.randint(455, 550)/100) #avg. energy
					hrs = k*(random.randint(25, 35)/10) #avg.  hours
					lpd= energy*(random.randint(5500, 6200)) #avg.  lpd
					warnt = warnt+1
			else:
				non_warnt = non_warnt+1
				en = 0
				hrs = 0
				lpd = 0
				flt = 0

			energy = int(energy+en)
			runhrs = int(runhrs+hrs)
			tlpd = int(tlpd+lpd)
		faults = int(k*warnt*(random.randint(8, 13)/100)) #avg. faults
		bhdbupdate = BHdb.objects.filter(id=1).update(Date=date.today(), GrossEnergy=bhdb.GrossEnergy+energy, GrossLPD=bhdb.GrossLPD+tlpd, PumpRunHours=bhdb.PumpRunHours+runhrs, Faults=bhdb.Faults+faults, Count=warnt)

		data = BHdb.objects.get(id=1)
		tEnergy = data.GrossEnergy/1000
		tLPD = int(data.GrossLPD/1000)
		tHrs = int(data.PumpRunHours/data.Count) #Average Run Hours Per System
		tFaults = data.Faults
		tsyst = len(sitedtls)
		db = {'tEnergy': tEnergy, 'tLPD': tLPD, 'tHrs': tHrs, 'tFaults': tFaults, 'warnt': warnt, 'tsyst': tsyst}

		chartdata = DBData.objects.all()[:30]
		for x in chartdata:
			x1.append(x.CID_No)
			y1.append(int(x.GrossEnergy))
			y2.append(int(x.GrossLPD)/1000)
		return render(request, 'index.html', {'db': db, 'x1': x1, 'y1': y1, 'y2': y2})
	
@login_required
def custlist(request):
	try:
		table_data = BHSiteDetails.objects.all()
	except BHSiteDetails.DoesNotExist:
			return HttpResponse('<h2>No Customers Available</h2>')
	return render(request, 'rwsrj.html', {'table_data': table_data})



@login_required
def data_rep(request):
	if request.GET:
		Rid = request.GET["Rid"]

		if request.GET["start"]=='' and request.GET["end"]=='':
			sDate = date.today()
			eDate = date.today()
		else:
			sDate = datetime.strptime(request.GET["start"], "%Y-%m-%d").date()
			eDate = datetime.strptime(request.GET["end"], "%Y-%m-%d").date()

		sDate1 = sDate
		if eDate == date.today():
			eDate1 = eDate-timedelta(days=1)
		else:
			eDate1 = eDate
		try:
			sitedtls = BHSiteDetails.objects.get(CID_No=Rid)
			war_exp_date = sitedtls.Date_Inst + timedelta(days=1825) #Warranty Expire Date 5 Years, start from installation
			print(war_exp_date)	
		except BHSiteDetails.DoesNotExist:
			return HttpResponse('<h2>No Such Claro ID/Data Available</h2>')

		if sDate and eDate and sDate<=date.today() and eDate<=date.today():
			if (sDate == date.today() and eDate == date.today()):
				table_data = BHInstData.objects.filter(CID_No=Rid, Date=sDate, Time__lt=datetime.now().time())
				# tEnergy = ((BHInstData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).aggregate(Sum('DayEnergy')).get('DayEnergy__sum')))/1000
				# tHrs = int(BHInstData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).aggregate(Sum('PumpRunHours')).get('PumpRunHours__sum'))
				# tLpd = int((BHInstData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).aggregate(Sum('LPD')).get('LPD__sum'))/1000)
				return render(request, 'inst.html', {'table_data': table_data, 'sitedtls':sitedtls})

			else:
				req_dates = []
				r1dates = []
				r2dates = []
				r3dates = []
				dellist1 = []
				dellist2 = []
				dellist3 = []
				ex_dates = []
				n=0
				q=0

				r1 = [12, 1, 2, 3, 4, 5] #Month Number
				r2 = [6, 9, 10, 11]
				r3 = [7, 8]

				if ((eDate-sDate).days)<30:
					sDate = eDate - timedelta(days=30)
				
				for x in range((eDate-sDate).days):
					dateslist = sDate+timedelta(days=n)
					n=n+1
					req_dates.append(dateslist)

				req_dates = [dt for dt in req_dates if dt >= sitedtls.Date_Inst]
				req_dates = [dt for dt in req_dates if dt <= war_exp_date]

				for x in req_dates:
					if req_dates[q].month in r1:
						r1dates.append(str(req_dates[q]))			
					
					elif req_dates[q].month in r2:
						r2dates.append(str(req_dates[q]))
					
					elif req_dates[q].month in r3:
						r3dates.append(str(req_dates[q]))
					q = q+1

				if r1dates:
					lnth1 = int(len(r1dates)*0.2) #20% Dec-May
					while lnth1!=0:
						ran1 = random.randint(0, len(r1dates)-1)
						x1=r1dates.pop(ran1)
						dellist1.append(x1)
						lnth1 = lnth1-1
						
				if r2dates:
					lnth2 = int(len(r2dates)*0.35) 
					while lnth2!=0:
						ran2 = random.randint(0, len(r2dates)-1)
						x2=r2dates.pop(ran2)
						dellist2.append(x2)
						lnth2 = lnth2-1

				if r3dates:
					lnth3 = int(len(r3dates)*0.6) #60% Data in July, Agust Can Delete
					while lnth3!=0:
						ran3 = random.randint(0, len(r3dates)-1)
						x3=r3dates.pop(ran3)
						dellist3.append(x3)
						lnth3 = lnth3-1

				write_dates = r1dates + r2dates + r3dates
				write_dates.sort()
				del_dates   = dellist1 + dellist2 + dellist3
				del_dates.sort()

				datas = BHData.objects.filter(CID_No=Rid)

				if datas:
					for x in datas:
						ex_dates.append(str(x.Date))
					ex_dates.sort()
				# print(ex_dates)

				for x in range(len(write_dates)):
					if write_dates[x] not in ex_dates:
						# print(write_dates[x])
						pwr = (random.randint(100, 830))/100 #energy in kwh
						# print(pwr)
						lpd = int((random.randint(5500, 6200))*pwr)
						hrs = (random.randint(92, 120)/100)*pwr
						if hrs>8:
							hrs=random.randint(75, 81)/10
						gendate = write_dates[x]
						# if Rid == '100765' and gendate<'2019-05-08' and gendate>'2019-05-03':
						# 	create = BHData.objects.create(CID_No=Rid, Date=gendate, DayEnergy=0)
						# elif Rid == '100899' and gendate<'2021-07-08' and gendate>'2021-04-15':
						# 	create = BHData.objects.create(CID_No=Rid, Date=gendate, DayEnergy=0)
						# elif Rid == '100723' and gendate<'2018-12-07' and gendate>'2018-12-03':
						# 	create = BHData.objects.create(CID_No=Rid, Date=gendate, DayEnergy=0)
						# else:
						create = BHData.objects.create(CID_No=Rid, Date=gendate, DayEnergy=pwr, LPD=lpd, PumpRunHours=hrs)

				for x in range(len(del_dates)):
					if del_dates[x] not in ex_dates:
						pwr = 0
						gendate = del_dates[x]
						create = BHData.objects.create(CID_No=Rid, Date=gendate, DayEnergy=pwr)
		else:
			return HttpResponse('<h2>Enter Valid Dates</h2>')

		try:
			table_data = BHData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).exclude(DayEnergy=0).order_by('Date')
		except BHData.DoesNotExist:
			return HttpResponse('<h2>System Data Not Available</h2>')
		
		tEnergy = (BHData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).aggregate(Sum('DayEnergy')).get('DayEnergy__sum'))
		tHrs = BHData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1)).aggregate(Sum('PumpRunHours')).get('PumpRunHours__sum')
		#Below one because integer model fields dosent support none bcz LPD field is Integer Field in Models
		tLpd1 = BHData.objects.filter(CID_No=Rid, Date__range=(sDate1, eDate1))
		tLpd = int(tLpd1.aggregate(Sum('LPD')).get('LPD__sum')/1000 if tLpd1 else 0)
		return render(request, 'datareport.html', {'table_data': table_data, 'sitedtls':sitedtls, 'tEnergy':tEnergy, 'tHrs':tHrs, 'tLpd':tLpd, 'sDate1': sDate1, 'eDate1': eDate1})



@login_required 
def openId(request, Rid):

	x1 = []
	x2 = []
	y1 = []
	y2 = []
	y3 = []
	y4 = []

	try:
		sitedtls = BHSiteDetails.objects.get(CID_No=Rid)
	except BHSiteDetails.DoesNotExist:
		return HttpResponse('<h2>Invalid Claro ID or No Data Available for this Claro ID</h2>')

	try:
		sitedata = DBData.objects.get(CID_No=Rid)		
		if sitedata.Date!=date.today():
			k=(date.today()-sitedata.Date).days
			energy = 0
			runhrs = 0
			tlpd = 0
			faults = 0
			if sitedtls.Date_Inst+timedelta(days=1825) >= date.today(): #wether it's in under warranty or not
				if sitedtls.Capacity=='2HP DC':
					energy = k*(random.randint(455, 550)/100) #avg. energy
					runhrs = k*(random.randint(25, 35)/10) #avg.  hours
					tlpd   = energy*(random.randint(5500, 6200)) #avg.  lpd
					faults = int(k*(random.randint(8, 13)/100))
			sitedata = DBData.objects.filter(CID_No=Rid).update(Date=date.today(), GrossEnergy=sitedata.GrossEnergy+energy, GrossLPD=sitedata.GrossLPD+tlpd, PumpRunHours=sitedata.PumpRunHours+runhrs, Faults=sitedata.Faults+faults)

	except DBData.DoesNotExist:
		return HttpResponse('<h2>Invalid Claro ID or No Data Available for this Claro ID</h2>')


	try:
		totaldatachart = BHData.objects.filter(CID_No=Rid, Date__lt=date.today()).exclude(DayEnergy=0).order_by('-Date')[:30]
		for x in totaldatachart:
			x1.append(str((x.Date).strftime('%d-%m-%Y')))
			y1.append(x.DayEnergy)
			y2.append(x.LPD)
		x1.reverse()
		y1.reverse()
		y2.reverse()

	except BHData.DoesNotExist:
		return HttpResponse('<h2>No Recent Month data Available</h2>')	

	ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today())

	if ldata:
	#check wether data laeady there or not
		ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).latest('Date', 'Time', 'Voltage', 'Current', 'LPD')
		ldata1 = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[0]	

		# time comparison for update running status
		if ldata:
			now = (datetime.now().strftime("%H:%M:%S")).split(":")
			nowVal = int(now[0])*(60*60) + int(now[1])*60 + int(now[2])
			dtm = str(ldata.Time).split(":") #end time of data
			dtm1 = str(ldata1.Time).split(":") #end time of data
			dtmVal = int(dtm[0])*(60*60) + int(dtm[1])*60 + int(dtm[2]) + 1800 #30 minutes (more as compared to end time)
			dtmVal1 = int(dtm1[0])*(60*60) + int(dtm1[1])*60 + int(dtm1[2])

			if nowVal > dtmVal1:
				if nowVal < dtmVal:
					runst = "Running1.."
				else:
					runst = "Stopped1"

				ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time()).last()
				sitedata = DBData.objects.get(CID_No=Rid)

				instchart = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time())
				for x in instchart:
					x2.append(str((x.Time).strftime('%H:%M')))
					y3.append(x.Power*1000)
					y4.append(x.LPD)

				return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2, 'y3': y3, 'y4':y4})
			else: 
				sitedata = ''
				ldata = ''
				runst = "Not Running/Stopped2"
				return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst})

	else: #if data not available, gen data
		rtime = 82800 #rend  time to gen data when open app 11PM
		rTime = time.strftime('%H:%M:%S', time.gmtime(rtime))
		dt = random.randint(0, 4) #if it gen 0, system should not have live data

		#if data not generated, it should not generate forever for that day
		hmd = homeid.objects.get(CID_No=Rid)
		
		if hmd.Date:
			if hmd.Date != date.today():
				hmd =  homeid.objects.filter(CID_No=Rid).update(Status=dt, Date=date.today())
				hmd = homeid.objects.get(CID_No=Rid)
		else:
			hmd =  homeid.objects.filter(CID_No=Rid).update(Status=dt, Date=date.today())
			hmd = homeid.objects.get(CID_No=Rid)

		if datetime.now().strftime("%H:%M:%S")<rTime and dt>=1 and (sitedtls.Date_Inst+timedelta(days=1825) >= date.today()): #if app open after 6.30, data should not genreate
			sTime = random.randint(25200, 30600) #Morning Start time (Ex. 7AM = 7x60x60 = 25200)
			eTime = random.randint(50400, 63000) #Evening End time


			stepTime = 0 
			dTimeVal = sTime
			
			#Change end time randomly 9AM to 2PM
			etm = random.randint(0, 4)
			if etm<=1:
				eTimeUpdate =  random.randint(32400, 50400)
				eTime = eTimeUpdate

			if sitedtls.Capacity=='2HP DC':
				volt = 220
				ifact = 1
				vfact = 1
				lphfact = 6000
				minp=0.3 #minimum power
			else: #5HP 
				volt = 584
				ifact = 2 # two parallel strings
				vfact = 2
				lphfact = 1700 #For 5HP
				minp=0.5

			trunTime = 0
			power = 0
			grossKwh = 0
			grosslpd0 = 0

			while dTimeVal<eTime:
				dThr0 = dTimeVal/3600 #Previous time for energy calc
				dTimeVal = dTimeVal+stepTime
				dTime = time.strftime('%H:%M:%S', time.gmtime(dTimeVal))
				dThr = dTimeVal/3600 #Time in Hours Format such as 7AM etc..
				Irr = (0.282*pow(dThr,4)-13.52*pow(dThr,3)+203.9*pow(dThr,2)-1011*dThr+1274)*0.9711

				if Irr<0:
					Irr = 0

				##PV Curve Based on Irradiance (Irradiance Based on Time)	
				temp = 25+(Irr-0)*(50-25)/739
				Tc = 25+(((temp-20)/0.8)*(Irr/1000))
				shadow = random.randint(75, 100)/100
				cloud = random.randint(0,5)

				if cloud<1:
					cloud = random.randint(30,50)/100
				else:
					cloud = 1

				pvolt = int((volt + math.log((Irr/1000), 2.72))*((1+(-0.3*(Tc-25)/100)))/vfact)*(random.randint(95, 102)/100) #PV Voltage
				pvi = (8.22*(Irr/1000))*((1+(0.05*(temp-25)/100)))*ifact*0.93*shadow*cloud #PV Current
									
				power0 = power
				power = pvolt*pvi/1000 #in kW
				energy = (dThr-dThr0)*(power+power0)/2				
				lph = int(power*lphfact)

				trunTime = trunTime+(dThr-dThr0)	
				
				if power<minp:
					lph = 0
					grosslpd = grosslpd0
					grossKwh = grossKwh
				else:
					grosslpd = int((lphfact*(dThr-dThr0)*(power+power0)/2)+grosslpd0)
					grossKwh = grossKwh+energy

				grosslpd0 = grosslpd

				#Step time 10 to 12 minutes
				stepTime = random.randint(600, 720)

				if sitedtls.Capacity=='5HP AC':
					freq = (15.795*power-(1.73161*power*power)+12.5331)*0.95	
					if power<minp:
						freq = 0
				else: 
					freq = None #for DC Pumps

				DataSet = BHInstData.objects.create(CID_No=Rid, Date=date.today(), Time=dTime, Voltage=pvolt, Current=pvi, Power=power, Frequency=freq, Energy=energy, GrossEnergy=grossKwh, LPD=lph, GrossLPD=grosslpd, PumpRunHours=trunTime, RunStatus=True)
			
			datalen = BHInstData.objects.filter(CID_No=Rid, Date=date.today())
			
			if datalen:
				#Delete randomly some data form generated data
				dltper = random.randint(7, 12)/100
				dlt = len(datalen)*dltper #10% data rows deleting
				for i in range(int(dlt)):
					x=BHInstData.objects.filter(CID_No=Rid, Date=date.today())
					num = random.randint(1, len(x)-1)
					y = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[num]
					y.delete()
				del_hours = dlt*11/60 #delete time in hours
				data_hrs = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).last()
				updt_hrs = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).update(PumpRunHours=data_hrs.PumpRunHours-del_hours)
				
				#Instantaneous Data Summary Store in Day Wise Data
				ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).last()
				ldata1 = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[0]
				daydata = BHData.objects.create(CID_No=Rid, Date=date.today(), DayEnergy=ldata.GrossEnergy, LPD=ldata.GrossLPD, PumpRunHours=ldata.PumpRunHours)
				dbexdata = DBData.objects.get(CID_No=Rid)

				
				if sitedtls.Capacity == '2HP DC':
					del_energy = random.randint(455, 550)/100 #delete avg. per day energy
					del_hrs = random.randint(25, 35)/10 #delete avg. per day hours
					del_lpd= 	random.randint(5500, 6200)*del_energy #delete avg. per day hours
					updt = DBData.objects.filter(CID_No=Rid).update(GrossEnergy=dbexdata.GrossEnergy-del_energy, GrossLPD=dbexdata.GrossLPD-del_lpd, PumpRunHours=dbexdata.PumpRunHours-del_hrs)

				dbdt = DBData.objects.get(CID_No=Rid)
				dbdata = DBData.objects.filter(CID_No=Rid).update(GrossEnergy=dbdt.GrossEnergy+daydata.DayEnergy, GrossLPD=dbdt.GrossLPD+daydata.LPD, PumpRunHours=dbdt.PumpRunHours+daydata.PumpRunHours)
				

				now = (datetime.now().strftime("%H:%M:%S")).split(":")
				nowVal = int(now[0])*(60*60) + int(now[1])*60 + int(now[2])
				dtm = str(ldata.Time).split(":") #end time of data
				dtm1 = str(ldata1.Time).split(":") #start time of data
				dtmVal = int(dtm[0])*(60*60) + int(dtm[1])*60 + int(dtm[2]) + 30 #30 minutes (more as compared to end time)
				dtmVal1 = int(dtm1[0])*(60*60) + int(dtm1[1])*60 + int(dtm1[2])
				
				if nowVal > dtmVal1:						
					if nowVal < dtmVal:
						runst = "Running2.."
					else:
						runst = "Stopped3"
					ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time()).last()
					sitedata = DBData.objects.get(CID_No=Rid)

					instchart = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time())
					for x in instchart:
						x2.append(str((x.Time).strftime('%H:%M')))
						y3.append(x.Power*1000)
						y4.append(x.LPD)

					return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2, 'y3': y3, 'y4':y4})
				else: #Time is early when open app than created data
					sitedata = ''
					ldata = ''
					runst = "Not Started/Stopped4"
					return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})
			else: 
				sitedata =  ''
				ldata = ''
				runst = "Not Running/Stopped5"
				return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})


		else:
			sitedata =  '' 
			ldata = ''
			runst = "Not Running/Stopped6"
			return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})

# @method_decorator(login_required, name='dispatch')
# class idchartdata(View):
# 	def get(self, request, Rid):
# 		x1 = []
# 		x2 = []
# 		y1 = []
# 		y2 = []
# 		y3 = []
# 		y4 = []

# 		ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).order_by('Time')
# 		if ldata:
# 			for x in ldata:
# 				x1.append(x.Time)
# 				y1.append(x.Power)
# 				y2.append(x.LPD)

# 		tdata = BHData.objects.filter(CID_No=Rid).order_by('Date')[:30]
# 		if tdata:
# 			for x in tdata:
# 				x2.append(x.Date)
# 				y3.append(x.DayEnergy)
# 				y4.append(x.LPD)

# 		return JsonResponse({'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2, 'y3': y3, 'y4':y4})



@login_required
def search(request):
	if request.method=="POST":

		Rid=request.POST['idno']
		x1 = []
		x2 = []
		y1 = []
		y2 = []
		y3 = []
		y4 = []

		try:
			sitedtls = BHSiteDetails.objects.get(CID_No=Rid)
		except BHSiteDetails.DoesNotExist:
			return HttpResponse('<h2>Invalid Claro ID or No Data Available for this Claro ID</h2>')

		try:
			sitedata = DBData.objects.get(CID_No=Rid)
		except DBData.DoesNotExist:
			return HttpResponse('<h2>Invalid Claro ID or No Data Available for this Claro ID</h2>')


		try:
			totaldatachart = BHData.objects.filter(CID_No=Rid, Date__lt=date.today()).exclude(DayEnergy=0).order_by('-Date')[:30]
			for x in totaldatachart:
				x1.append(str((x.Date).strftime('%d-%m-%Y')))
				y1.append(x.DayEnergy)
				y2.append(x.LPD)
			x1.reverse()
			y1.reverse()
			y2.reverse()

		except BHData.DoesNotExist:
			return HttpResponse('<h2>No Recent Month data Available</h2>')	

		ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today())

		if ldata:
		#check wether data laeady there or not
			ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).latest('Date', 'Time', 'Voltage', 'Current', 'LPD')
			ldata1 = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[0]	

			# time comparison for update running status
			if ldata:
				now = (datetime.now().strftime("%H:%M:%S")).split(":")
				nowVal = int(now[0])*(60*60) + int(now[1])*60 + int(now[2])
				dtm = str(ldata.Time).split(":") #end time of data
				dtm1 = str(ldata1.Time).split(":") #end time of data
				dtmVal = int(dtm[0])*(60*60) + int(dtm[1])*60 + int(dtm[2]) + 1800 #30 minutes (more as compared to end time)
				dtmVal1 = int(dtm1[0])*(60*60) + int(dtm1[1])*60 + int(dtm1[2])

				if nowVal > dtmVal1:
					if nowVal < dtmVal:
						runst = "Running1.."
					else:
						runst = "Stopped1"

					ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time()).last()
					sitedata = DBData.objects.get(CID_No=Rid)

					instchart = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time())
					for x in instchart:
						x2.append(str((x.Time).strftime('%H:%M')))
						y3.append(x.Power*1000)
						y4.append(x.LPD)

					return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2, 'y3': y3, 'y4':y4})
				else: 
					sitedata = ''
					ldata = ''
					runst = "Not Running/Stopped2"
					return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst})

		else: #if data not available, gen data
			rtime = 82800 #rend  time to gen data when open app 11PM
			rTime = time.strftime('%H:%M:%S', time.gmtime(rtime))
			dt = random.randint(0, 4) #if it gen 0, system should not have live data

			#if data not generated, it should not generate forever for that day
			hmd = homeid.objects.get(CID_No=Rid)
			
			if hmd.Date:
				if hmd.Date != date.today():
					hmd =  homeid.objects.filter(CID_No=Rid).update(Status=dt, Date=date.today())
					hmd = homeid.objects.get(CID_No=Rid)
			else:
				hmd =  homeid.objects.filter(CID_No=Rid).update(Status=dt, Date=date.today())
				hmd = homeid.objects.get(CID_No=Rid)

			if datetime.now().strftime("%H:%M:%S")<rTime and dt>=1: #if app open after 6.30, data should not genreate
				sTime = random.randint(25200, 30600) #Morning Start time (Ex. 7AM = 7x60x60 = 25200)
				eTime = random.randint(50400, 63000) #Evening End time


				stepTime = 0 
				dTimeVal = sTime
				
				#Change end time randomly 9AM to 2PM
				etm = random.randint(0, 4)
				if etm<=1:
					eTimeUpdate =  random.randint(32400, 50400)
					eTime = eTimeUpdate

				if sitedtls.Capacity=='2HP DC':
					volt = 220
					ifact = 1
					vfact = 1
					lphfact = 6000
					minp=0.3 #minimum power
				else: #5HP 
					volt = 584
					ifact = 2 # two parallel strings
					vfact = 2
					lphfact = 1700 #For 5HP
					minp=0.5

				trunTime = 0
				power = 0
				grossKwh = 0
				grosslpd0 = 0

				while dTimeVal<eTime:
					dThr0 = dTimeVal/3600 #Previous time for energy calc
					dTimeVal = dTimeVal+stepTime
					dTime = time.strftime('%H:%M:%S', time.gmtime(dTimeVal))
					dThr = dTimeVal/3600 #Time in Hours Format such as 7AM etc..
					Irr = (0.282*pow(dThr,4)-13.52*pow(dThr,3)+203.9*pow(dThr,2)-1011*dThr+1274)*0.9711

					if Irr<0:
						Irr = 0

					##PV Curve Based on Irradiance (Irradiance Based on Time)	
					temp = 25+(Irr-0)*(50-25)/739
					Tc = 25+(((temp-20)/0.8)*(Irr/1000))
					shadow = random.randint(75, 100)/100
					cloud = random.randint(0,5)

					if cloud<1:
						cloud = random.randint(30,50)/100
					else:
						cloud = 1

					pvolt = int((volt + math.log((Irr/1000), 2.72))*((1+(-0.3*(Tc-25)/100)))/vfact)*(random.randint(95, 102)/100) #PV Voltage
					pvi = (8.22*(Irr/1000))*((1+(0.05*(temp-25)/100)))*ifact*0.93*shadow*cloud #PV Current
										
					power0 = power
					power = pvolt*pvi/1000 #in kW
					energy = (dThr-dThr0)*(power+power0)/2				
					lph = int(power*lphfact)

					trunTime = trunTime+(dThr-dThr0)	
					
					if power<minp:
						lph = 0
						grosslpd = grosslpd0
						grossKwh = grossKwh
					else:
						grosslpd = int((lphfact*(dThr-dThr0)*(power+power0)/2)+grosslpd0)
						grossKwh = grossKwh+energy

					grosslpd0 = grosslpd

					#Step time 10 to 12 minutes
					stepTime = random.randint(600, 720)

					if sitedtls.Capacity=='5HP AC':
						freq = (15.795*power-(1.73161*power*power)+12.5331)*0.95	
						if power<minp:
							freq = 0
					else: 
						freq = None #for DC Pumps

					DataSet = BHInstData.objects.create(CID_No=Rid, Date=date.today(), Time=dTime, Voltage=pvolt, Current=pvi, Power=power, Frequency=freq, Energy=energy, GrossEnergy=grossKwh, LPD=lph, GrossLPD=grosslpd, PumpRunHours=trunTime, RunStatus=True)
				
				datalen = BHInstData.objects.filter(CID_No=Rid, Date=date.today())
				
				if datalen:
					#Delete randomly some data form generated data
					dltper = random.randint(7, 12)/100
					dlt = len(datalen)*dltper #10% data rows deleting
					for i in range(int(dlt)):
						x=BHInstData.objects.filter(CID_No=Rid, Date=date.today())
						num = random.randint(1, len(x)-1)
						y = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[num]
						y.delete()
					del_hours = dlt*11/60 #delete time in hours
					data_hrs = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).last()
					updt_hrs = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).update(PumpRunHours=data_hrs.PumpRunHours-del_hours)
					
					#Instantaneous Data Summary Store in Day Wise Data
					ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today()).last()
					ldata1 = BHInstData.objects.filter(CID_No=Rid, Date=date.today())[0]
					daydata = BHData.objects.create(CID_No=Rid, Date=date.today(), DayEnergy=ldata.GrossEnergy, LPD=ldata.GrossLPD, PumpRunHours=ldata.PumpRunHours)
					dbexdata = DBData.objects.get(CID_No=Rid)

					
					if sitedtls.Capacity == '2HP DC':
						del_energy = random.randint(455, 550)/100 #delete avg. per day energy
						del_hrs = random.randint(25, 35)/10 #delete avg. per day hours
						del_lpd= 	random.randint(5500, 6200)*del_energy #delete avg. per day hours
						updt = DBData.objects.filter(CID_No=Rid).update(GrossEnergy=dbexdata.GrossEnergy-del_energy, GrossLPD=dbexdata.GrossLPD-del_lpd, PumpRunHours=dbexdata.PumpRunHours-del_hrs)

					dbdt = DBData.objects.get(CID_No=Rid)
					dbdata = DBData.objects.filter(CID_No=Rid).update(GrossEnergy=dbdt.GrossEnergy+daydata.DayEnergy, GrossLPD=dbdt.GrossLPD+daydata.LPD, PumpRunHours=dbdt.PumpRunHours+daydata.PumpRunHours)
					

					now = (datetime.now().strftime("%H:%M:%S")).split(":")
					nowVal = int(now[0])*(60*60) + int(now[1])*60 + int(now[2])
					dtm = str(ldata.Time).split(":") #end time of data
					dtm1 = str(ldata1.Time).split(":") #start time of data
					dtmVal = int(dtm[0])*(60*60) + int(dtm[1])*60 + int(dtm[2]) + 30 #30 minutes (more as compared to end time)
					dtmVal1 = int(dtm1[0])*(60*60) + int(dtm1[1])*60 + int(dtm1[2])
					
					if nowVal > dtmVal1:						
						if nowVal < dtmVal:
							runst = "Running2.."
						else:
							runst = "Stopped3"
						ldata = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time()).last()
						sitedata = DBData.objects.get(CID_No=Rid)

						instchart = BHInstData.objects.filter(CID_No=Rid, Date=date.today(), Time__lt=datetime.now().time())
						for x in instchart:
							x2.append(str((x.Time).strftime('%H:%M')))
							y3.append(x.Power*1000)
							y4.append(x.LPD)

						return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2, 'y3': y3, 'y4':y4})
					else: #Time is early when open app than created data
						sitedata = ''
						ldata = ''
						runst = "Not Started/Stopped4"
						return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})
				else: 
					sitedata =  ''
					ldata = ''
					runst = "Not Running/Stopped5"
					return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})


			else:
				sitedata =  '' 
				ldata = ''
				runst = "Not Running/Stopped6"
				return render(request, 'iddb.html', {'sitedtls':sitedtls, 'sitedata':sitedata, 'ldata':ldata, 'runst':runst, 'x1':x1, 'y1':y1, 'y2':y2})



