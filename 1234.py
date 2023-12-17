import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch movie poster URL
def fetch_poster(movie_id):
    base_url = 'https://image.tmdb.org/t/p/original/'
    api_key = '8283ed0ee54dc646bb51b790d956e82f'  # Replace YOUR_API_KEY with your actual API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    
    try:
        data = requests.get(url).json()
        poster_path = data['poster_path']
        full_path = base_url + poster_path
        return full_path
    except Exception as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return None

# Function to recommend movies based on selected movie
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies.append({'name': movies.iloc[i[0]].title, 'poster': poster_url})
    
    return recommended_movies

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app logic with custom styles
st.title('Movie Matchmaker')
st.markdown(
    """
           <style>
        body {
            background-color: #333333;
            color: #ffffff;
        }
        #cover-container {
            text-align: center;
            max-width: 600px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: #1e1e1e;
            margin: 20px auto;
        }
        h1 {
            font-family: 'Limelight', cursive;
            font-size: 42px;
            color: #ff9e80;
            margin-bottom: 20px;
        }
        p {
            margin-bottom: 20px;
        }
        #movie-doodle {
            width: 100px;
            margin-bottom: 20px;
        }
        #start-matching-btn {
            background-color: #ff9e80;
            color: #1e1e1e;
            padding: 14px 28px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s ease;
        }
        #start-matching-btn:hover {
            background-color: #ff7043;
        }
        .recommendation-container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .movie-card {
            background-color: #2c2c2c;
            color: #ffffff;
            padding: 10px;
            margin: 10px;
            border-radius: 8px;
            width: 100px;
            height: auto;
            text-align: center;
        }
    </style>
           """,
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendations'):
    recommended_movies = recommend(selected_movie)
    
    for movie in recommended_movies:
        st.text(movie['name'])
        st.image(movie['poster'], caption=movie['name'], use_column_width=True)
