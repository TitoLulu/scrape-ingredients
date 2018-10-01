
# coding: utf-8

# In[274]:


import os
IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open
import pandas as pd


# In[313]:


import numpy as np
import csv


# In[276]:


import urllib


# In[277]:


from bs4 import BeautifulSoup


# In[681]:


class ScrapeGrowFit:
    
    def getName(self, url):
        growUrl="https://getgrowfit.com/collections/essentials"
        openGrowUrl= urllib.urlopen(url)
        parseGrowUrl=BeautifulSoup(openGrowUrl, 'html.parser')
        productnames=[]
        for a_tag in parseGrowUrl.findAll("div", attrs={"class": "details ng-scope"}):
            a_tag=a_tag.findAll("a")
            
            for tag in a_tag:
                product_title=tag.findAll('p')
                for prod in product_title:
                    productnames.append(prod.text.strip())
                    #print(productnames)
        return productnames
    def getInnnerUrl(self, url):
        growUrl=url
        openGrowUrl= urllib.urlopen(url)
        parseGrowUrl=BeautifulSoup(openGrowUrl, 'html.parser')
        innerlinks=[]
        for a_tag in parseGrowUrl.findAll("div", attrs={"class": "details ng-scope"}):
            innerlinks.append("https://getgrowfit.com" + a_tag.a['href'])
            
            #print(innerlinks)
        return innerlinks
    def extractIngredientInformation(self,innerlinks):
        ingredients=[]
        for link in innerlinks:
            openlinks=urllib.urlopen(link)
            soup=BeautifulSoup(openlinks, "html.parser")
            for row in soup.find_all("div", attrs={"class":"ingre"}):
                ingredients.append(row.text.strip())
           # print(ingredients)

        return ingredients
    def write2csv(self,productnames, ingredients):
        products=pd.DataFrame(productnames, columns=['Attas & Flours'])
        ingred=pd.DataFrame(ingredients, columns=['Attas & Flours Ingredients'])
        growAttasandFlours=pd.concat([products, ingred], sort=False)
        
        
        growAttasandFlours.to_excel("Breakfasts.xlsx")
        
       
            


# In[682]:


checkproducts=ScrapeGrowFit()


# In[683]:


products=checkproducts.getName("https://www.bigbasket.com/cl/foodgrains-oil-masala/?nc=nb")


# In[684]:


productsInnerUrl=checkproducts.getInnnerUrl("https://getgrowfit.com/collections/breakfast")


# In[685]:


productsIngredients=checkproducts.extractIngredientInformation(productsInnerUrl)


# In[687]:


dataframes=checkproducts.write2csv(products,productsIngredients)


# In[656]:


