#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup as bs
import requests
import numpy as np
from time import sleep
from random import randint
import pandas as pd


# In[5]:


pages = np.arange(1,1000,100)
headers = {"Accept-Language": "en-US,en;q=0.5"}

movie_name = []
year = []
time=[]
rating=[]
gross = []
description = []


for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt")
    soup = bs(page.text, 'html.parser')
    movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
    sleep(randint(2,8))
    for store in movie_data:
        name = store.h3.a.text
        movie_name.append(name) 
        
        year_of_release = store.h3.find('span', class_ = "lister-item-year text-muted unbold").text
        
        year.append(year_of_release)
        
        runtime = store.p.find("span", class_ = 'runtime').text
        time.append(runtime)
        
        rate = store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
        rating.append(rate)
        
        
        value = store.find_all('span', attrs = {'name': "nv"})
        
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else 'na'
        description.append(description_)


# In[6]:


movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Duration": time,"Movie Rating": rating, "Description": description  })


# In[7]:


movie_list.head(5)


# In[8]:


for i in range(0,1000):
    year_str=movie_list['Year of Release'][i]
    year_str = year_str.replace("(", "")
    year_str = year_str.replace(")", "")
    year_str = year_str.replace("I", "")
    movie_list['Year of Release'][i]=year_str


# In[9]:


movie_list.head(5)


# In[10]:


movie_list.to_csv("IMDb movies.csv")


# In[11]:


movie_list

