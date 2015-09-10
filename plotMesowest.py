
import Meteoframes as mf 
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import dates
import datetime
import os
import seaborn as sns
import pandas as pd 

sns.set_color_codes()

mesofiles=[ '/home/rvalenzuela/SURFACE/case03/KAPC_Napa_County_Airport.xls',
			'/home/rvalenzuela/SURFACE/case03/KSTS_Santa_Rosa.xls',
			'/home/rvalenzuela/SURFACE/case03/KUKI_Ukiah_Municipal_Airport.xls']

st = datetime.datetime(2001, 1, 23, 0, 0)
en = datetime.datetime(2001, 1, 25, 0, 0)
var=['TMP','RELH','DRCT']
hl=[]
xticks = pd.date_range(start=st,end=en, freq='3H')
fig,ax = plt.subplots(3,1,figsize=(13,10),sharex=True)
for i,f in enumerate(mesofiles):
	df=mf.parse_mesowest_excel(f)
	df2=df[st:en]
	for j in range(3):
		l=ax[j].plot(df2.index,df2[var[j]],'-o')
		ax[j].invert_xaxis()
		ax[j].set_xticks(xticks)
		ax[j].set_xlim([en,st])
		if j == 0: hl.append(l)

lns = hl[0]+hl[1]+hl[2]
labs = ['KAPC','KSTS','KUKI']
deg_sign= u'\N{DEGREE SIGN}'
ax[0].legend(lns, labs, loc=0)
ax[0].set_ylabel('Temperature [' +deg_sign+'C]')
ax[1].set_ylim([40,105])
ax[1].set_ylabel('Relative humidity [%]')
ax[2].set_yticks(range(0,360+60,60))
ax[2].set_ylabel('Wind direction [deg]')
datefmt = dates.DateFormatter('%H\n%d')
ax[2].xaxis.set_major_formatter(datefmt)
ax[2].set_xlabel(r'$\Leftarrow$'+' Time [UTC]')
t1='NWS surface observations (source: Mesowest)'
t2='\nDate: ' + st.strftime('%b-%Y')
plt.suptitle(t1+t2)
plt.show()
