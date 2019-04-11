
# coding: utf-8

# IPython reserach for internet temperature. 
# We use now only fontanka.ru website, 
# later other sites and methods will be added.

# In[20]:

import requests
import lxml.html as lh

import datetime
now = datetime.datetime.now()


# In[30]:

url = "http://www.fontanka.ru/fontanka/"


# In[106]:

myyear, mymonth, myday = now.year, now.month, now.day
plus = "{0:04d}/{1:02d}/{2:02d}" .format (myyear, mymonth, myday)
fullurl = url + plus + '/all.html'
print ("Getting data from {}" .format(fullurl))


# In[107]:

page = requests.get(fullurl)
tree = lh.fromstring(page.text)
#print(tree.text_content())


# In[108]:

#bloks = tree.xpath("//div[@class<='entry article switcher-all-news']")
bloks_spb = tree.xpath("//div[@class='entry article switcher-all-news switcher-spb-news']")
bloks_rus = tree.xpath("//div[@class='entry article switcher-all-news switcher-russian-news']")
bloks_world = tree.xpath("//div[@class='entry article switcher-all-news switcher-world-news']")
bloks = bloks_spb + bloks_rus + bloks_world


# In[109]:

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


# In[110]:

for blog in blogs:
    blok = blog[1]
    dt = blok.xpath("div[@class='entry_date']")
    if dt[0].text.strip()[2] != ":": continue
    print (blog[0], plus, dt[0].text.strip(), end=" ")
    tit = blok.xpath("div[@class='entry_title']")
    ref = tit[0].xpath("a[@href]")
    print (ref[0].text.strip())


# In[ ]:



