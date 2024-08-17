import pickle
import requests
import streamlit as st

# Replace with your OMDb API key
omdb_api_key = "8408d5e0"  # Corrected to only include the API key

def fetch_poster(movie_title):
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey={omdb_api_key}"  # Changed to HTTPS
    response = requests.get(url)
    data = response.json()
    
    # Debug: Print the API response to check if it's correct
    print(f"API response for {movie_title}: {data}")
    
    # Check if the poster URL exists
    if 'Poster' in data and data['Poster'] != "N/A":
        return data['Poster']
    else:
        return "https://via.placeholder.com/500x750?text=Poster+Not+Available"  # Placeholder if no poster is found

# Load your movie list and similarity data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

# Test fetching posters to verify they work
imageUrls = [
    fetch_poster("The Godfather"),
    fetch_poster("Avengers: Infinity War"),
    fetch_poster("Inception"),
    fetch_poster("The Dark Knight"),
    fetch_poster("Spider-Man: Into the Spider-Verse"),
]

# Display the posters to check if they are working
for imageUrl in imageUrls:
    st.image(imageUrl)  # You should see the test images here

# Select movie from dropdown
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

if st.button("Show Recommend"):
    movie_names, movie_posters = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_names[0])
        st.image(movie_posters[0])
    with col2:
        st.text(movie_names[1])
        st.image(movie_posters[1])
    with col3:
        st.text(movie_names[2])
        st.image(movie_posters[2])
    with col4:
        st.text(movie_names[3])
        st.image(movie_posters[3])
    with col5:
        st.text(movie_names[4])
        st.image(movie_posters[4])
