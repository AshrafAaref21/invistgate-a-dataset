#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate TMDb movie data set
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
# 
# The author always had a big interest in watching movies. As most people did, the author also experienced good and bad movies. But what determines if a movie is considered as good or bad? There could be several factors influencig the quality of a movie, as for example the budget, genre, etc. This little project should help the author to improve his data analytics skills and explore some of the success criteria for movies. 
# 
# ### Questions to answer
# 
# <ul>
#     <li>Which genres are most popular from year to year?</li>
#     <li>What kinds of properties are associated with movies that have high revenues?</li>
#     <li>Did movies with higher vote count received a better rating?</li>
#     <li>What were the most popular produced genres in 2000 compared to 2015?</li>
#     <li>How did the amount of produced films changed over time?</li>
# </ul>
# 

# In[4]:


# Using this cell to set up import statements for all of the packages that are considered to be used
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

"""Changing scientific numbers to numeric numbers"""
#https://stackoverflow.com/questions/38689125/how-to-get-rid-of-pandas-converting-large-numbers-in-excel-sheet-to-exponential
pd.options.display.float_format = '{:.2f}'.format


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties

# In[7]:


# Loading the data and having a look at the first few lines
df = pd.read_csv('tmdb-movies.csv')
df.head()


# In[8]:


df.info(),
print('-------------')
print('Dataframe contains {} rows and {} columns'.format(df.shape[0],df.shape[1]))


# In[9]:


df.hist(figsize=(13,13));


# In[10]:


df.describe()


# ### Frist impression
# 
# There are plenty of columns indicating a problem. Many rows seems to contain several values, which are seperated by an "|". They need to be cleaned in the first place in order to provide a proper dataset for the intended analysis. The rows containing such values are:
# 
# <ul>
#     <li>cast</li>
#     <li>director</li>
#     <li>keywords</li>
#     <li>genres</li>
#     <li>production_companies</li>
# </ul>
# 
# Evenmore, there are columns in the dataset, which are not important to the intended analysis and therefore will be removed by the author. This includes:
# 
# <ul>
#     <li>imdb_id</li>
#     <li>homepage</li>
#     <li>overview</li>
#     <li>release_date</li>
#     <li>tagline</li>
# </ul>
# 
# ### Dealing with 0 and NaN
# df.info( ) revealed that most columns with important content for the analysis, such us revenue, release_year, etc. have a big amount of available data for the analysis. However, the .describe() method, as well as the histogramms, indicate that many columns, especially budget and revenue, contain many "0" in their columns. In order to provide a proper analysis, the columns "budget_adj", "revenue_adj", "budget", "revenue" and "runtime" will change its "0" values into "nan" and the respective colums will be dropped for the analysis.
# 

# ## Data Cleaning 

# In this section the before mentioned "0" will be replaced with nan-Values and will be dropped. Then, the rows with several values will be seperated in single columns containing only one value. This is needed in order to perform a proper analysis. Afterwards, unwanted rows for the analysis will be dropped, before the author will perform general data cleaning action as dropping duplicated lines, correct data types, check duplicated entries in some selected columns.

# In[11]:


df['revenue_adj'].replace(0, np.NAN, inplace=True)
df['revenue'].replace(0, np.NAN, inplace=True)
df['budget_adj'].replace(0, np.NAN, inplace=True)
df['budget'].replace(0, np.NAN, inplace=True)
df['runtime'].replace(0, np.NAN, inplace=True)

df.dropna(axis=0, inplace=True)


# In[12]:


"""Seperating columns with several values, split by an '|', into as many columns as needed"""
#source: https://apassionatechie.wordpress.com/2018/02/24/how-do-i-split-a-string-into-several-columns-in-a-dataframe-with-pandas-python/

df_c = (df['cast'].str.split('|', expand=True).rename(columns=lambda x: f"cast_{x+1}"))
df_d = (df['director'].str.split('|', expand=True).rename(columns=lambda x: f"director_{x+1}"))
df_k = (df['keywords'].str.split('|', expand=True).rename(columns=lambda x: f"keywords_{x+1}"))
df_g = (df['genres'].str.split('|', expand=True).rename(columns=lambda x: f"genres_{x+1}"))
df_p = (df['production_companies'].str.split('|', expand=True).rename(columns=lambda x: f"production_companies_{x+1}"))

#Checking df_c if split was conducted as intended
df_c.head()


# In[13]:


"""Joining the seperated columns to the original dataframe and
dropping unneeded columns for the analysis"""

df = df.join([df_c, df_d, df_k, df_g, df_p])
df = df.drop(['cast', 'keywords', 'director', 'genres', 'production_companies', 'imdb_id', 'homepage', 'overview', 'release_date', 'tagline'], axis=1)


# In[14]:


"""Checking number of duplicates"""
df.duplicated().sum()


# In[15]:


"""Checking if all rows contain the intended data type"""
df.dtypes


# So far the data looks prepared for the analysis, no duplicates have been found, columns containing multiple values have been seperated and data types look ready for analysis. Next, the author will use masks (or queries) to  have a deeper look, if some double entries are in specific columns.

# In[16]:


df['original_title'].value_counts().head()


# Since the value_counts() in the title column showed that there may be double entries of movie names, a function "check_double_title" was defined to have a deeper look in the rows with same movie title.

# In[17]:


"""Checking column for dubplicated original_title entries"""
limit_4_title = df['original_title'].value_counts().index.tolist()
limit_4_title = limit_4_title[:4]
limit_4_title

limit_4_id = df['original_title'].value_counts().index.tolist()

def check_double_title(names):
    for limit in limit_4_title:
        df_title = df[df['original_title'] == limit]
        print(df_title.iloc[:,:5])
        print("---------------------------------------------------------------------")
        
check_double_title(limit_4_title)


# In[18]:


print('Dataframe contains {} rows and {} columns'.format(df.shape[0],df.shape[1]))


# The results show that despite having a same movie title, the movies differ in other columns. Hence, the author implies that there are movies with the same title but different content. Therefore, no more rows need to be dropped. The drop of all rows containing relevant nan-values has led to a big decrease in the dataframe. Now, only 1287 movies will be used for the analysis. This will influence the outcome of the research questions.

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1: Which genres are most popular from year to year?

# In[19]:


# Selecting genres columns for the analysis of the original data frame
df_genres = df.loc[:, 'genres_1': 'genres_5' ]
# Adding release year to df_genres
df_genres_dates = df_genres.join(df['release_year'])


# In[20]:


years = df_genres_dates['release_year'].unique() #creates an array of years mentioned in release year 
most_common = [] #creates a list of tuples for most common genres in specific years

#for loop to create most_common list
for year in years:
    #creates df filtered by every year mentioned in years
    a = df_genres_dates[df_genres_dates['release_year'] == year] 
    #drops columns "release_year to perferm stack value count in next line
    b = a.drop(['release_year'], axis = 1)
    #performs value count trough genres_1 - genres_5 and stores the index of maximum count
    c = b.stack().value_counts().idxmax() 

    #creates a masked DataFrame for respective years
    x = df[df['release_year'] == year]
    #creates the mean of vote_average and stores the index of maximum value
    y = x.groupby(['genres_1'])['vote_average'].mean().idxmax()
    if c == y:
        z = 'Equal'
    else:
        z = 'Not equal'
        #appends year with value count trough genres_1 - genres_5, the highest average vote_average and indicates if the resulting columns match
    most_common.append((year, c, y, z))

#creates df for list of tuples named most_common
df_most_popular = pd.DataFrame(most_common, columns=['release_year', 'popular_produced_genre', 'popular_voted_gerne', 'is_equal']).sort_values('release_year').reset_index().drop(['index'], axis=1)
df_most_popular


# In[21]:


df_most_popular['is_equal'].value_counts()


# ### Research Question 2:  What kinds of properties are associated with movies that have high revenues?

# In[22]:


# Creating a copy of the original DataFrame
df_revenue = df


# In[23]:


#Performing basic statistic in order to create 4 classifications of the revenue_adj
df_revenue['revenue_adj'].describe()


# In[24]:


#Bin_edges correspond to min - max entries in previous cell. Quantiles are lables by bin_names.
#new column 'revenue_level' is created to classify columns based on revenues

bin_edges = [2.37,10465848.09,43956661.16,131648235.91,2827123750.41]
bin_names = ['very low' ,'low' ,'medium' ,'high' ] 
df_revenue['revenue_level'] = pd.cut(df_revenue['revenue_adj'], bin_edges, labels=bin_names)


# In[25]:


#list of revenue_levels classification is created for loop in next cell
df_revenue['revenue_level'].unique()
revenue_levels = df_revenue['revenue_level'].unique().tolist()
del revenue_levels[-1]


# In[26]:


#nested dictionary is created with 8 attributes based on revenue_levels

movie_data = {}

for level in revenue_levels:
    
    #stack.value_counts seciton
    grouped_data = df_revenue[df_revenue['revenue_level'] == level]
        #director
    director = grouped_data.loc[:, 'director_1': 'director_6']
    frequent_director = director.stack().value_counts().idxmax()
        #cast
    cast = grouped_data.loc[:, 'cast_1': 'cast_5']
    frequent_cast = cast.stack().value_counts().idxmax()
        #genres
    genres = grouped_data.loc[:, 'genres_1': 'genres_5']
    frequent_genres = genres.stack().value_counts().idxmax()
        #production companies
    production = grouped_data.loc[:, 'production_companies_1': 'production_companies_5']
    frequent_production = production.stack().value_counts().idxmax()
        #release_year
    release_year = grouped_data['release_year'].value_counts().idxmax()
    
    #average section
    avg_duration = grouped_data['runtime'].mean()
    avg_budget = grouped_data['budget_adj'].mean()
    avg_vote = grouped_data['vote_average'].mean()
    
    #creating nested dictionary
    movie_data[level] = {'avg_duration' : avg_duration, 
                         'frequent_director' : frequent_director, 
                         'avg_budget' : avg_budget, 
                         'avg_vote' : avg_vote,
                        'frequent_cast' : frequent_cast,
                        'frequent_genres' : frequent_genres,
                        'release_year' : release_year,
                        'frequent_production_companies' : frequent_production}


# In[27]:


#https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionaryuser_ids = []
#transforming nested dictionary into dataframe

movie_classes = []
frames = []

for movie_class, d in movie_data.items():
    movie_classes.append(movie_class)
    frames.append(pd.DataFrame.from_dict(d, orient='index'))
    
properties = pd.concat(frames, keys=movie_classes)  

properties.columns = ['values']
properties


# In[28]:


df_revenue.corr()


# ### Research Question 3:  Did movies with higher vote count received a better rating?

# In[29]:


#Slice DataFrame to get 2 columns 'vote_count' and 'vote_average'
df_vote = df.loc[:, 'vote_count' : 'vote_average']
#To compare results only entries are considered with more than 2000 votes
df_vote_2000 = df_vote[df_vote['vote_count'] > 2000]


# In[30]:


df_vote.plot(x='vote_count', y='vote_average', kind='scatter');
'''plot that describe the relation between votes and rates'''
df_vote_2000.plot(x='vote_count', y='vote_average', kind='scatter');
'''plot that describe the relation between more than 2000 votes and rates'''


# as we see the number of votes doesn't affect the rates.

# In[31]:


df_vote.corr()


# Correlation matrix finds the pairwise correlation between votes and rates 

# In[32]:


df_vote_2000.corr()


# Correlation matrix finds the pairwise correlation between more than 2000 votes and rates 

# and as we see there's no high correlation between votes and rates.

# ### Research Question 4:  What were the most popular produced genres in 2000 compared to 2015?

# In[33]:


#Creating a Mask for the release_year 2015
df_2015 = df_genres_dates[df_genres_dates['release_year'] == 2015].copy()
#drop release_year
df_2015.drop('release_year',axis=1, inplace=True)
#value_counts across columns
df_2015 = df_2015.stack().value_counts()


# In[34]:


#Creating a Mask for the release_year 2000
df_2000 = df_genres_dates[df_genres_dates['release_year'] == 2000].copy()
#drop release_year
df_2000.drop('release_year',axis=1, inplace=True)
#value_counts across columns
df_2000 = df_2000.stack().value_counts()


# In[35]:


#Comparing index of both dataframes
df_2015.index.sort_values(),df_2000.index.sort_values()

#Adjusting columns to have a match in columns
df_2000['Animation'] = 0
df_2000['Crime'] = 0
df_2000['History'] = 0
df_2000['Horror'] = 0
df_2000['Music'] = 0
df_2000['Western'] = 0

#Updating DataFrames, sort it by index
df_2015 = df_2015.sort_index()
df_2000 = df_2000.sort_index()


# In[36]:


'''Creating a plot with a bar chart with 2 bars'''
labels = df_2000.index.sort_values()
ind = np.arange(len(df_2015))  # the x locations for the groups
width = 0.35       # the width of the bars

# plot bars
red_bars = plt.bar(ind, df_2015, width, color='r', alpha=.7, label='2015')
white_bars = plt.bar(ind + width, df_2000, width, color='b', alpha=.7, label='2000')

# title and labels
plt.ylabel('Frequency')
plt.xlabel('Genre')
plt.title('Frequency of Genre in 2000 and 2015')
locations = ind + width / 2  # xtick locations
labels = labels # xtick labels
plt.xticks(locations, labels)
plt.rcParams["figure.figsize"] = (20,10)
# legend
plt.legend();


# ### Research Question 5:  How did the amount of produced films changed over time?

# In[37]:


amount_of_movies = [] #creates a list of tuples for amount of movies

#for loop to create amount_of_movies, years was previously defined
for year in years:
    d = df_genres_dates[df_genres_dates['release_year'] == year] #creates df filtered by every year mentioned in years
    e = len(d.index) #determines the number of rows 
    amount_of_movies.append((year, e)) #appends year with respective number of rows
    
#creates df for list of tuples amount_of_movies
df_amount_of_movies = pd.DataFrame(amount_of_movies, columns=['release_year', 'amount_of_mvies']).sort_values('release_year').reset_index().drop(['index'], axis=1)


# In[38]:


df_amount_of_movies.plot(x='release_year', y='amount_of_mvies', kind='line', figsize=(20,10), title="Amount of movies over years", label="Amount of movies", )
plt.xlabel('Year')
plt.ylabel('Amount');
df_amount_of_movies


# <a id='conclusions'></a>
# ## Conclusions
# 
# The first research question "Which genres are most popular from year to year?" has shown surprising results, as the most popular genre differed a lot. To the authors surprise, only in 11 occasions the most frequent produced genres was also voted as best genre by the users. In all remaining 40 occasions the two values differed.
# 
# The second research question "What kinds of properties are associated with movies that have high revenues?" shows interesting result. The numeric columns of "popularity, budget and vote_count" show the highest correlations. One can argue that movies with higher budgets are able to receive higher revenues, nevertheless, the correlation is not on a very high level. Vote_count is indicating that the more people vote for a movie, the higher the revenue is. Most probably, this is not a good indicator for high revenue movies. High revenue movies indicate that they are most commonly directed by Matt Damon, cast Tom Cruise as actor and contain the genre Action.
# 
# The third research question "Did movies with higher vote count received a better rating?" does not indicate that movies with a higher vote_count receive a higher vote_average. Also by considering columns with more than 2000 vote_count does not change the impression. Furthermore, the corralation does not indicate that higher vote counts result in higher vote averages. 
# 
# The forth research question "What were the most popular produced genres in 2000 compared to 2015?" indicate that in the year 2015 dramas were by far the most frequent produced movies, followed by thrillers and action. In 2000 the most frequent produced genre was thriller, followed by action and comedies. The bar chart indicates that in 2015 much more movies were produced compared to the year 2000. 
# 
# The fifth research question "How did the amount of produced films changed over time?" reveals that the amount of produced films significantly increased from 1960 to 2015. Up to 1983 not more than 100 movies were prodcued per year, while in 2014 700 movies were produced. A strong increase in movie production can be obsorved between 1997-2009. One has to consider that the line chart does not show accurate results, as many rows from the original dataset were dropped.
# 
# **All results are limited to the underlying data set and as no advaned statistics were performed, the results can only be treated as indicators and are not generalizable. Furthermore, one has to consider that many entries in the dataset have been removed due to missing data**
# 
# 

# In[ ]:




