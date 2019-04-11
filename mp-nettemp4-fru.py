
# coding: utf-8

# Mikhail Kolodin.
# 
# Project: Internet temperature. 2015-12-18 1.5.1
# 
# IPython research for internet temperature. We use now only fontanka.ru website, later other sites and methods will be added.
# 
# Version with database recording. Now full archive of headers since 2000.
# 
# Here we count good and bad words in the database. No more downloading info from websites.

# In[1]:

import datetime
now = datetime.datetime.now()

import sqlite3


# In[2]:

#%pylab inline
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date, time, timedelta
from time import gmtime, strftime


# In[3]:

# main db
db = "mp-nettemp3-fru-2015.db"
dbcf = "mp-nettemp3-fru-2015-stat.db"
conn = sqlite3.connect(db)
cur = conn.cursor()


# In[4]:

# temp db, later - also to main
#dbc = sqlite3.connect(":memory:")
dbc = sqlite3.connect(dbcf)
curc = dbc.cursor()


# In[110]:

# calc data per days
#dbc.execute("create table daydata (day text, wpos int, wneg int, mark number)")


# In[18]:

dbc.commit()


# In[5]:

cur.execute("select dtyear, sum(wpos), sum(wneg), sum(mark) from netdata group by dtyear")


# In[6]:

vals = []


# In[7]:

for row in cur:
    print (row)
    vals += [row]


# In[8]:

#print (vals)
vdates = []
vpos = []
vneg = []
vmark = []
for val in vals:
    vdates += [val[0]]
    vpos += [val[1]]
    vneg += [(-val[2])]
    vmark += [val[3]]
#print (vdates, vpos, vneg, vmark)


# In[9]:

#from matplotlib.finance import quotes_historical_yahoo_ochl
#from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
#from matplotlib.finance import quotes_historical_yahoo_ochl
#years = YearLocator()   # every year
#months = MonthLocator()  # every month
#yearsFmt = DateFormatter('%Y')
x = mdates.drange(datetime.strptime(vdates[0], "%Y-%m-%d"), 
    datetime.strptime(vdates[-1], "%Y-%m-%d"), 
    timedelta(days=1))
y = np.array(vmark)
#x = [v[0] for v in vdates]
#y = [v[0] for v in vdates]
x = np.array(range(len(y)))
sp = plt.subplot()
sp.plot_date(x, y, '-') 
#x
#y
sp.plot(x, y, '-')
#sp.title('title')
#sp.ylabel('marks')
#sp.grid(True)
#sp.plot_date(vdates, vmark, '-')
plt.show()


# In[105]:

conn.close()
dbc.close()


# In[ ]:



