import pickle
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"


@st.cache_resource(show_spinner=False)
def load_data():
    movies = pickle.load(open("model/movie_list.pkl", "rb"))
    top_k = pickle.load(open("model/similarity_topk.pkl", "rb"))
    return movies, top_k


def recommend(movie, movies, top_k):
    index = movies[movies["title"] == movie].index[0]
    neighbors = top_k[index][:10]

    names, posters = [], []
    for neighbor_index, _score in neighbors:
        movie_id = movies.iloc[neighbor_index].movie_id
        names.append(movies.iloc[neighbor_index].title)
        posters.append(fetch_poster(movie_id))
    return names, posters


st.header("🎬 Movie Recommender System")

movies, top_k = load_data()
movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    with st.spinner("Finding movies you'll like..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, top_k)

    cols = st.columns(5)
    for i in range(min(5, len(recommended_movie_names))):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

    if len(recommended_movie_names) > 5:
        cols2 = st.columns(5)
        for i in range(5, min(10, len(recommended_movie_names))):
            with cols2[i - 5]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
