
# coding: utf-8

# Mikhail Kolodin. 
# Project: Internet temperature.
# 2015-12-15 1.2.2
# 
# IPython research for internet temperature. 
# We use now only fontanka.ru website, 
# later other sites and methods will be added.
# 
# Version with database recording.

# In[10]:

import requests
import lxml.html as lh

import datetime
now = datetime.datetime.now()

import sqlite3


# In[76]:

db = "mp-nettemp2-fru.db"
conn = sqlite3.connect(db)

conn.execute('''DROP TABLE IF EXISTS netdata''')
conn.execute('''CREATE TABLE netdata (source, areal, ndate, addr, mshort, mlong)''')
conn.commit()
source = "fontanka"


# In[77]:

url = "http://www.fontanka.ru/fontanka/"


# In[78]:

myyear, mymonth, myday = now.year, now.month, now.day
plus = "{0:04d}/{1:02d}/{2:02d}" .format (myyear, mymonth, myday)
fullurl = url + plus + '/all.html'
print ("Getting data from {}" .format(fullurl))


# In[79]:

page = requests.get(fullurl)
tree = lh.fromstring(page.text)
#print(tree.text_content())


# In[80]:

bloks_spb = tree.xpath("//div[@class='entry article switcher-all-news switcher-spb-news']")
bloks_rus = tree.xpath("//div[@class='entry article switcher-all-news switcher-russian-news']")
bloks_world = tree.xpath("//div[@class='entry article switcher-all-news switcher-world-news']")
bloks = bloks_spb + bloks_rus + bloks_world


# In[81]:

blogs_spb = []
for b in bloks_spb:
    blogs_spb.append (("spb", b))
blogs_rus = []
for b in bloks_rus:
    blogs_rus.append (("rus", b))
blogs_world = []
for b in bloks_world:
    blogs_world.append (("mir", b))
blogs = blogs_spb + blogs_rus + blogs_world
#print (blogs)


# In[82]:

def procref (addr):
    """get full text of news"""
    if addr == "": return
    page = requests.get(addr)
    tree = lh.fromstring(page.text)
    try:
        full = tree.xpath("//div[@class='article_fulltext']")
        print (full[0].xpath("./p"))
#        print (full[0].text.strip())
    except:
        print ("None")


# In[83]:

for blog in blogs:
    blok = blog[1]
    dt = blok.xpath("div[@class='entry_date']")
    dtout = dt[0].text.strip()
    if dtout[2] != ":": continue
    plusout = plus.replace("/", "-")
    print (blog[0], plusout, dtout, end=" ")
    tit = blok.xpath("div[@class='entry_title']")
    ref = tit[0].xpath("a[@href]")
    outtext = ref[0].text.strip()
    print ("text = [{}]" .format (outtext), end=" ")
    goes = tit[0].xpath("a/@href")[0]
    if goes.startswith('/'):
        goes = url + goes
    print ("goto = [{}]" .format(goes))
#    procref(goes)
    
    alldtout = plusout + " " + dtout
    conn.execute("""INSERT INTO netdata (source, areal, ndate, addr, mshort, mlong) VALUES (?, ?, ?, ?, ?, ?)""", (source, blog[0], alldtout, goes, outtext, ""))
    conn.commit()
    
print ("...\nTotal records: {}" .format(len(blogs)))


# In[84]:

conn.close()


# In[ ]:



