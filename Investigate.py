#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset (TMDB movies !)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > we are going to do some games with our dataset(TMDB Movies) to know the properties of our dataset for answering some questions such as  ''What kinds of properties are associated with movies that have high revenues''.

# In[86]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > In this section of the report, We will load in the data, check for cleanliness, and then trim and clean our dataset for analysis.
# 
# ### General Properties
# Dataset chosen for analysis: TMDB movies
# >This data set contains information more than 10,000 movies collected from The Movie Database (TMDb),including user ratings and revenue.I'll ask questions related to genres and popularity.
# 
# Questions to answer:
# >1- Which genres are most popular from year to year?
# 
# >2- What kinds of properties are associated with movies that have high revenues?

# In[87]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df=pd.read_csv('tmdb-movies.csv')
df.head(2)


# In[88]:


df.describe()


# In[89]:


df.info()


# In[90]:


df.shape


# <a id='eda'></a>
# 
# Data Cleaning (drop unneeded columns, fix structure)
# >TMDb Movie Data is the choosen dataset
# The database contains information about movies collected from The Movies Database, including revenue, budget.
# 
# The Data Structure
# >Before working with the data I checked the database and found missing values, inconsistency or inadequate datatype. After getting more information and find out the questions I wanted to pose, I cleaned the database. There were unecessary columns with missing data, inadequate datatypes. The columns 'genres' and 'production_companies' contained multiple values that doesn't meet the requirements of the normal form.
# 
# The Cleaning Process
# >I removed the columns cast, homepage, tagline, keywords, overview and imdb id to improve database redability.
# The column 'genres' and 'productions_companies' were not in the first normal form which requires that in the table should not have multiple value in the same row of data. I was unable to create a second joined column, so I decided to remove the values after the first '|' sign to get better grouping and cleaner visualization in the further analysis.
# I casted release_date from string to date datatype.
# I converted the columns revenue, budget from float to int.
# I dropped the Null value raws

# In[91]:


'''we can drop some columns to make it more readable'''
df=df.drop(['id','cast', 'homepage', 'tagline', 'keywords', 'overview', 'imdb_id'], axis=1)
df.head(1)


# In[92]:


'''drop rows with missing values'''
df = df.dropna()
df.info()


# after this cleaning we are going to visualize our new data

# In[93]:


df.hist(figsize=(15,10))


# In[94]:


#dropping the null values

df.dropna(inplace=True)
df.info()


# In[95]:


# Convert release_date (object datatype) to date.

df['release_date'] = pd.to_datetime(df['release_date'])


# In[96]:


#replace 0 values with means in columns budget.

df['budget'] = df['budget'].replace(0,df['budget'].mean())


#replace 0 values with means in columns revenue.

df['revenue'] = df['revenue'].replace(0,df['revenue'].mean())


# In[97]:


#delete extra data from the rows with multiple values.

df['genres'] = df['genres'].apply(lambda x: x.split('|')[0])

df['production_companies'] = df['production_companies'].apply(lambda x: x.split('|')[0])


# In[98]:


df.head(3)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# >  Now that we've trimmed and cleaned our data, we're ready to move on to exploration.
# ### Research Question 1 (What kinds of properties are associated with high revenues?)

# In[99]:


# Sort movies by revenue in descending order.

sorted_revenue_biggest = df.sort_values(by=['revenue'], ascending = False).head(200)
sorted_revenue_biggest.head(1)


# In[100]:


sorted_revenue_biggest.popularity.hist()


# In[101]:


sorted_revenue_biggest.runtime.hist()


# In[102]:


sorted_revenue_biggest.genres.hist(figsize=(20,12))


# we see that the most revenuable movies has popularity between 0 and 5, runtime is between 100-130 min for most of them, and the action and animations are the most populare movies.
# 
# 

# ### Are short movies more popular?

# In[103]:


short_movies = df.sort_values(by=['runtime'], ascending = False).head(200)
runtime = short_movies['runtime']
popularity = short_movies['popularity']


# In[104]:


plt.scatter(runtime, popularity)
plt.show()


# as we see the more popular movies is the shortest movies.

# ### Research Question 2  (Which genres are most popular from year to year?)

# In[105]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
genres_popularity = df.groupby(['genres'])['popularity'].mean()
genres_popularity


# In[106]:


plt.subplots(figsize=(22, 6))
plt.bar(genres_popularity.index, genres_popularity)
plt.title('popularity by genre')
plt.xlabel('genre')
plt.ylabel('Popularity');


# as we see that Adventure movies is the most popular genre then the science fiction movies is the second one (Marvel and DC war ::""D).

# <a id='conclusions'></a>
# ## Conclusions
# 
# > it was a good game haha..now we are going to do a small Summary to get a decisions for our future industry.
# > from first question : we get that the most revenuable movies has popularity between 0 and 5, runtime is between 100-130 min for most of them, and the action and animations are the most populare movies. the more popular movies is the shortest movies.
# 
# >from second question we get that Adventure then science fiction movies are the most popular
# 
# >> so in future when we are making movies we should invest in adventure and science fiction movies with as short time as we can
# 

# In[107]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

