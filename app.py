import streamlit as st
import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import requests

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Set page config
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# TMDB API Configuration
TMDB_API_KEY = "YOUR_API_KEY"  # Replace with your TMDB API key
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Title and description
st.title("🎬 Movie Recommender System")
st.write("Find similar movies based on your favorite films!")

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url).json()
        poster_path = data['poster_path']
        if poster_path:
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        return None
    except:
        return None

# Load and process data
@st.cache_data
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    
    # Merge on title
    movies = movies.merge(credits, on='title')
    
    # Select required columns
    movies = movies[['movie_id','genres','title','id','keywords','overview','cast','crew']]
    
    # Drop null values
    movies.dropna(inplace=True)
    
    # Convert JSON-like strings to lists of names
    def convert(obj):
        list = []
        for i in ast.literal_eval(obj):
            list.append(i['name'])
        return list

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    # Convert cast: top 3 actors
    def convert3(obj):
        list = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter != 3:
                list.append(i['name'])
                counter += 1
            else:
                break
        return list

    movies['cast'] = movies['cast'].apply(convert3)

    # Fetch director
    def fetch_director(obj):
        list = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                list.append(i['name'])
                break
        return list

    movies['crew'] = movies['crew'].apply(fetch_director)

    # Process overview
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # Remove spaces in tags
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])

    # Create tags
    movies['tag'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords']

    # New dataframe
    new_movies = movies[['movie_id','title','tag']]
    new_movies['tag'] = new_movies['tag'].apply(lambda x: " ".join(x))
    new_movies['tag'] = new_movies['tag'].apply(lambda x: x.lower())

    # Stemming
    ps = PorterStemmer()
    def stem(text):
        y = []
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)

    new_movies['tag'] = new_movies['tag'].apply(stem)

    # Vectorization
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new_movies['tag']).toarray()

    # Similarity Matrix
    similarity = cosine_similarity(vector)
    
    return new_movies, similarity, movies

# Load data
new_movies, similarity, movies = load_data()

# Create a search box with autocomplete
movie_list = new_movies['title'].tolist()
selected_movie = st.selectbox(
    "Search or select a movie:",
    [""] + movie_list,  # Add empty string as first option
    index=0  # Select empty string by default
)

# Recommendation function
def recommend(movie):
    movie = movie.lower()
    titles = new_movies['title'].str.lower()
    if movie not in titles.values:
        st.error(f"'{movie}' not found in the dataset.")
        return [], []
    movie_index = titles[titles == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Get recommendations
if st.button("Get Recommendations"):
    if selected_movie:
        recommendations, posters = recommend(selected_movie)
        
        if recommendations:
            st.subheader("Recommended Movies:")
            
            # Create columns for movie posters and titles
            cols = st.columns(5)
            for i in range(len(recommendations)):
                with cols[i]:
                    if posters[i]:
                        st.image(posters[i], use_column_width=True)
                    st.write(f"{i+1}. {recommendations[i]}")
    else:
        st.warning("Please select a movie first!")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 