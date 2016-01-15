''' 
	Plot METAR observations downloaded from
	mesowest site: http://mesowest.utah.edu

	Raul Valenzuela
	raul.valenzuela@coloraod.edu
'''


import Meteoframes as mf 
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import dates
from datetime import datetime
import os
import seaborn as sns
import pandas as pd 

sns.set_color_codes()
stname={	'KAPC': 'Napa County Airport',
			'KSTS': 'Santa Rosa Sonoma County Airport',
			'KUKI': 'Ukiah Municipal Airport',
			'KSCK': 'Stockton Metropolitan Airport'}
basedir='/home/rvalenzuela/SURFACE/'

def main():

	case=7
	mesocase=get_mesocase(case)
	mesofiles=mesocase['files']
	st = mesocase['dates'][0]
	en = mesocase['dates'][1]
	stations=mesocase['stations']
	var=['TMP','RELH','PMSL','DRCT']
	hl=[]
	xticks = pd.date_range(start=st,end=en, freq='3H')
	fig,ax = plt.subplots(len(var),1,figsize=(13,10),sharex=True)
	for i,f in enumerate(mesofiles):
		df=mf.parse_mesowest_excel(f)
		df2=df[st:en]
		for j in range(len(var)):
			l=ax[j].plot(df2.index,df2[var[j]],'-o')
			ax[j].invert_xaxis()
			ax[j].set_xticks(xticks)
			ax[j].set_xlim([en,st])
			if j == 0: hl.append(l)

	deg_sign= u'\N{DEGREE SIGN}'
	lns = [line[0] for line in hl]
	ax[0].legend(lns, stations, loc=0)
	ax[0].set_ylabel('Temperature [' +deg_sign+'C]')
	ax[1].set_ylim([40,105])
	ax[1].set_ylabel('Relative humidity [%]')
	ax[2].set_ylim([1015,1025])
	ax[2].set_ylabel('Pressure MSL [hPa]')
	
	ax[3].set_yticks(range(0,360+60,60))
	ax[3].set_ylabel('Wind direction [deg]')
	datefmt = dates.DateFormatter('%d\n%H')
	ax[3].xaxis.set_major_formatter(datefmt)
	ax[3].set_xlabel(r'$\Leftarrow$'+' Time [UTC]')
	
	t1='METAR surface observations (source: Mesowest)'
	t2='\nDate: ' + st.strftime('%b-%Y')
	plt.suptitle(t1+t2)
	plt.show(block=False)

def get_mesocase(casenum):

	case = {3: {'stations':['KAPC','KSTS','KUKI'], 
				'dates': [datetime(2001, 1, 23, 0, 0), datetime(2001, 1, 25, 0, 0) ],
				'files':[]},
			6: {'stations':['KSCK','KUKI'], 
				'dates': [datetime(2001, 2, 11, 0, 0), datetime(2001, 2, 12, 0, 0) ],
				'files':[]},				
			7: {'stations':['KSCK','KUKI'], 
				'dates': [datetime(2001, 2, 17, 0, 0), datetime(2001, 2, 18, 0, 0) ],
				'files':[]}				
			}

	mesocase=case[casenum]
	files=[]
	for s in mesocase['stations']:
		f=basedir+'case'+str(casenum).zfill(2)+'/'+s+'.xls'
		files.append(f)	
	mesocase['files']=files

	return mesocase

main()
