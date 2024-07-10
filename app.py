import pandas as pd
import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    for i in movies_list:
        movie_id = i[0]
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')
selected_moviename =st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)
if st.button('RECOMMEND'):
    recommendation = recommend(selected_moviename)
    for i in recommendation:
        st.write(i)
