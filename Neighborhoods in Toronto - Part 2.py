
# coding: utf-8

# In[1]:



#Import the required Libraries
import pandas as pd
import numpy as np
import requests
print("Imported Libraries")


# In[2]:


#Download the URL from wikipedia page
url  = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
page = requests.get(url)
if page.status_code == 200:
    print('URL downloaded successfully')
else:
    print('ERROR in Downloading. Error code: {}'.format(page.status_code))


# In[4]:


#We have to discard the "Not Assigned" columns, so we set them to NaN, so that we can later use the dropna method.
df_Canada = pd.read_html(url, header=0, na_values = ['Not assigned'])[0]
df_Canada.head()


# In[5]:


#Drop the "Borough" rows which are empty
df_Canada.dropna(subset=['Borough'], inplace=True)


# In[8]:


#Number of rows in "Neighborhood" which are empty, but "Borough" exists
n_empty_neighborhood = df_Canada[df_Canada['Neighbourhood'].isna()].shape[0]
print('Number of rows in Neighborhood column which are empty: {}'.format(n_empty_neighborhood))

#Rows in which "Neighborhood" is emtpy but "Borough" exists
df_Canada[df_Canada['Neighbourhood'].isna()]


# In[9]:


#Replace NaN value in "Neighborhood" with "Borough" name & recheck the rows again
df_Canada['Neighbourhood'].fillna(df_Canada['Borough'], inplace=True)
n_empty_neighborhood = df_Canada[df_Canada['Neighbourhood'].isna()].shape[0]
print('Number of rows in Neighborhood column which are empty: {}'.format(n_empty_neighborhood))


# In[10]:


#Recheck the "Neighborhood" value on "Queen's Park" row
df_Canada[df_Canada['Borough']=="Queen's Park"]


# In[11]:


#Groupby Postcodes/Borough
df_postcodes = df_Canada.groupby(['Postcode','Borough']).Neighbourhood.agg([('Neighbourhood', ', '.join)])
df_postcodes.reset_index(inplace=True)
df_postcodes.head(5)


# In[12]:


#Check "Downtown Toronto", and compare it with the dataframe shown in the assignment
df_postcodes[df_postcodes['Borough']=='Downtown Toronto']


# In[13]:


#Shape of the dataset
print('The shape of dataset is:',df_postcodes.shape)


# In[15]:


#Export dataset to .csv file, So that we can use it in future Projects
df_postcodes.to_csv('Canada_Postcodes.csv')
print("File Saved")

