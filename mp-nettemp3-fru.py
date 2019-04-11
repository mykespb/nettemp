
# coding: utf-8

# Mikhail Kolodin. 
# Project: Internet temperature.
# 2015-12-15 1.3.3
# 
# IPython research for internet temperature. 
# We use now only fontanka.ru website, 
# later other sites and methods will be added.
# 
# Version with database recording.
# Now full archive of headers since 2000.

# In[1]:

import requests
import lxml.html as lh

import datetime
now = datetime.datetime.now()
import time

import sqlite3


# In[25]:

# do we print all messages every days, or only several to check received data
printAll = True
#printAll = False
# total counter of received news
allNews = 0
# how many do we show
maxShow = 5
# seconds to wait between calls (may be 0.1 etc)
waitSec = 1  


# In[14]:

db = "mp-nettemp3-fru.db"
conn = sqlite3.connect(db)

conn.execute('''DROP TABLE IF EXISTS netdata''')
conn.execute('''CREATE TABLE netdata (source text, ndate text, addr text, header text, wpos int, wneg int, mark number)''')
conn.commit()
source = "fontanka"


# In[15]:

url = "http://www.fontanka.ru/fontanka/"


# In[16]:

myyear, mymonth, myday = now.year, now.month, now.day
plus = "{0:04d}/{1:02d}/{2:02d}" .format (myyear, mymonth, myday)
fullurl = url + plus + '/all.html'
print ("Getting data from {}" .format(fullurl))


# In[26]:

def getoneday(ayear, amonth, aday, fullurl):
    """get all headers from fontanka for 1 given day"""
    global allNews
    thisdt = "{0:04d}-{1:02d}-{2:02d}" .format (ayear, amonth, aday)
    print ("This DT {}" .format (thisdt))
    try:
        print ("Full URL = {}" .format (fullurl))
        page = requests.get(fullurl)
        tree = lh.fromstring(page.text)

        arts = tree.xpath("//div[@class='calendar-item']")
        print ("found {} records" .format(len(arts)))
        weShowed = 0
        
        for art in arts:
            dt = art.xpath("div[@class='calendar-item-date']")[0].text.strip()
            tit = art.xpath("div[@class='calendar-item-title']/a")[0].text.strip()
            outdt = thisdt + " " + dt

            conn.execute("""INSERT INTO netdata (source, ndate, addr, header, wpos, wneg, mark) VALUES (?, ?, ?, ?, ?, ?, ?)""", (source, outdt, fullurl, tit, 0, 0, 0))
            conn.commit()
            
            weShowed += 1
            if weShowed <= maxShow:
                print ("{} {}" .format (dt, tit))
            else:
                print (".", end="")

    except:
        print ("Error or no such date")
    time.sleep(waitSec)

    print ("...\nTotal records: {}" .format(len(arts)))
    allNews += len(arts)


# In[1]:

def getalldays():
    """get info for all days in history"""
    for ayear in range(2000, 2016):
        for amonth in range(1, 13):
            for aday in range(1, 32):
                fulldate = "{0:04d}/{1:02d}/{2:02d}" .format (ayear, amonth, aday)
                fullurl = url + fulldate + "/all.html"
                print ("Processing {}" .format(fullurl))
                getoneday (ayear, amonth, aday, fullurl)


# In[20]:

getalldays()


# In[24]:

conn.close()


# Details and refs:
# 
# SQLite
# https://docs.python.org/2/library/sqlite3.html#sqlite3.connect
# 
# XSL
# https://msdn.microsoft.com/ru-ru/library/ms256086(v=vs.120).aspx
# 
