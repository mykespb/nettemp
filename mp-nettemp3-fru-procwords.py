
# coding: utf-8

# Mikhail Kolodin. Project: Internet temperature. 2015-12-15 1.4.1
# 
# IPython research for internet temperature. We use now only fontanka.ru website, later other sites and methods will be added.
# 
# Version with database recording. Now full archive of headers since 2000.
# 
# Here we count good and bad words in the database. No more downloading info from websites.

# In[2]:

import datetime
now = datetime.datetime.now()
import time

import sqlite3


# Part I. Get database with data and correct it. 

# In[74]:

db = "mp-nettemp3-fru-2015.db"
conn = sqlite3.connect(db)
cur = conn.cursor()


# In[75]:

#conn.execute ("alter table netdata add dtyear int")


# In[76]:

cur.execute ("select count(*) from netdata")
print ("total records: {}" .format(cur.fetchone()))


# In[77]:

rc = cur.execute ("select distinct substr(ndate, 1, 10) from netdata")
cnt = 0
for r in rc: cnt += 1
print ("We have data for {} days" .format(cnt))


# In[78]:

#cur.execute ("update netdata set dtyear = substr(ndate, 1, 10)")
#conn.commit()


# Part II. get good and bad words and strore them locally.

# In[34]:

goods, bads = "words-good.txt", "words-bad.txt"


# In[40]:

with open(goods) as good:
    goodw = good.read().split()
goodw.sort()
goodw = tuple(goodw)


# In[41]:

print ("Good words:", goodw)


# In[42]:

with open(bads) as bad:
    badw = bad.read().split()
badw.sort()
badw = tuple(badw)


# In[43]:

print ("Bad words:", badw)


# Part III. Process add data in database, 
# set wpos, wneg, mark as counters for good and bad words in each record.

# In[79]:

cur.execute ("select *, rowid from netdata")


# In[80]:

toshow = 10
shown = 0

for row in cur.fetchall():
    header = row[3].lower()
    dthere = row[1]
    cpos = cneg = 0
    for w in goodw:
        if w in header:
            cpos += 1
    for w in badw:
        if w in header:
            cneg += 1
    mark = cpos - cneg
    rid = row[-1]
    cur.execute ("update netdata set wpos=?, wneg=?, mark=? where rowid=?", (cpos, cneg, mark, rid))
    if shown < toshow:
        print ("update: rowid={5}, dt={4}, header={0}, wpos={1}, wneg={2}, mark={3}" .format(header, cpos, cneg, mark, dthere, rid))
        shown += 1


# In[81]:

conn.commit()


# In[49]:

conn.close()


# In[ ]:



