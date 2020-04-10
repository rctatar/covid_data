# function to generate graph from CSSE COVID-19 data
# 2020-Apr-10 RCT V1.5
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import date, datetime

#from matplotlib.dates import (YEARLY, DAILY, DateFormatter, rrulewrapper, RRuleLocator, drange)
from matplotlib.dates import (DateFormatter, WeekdayLocator, MO, drange, datestr2num)

import numpy as np
from scipy.optimize import curve_fit

#today = date.today()
today = datetime.now()

# To display interactively, uncomment the following line.
#matplotlib.interactive('True')

covid_all = pd.read_csv("US_Covid.txt", header=None)

x0 = 43+28+2
dates = covid_all.iloc[0:1, x0:]
tdates = dates.transpose()
x = datestr2num(tdates[0].values)

covid_data = covid_all.iloc[1:3, x0:]
covid = covid_data.transpose()
covid.columns = ['Infections', 'Deaths']

y = covid['Infections'].astype(float).values
y2 = covid['Deaths'].astype(float).values

fig, ax = plt.subplots()

# Add pre-fit data
pdates = covid_all.iloc[0:1, 4:]
ptdates = pdates.transpose()
px = datestr2num(ptdates[0].values)

x0_date = tdates[0].values[0]
x0_str = datetime.strptime(x0_date, '%m/%d/%y').strftime('%Y-%b-%d')
print(f'x0 = {x0_str}')

pcovid_data = covid_all.iloc[1:3, 4:]
pcovid = pcovid_data.transpose()
pcovid.columns = ['Infections', 'Deaths']

py = pcovid['Infections'].astype(float).values
py2 = pcovid['Deaths'].astype(float).values

plt.plot_date(px,py, label='Infections', color='cornflowerblue', markersize=4)
plt.plot_date(px,py2, label='Deaths', color='red', markersize=4)
plt.yscale('log')

formatter = DateFormatter('%b-%d')
ax.xaxis.set_major_formatter(formatter)

loc = WeekdayLocator(byweekday=MO, interval=1)
ax.xaxis.set_major_locator(loc)
plt.ylabel('# infections and deaths (n)')
plt.title(f'US Data and Model for {today.strftime("%Y-%b-%d %H:%M:%S")}')

# Calculate Model
#inf = covid['Infections'].values

dlen = len(y)
ind = np.linspace(1,dlen,dlen)

cf = curve_fit(lambda t,a,b: a*np.exp(b*t), ind, y, p0=(100,0.25))
cf2 = curve_fit(lambda t,a,b: a*np.exp(b*t), ind, y2, p0=(5,0.25))

ndays = 14
forward = np.linspace(dlen+1, dlen+ndays, ndays)

# To compute all values in forward index
f = lambda x: cf[0][0]*np.exp(cf[0][1]*x)
FI = f(forward)
Infections_Model = 'Model Infections(x) = {:.3f}*Exp[{:.4}*(x-x0)]'.format(cf[0][0],cf[0][1])

f2 = lambda x: cf2[0][0]*np.exp(cf2[0][1]*x)
FD = f2(forward)
Deaths_Model = 'Model Deaths(x) = {:.4f}*Exp[{:.4}*(x-x0)]'.format(cf2[0][0],cf2[0][1])

plt.text(0.02,0.67,Infections_Model,transform=ax.transAxes, color='cornflowerblue')
plt.text(0.02,0.62,Deaths_Model,transform=ax.transAxes, color='red')
plt.text(0.02,0.57,f'x = day, x0 = {x0_str}', transform=ax.transAxes, color='grey')

ndays = 14
lastx = x[-1]+1
fx = [ lastx+i for i in range(ndays) ]

plt.plot_date(fx, FI, linestyle='solid', marker='None', label='Model Infections', color='cornflowerblue')

plt.plot_date(fx, FD, linestyle='solid', marker='None', label='Model Deaths', color='red')
plt.legend()

plt.grid(linestyle='-', color='lightgrey')

#print(f'x = {x}')
#print(f'y = {y}')
#print(f'y2 = {y2}')

fig.set_figheight(5)
fig.set_figwidth(9)

plt.xticks(rotation='25')
plt.savefig('covid.png')
          
