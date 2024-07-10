# -*- coding: utf-8 -*-
"""MovieRecommendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f7XUaZp4c40qRFKzYvadlCZANfCXaFTL
"""

import numpy as np
import pandas as pd
import ast

movies=pd.read_csv('/content/tmdb_5000_movies.csv')
credits=pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head(1)

credits.head(1)

#merging the datasets
movies=movies.merge(credits,on='title')

movies.head(1)

#eliminating coloumns which arent in use.
#genres
#id
#keywords
#title
#overview
#cast
#crew this all kept others are removed
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

#check for missing data
movies.isnull().sum()

movies.dropna(inplace=True)

#check for duplicate data
movies.duplicated().sum()

movies.iloc[0].genres

# We will now convert this data into the form like
# [Action,Adventure,Fantasy,Sci-fi]
#We will use a helper function which runs as a loop in the genres and find values from the "name:"
#THe ast module in python has a function called literal_eval which convert the string of list into a list.
def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

convert('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

#now change the movies genres coloumn into the updates one
movies['genres']=movies['genres'].apply(convert)

movies.head()

#now apply same function on the keywords coloumn on the movies dataset
movies['keywords']=movies['keywords'].apply(convert)

movies.head()

#now we have to repeat the same thing in the cast coloumn but we only need the first 3 names of each row of the coloumn cast.
def conver3(obj):
  L=[]
  counter=0                               #initialize a variable with 0
  for i in ast.literal_eval(obj):
    if counter!=3:                        #it will run upto 3 names found on the cast coloumn.
      L.append(i['name'])
      counter+=1
    else:
      break
  return L

movies['cast']=movies['cast'].apply(conver3)

movies.head()

#now we have to create a function for the crew coloumn which will find te director name only for each movie.
def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      L.append(i['name'])
      break
  return L

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

#as our overview coloumn is a string we have to apply a lambda function which will convert the string into a list.
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

#now we will remove any spaces which lies in between two words, like in the genres coloumn "Science Fiction" will converted into "ScienceFiction"
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])   #a lambda function is used which removed the spaces in between.

#similarly we will do this for keywords,cast,crew also.
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

# Now we will concatenate the overview ,genres,keywords,cast,crew into a new coloumn called tags.
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

#Now we will create a new dataframe which will only have movie id ,title and tags coloumn
new_df=movies[['movie_id','title','tags']]

new_df.head()

#NOW WE HAVE TO CONVERT THE TAGS COLUMN INTO A STRING
new_df['tags']=new_df['tags'].apply(lambda x:"".join(x))

new_df.head()

#now convert the tags column into lowercase
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

new_df.head()

#now we can use stemming to eliminate the same type of words like activities and activity \
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

#now we create a helper function which will stem all the words
def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

#apply this on new_df tags
new_df['tags']=new_df['tags'].apply(stem)

#now we will use text vectorization , through which if a person select one movie that is a vector , the nearest vector  to that vector is to be recommended .
#There are different types of method in text vectorization , We will use the method bag of words.

#Now use sklearn
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

vectors[0]

cv.get_feature_names_out()

#we use stemming process
#examples
ps.stem('dancing')

stem('now we will use text vectorization , through which if a person select one movie that is a vector')

#now as all movies are vectors , so we have to calculate the distance between the movies
#higher the distance lower the similarity
#we will calculate the cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
similar=cosine_similarity(vectors)
similar[1]

#Here we have sorted the data on basis of similarity having the index constand
sorted(list(enumerate(similar[5])),reverse=True,key=lambda x:x[1])[1:6]

#Now we need to create a function , where we provide a movie a movie name and it will give 5 similar movies.
def recommend(movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances=similar[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movies_list:
    print(new_df.iloc[i[0]].title)

recommend('Clay Pigeons')

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))

pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))

pickle.dump(similar,open('similarity.pkl','wb'))