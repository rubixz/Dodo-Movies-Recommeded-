import pickle
import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- TMDB API Key ---
TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")

# --- Custom CSS for Styling, Button Alignment & Blur Effect ---
CUSTOM_CSS = """
/* Background blur for popup modal */
div[data-modal-container="true"] {
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

/* Center align content and buttons nicely under the poster */
.movie-card-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 20px;
}
"""
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

# --- Helper Functions (Cached) ---
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

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5).json()
        genres = [g["name"] for g in data.get("genres", [])]
        return {
            "title": data.get("title", ""),
            "genres": genres,
            "overview": data.get("overview", "No overview available.")
        }
    except Exception:
        return {"title": "", "genres": [], "overview": "No overview available."}

@st.cache_data(show_spinner=False)
def fetch_credits(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5).json()
        cast_list = data.get("cast", [])[:4]
        cast = [{"actor": c.get("name"), "character": c.get("character")} for c in cast_list]

        director = "Unknown"
        for member in data.get("crew", []):
            if member.get("job") == "Director":
                director = member.get("name")
                break
        return {"cast": cast, "director": director}
    except Exception:
        return {"cast": [], "director": "Unknown"}

@st.cache_resource(show_spinner=False)
def load_data():
    movies = pickle.load(open("model/movie_list.pkl", "rb"))
    top_k = pickle.load(open("model/similarity_topk.pkl", "rb"))
    return movies, top_k

# --- Netflix Style Popup Dialog (Compact Size & Custom Order Flow) ---
@st.dialog("🎬 Movie Details", width="medium") # width ko 'medium' kiya taaki size chota rahe
def show_movie_popup(movie_id, movie_title):
    with st.spinner("Loading details..."):
        details = fetch_movie_details(movie_id)
        credits = fetch_credits(movie_id)
        poster_url = fetch_poster(movie_id)

    # Layout: Left (Poster) | Right (Details following your custom flow)
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(poster_url, use_container_width=True)

    with col2:
        # 1. Title
        st.subheader(details["title"] or movie_title)

        # 2. Genre
        if details["genres"]:
            st.markdown(f"**Genre:** {', '.join(details['genres'])}")

        st.markdown("---")        

        # 3. Cast
        if credits["cast"]:
            st.markdown("**Cast:**")
            cast_lines = [f"- {c['actor']} as *{c['character']}*" for c in credits["cast"] if c["actor"]]
            st.markdown("\n".join(cast_lines))

        st.markdown("---")

        # 4. Director
        st.markdown(f"**Director:** {credits['director']}")

        # 5. Overview (Sabse aakhir mein cast ke baad)
        st.markdown("**Overview:**")
        st.write(details["overview"])


# --- Main App UI ---
st.header("🎬 Movie Recommender System")

movies, top_k = load_data()
movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    with st.spinner("Finding movies you'll like..."):
        try:
            index = movies[movies["title"] == selected_movie].index[0]
            neighbors = top_k[index][:10]
            recommended_movie_ids = [movies.iloc[n].movie_id for n, _ in neighbors]
            recommended_movie_names = [movies.iloc[n].title for n, _ in neighbors]
            recommended_movie_posters = [fetch_poster(mid) for mid in recommended_movie_ids]

            st.session_state["rec_ids"] = recommended_movie_ids
            st.session_state["rec_names"] = recommended_movie_names
            st.session_state["rec_posters"] = recommended_movie_posters
        except IndexError:
            st.error("Movie not found in database.")

# Render grid if recommendations exist
if "rec_ids" in st.session_state:
    rec_ids = st.session_state["rec_ids"]
    rec_names = st.session_state["rec_names"]
    rec_posters = st.session_state["rec_posters"]

    def render_row(start, end):
        cols = st.columns(5)
        for col, i in zip(cols, range(start, end)):
            with col:
                # Poster
                st.image(rec_posters[i], use_container_width=True)
                
                # Title 
                st.markdown(
                    f"<p style='text-align: center; font-weight: 600; font-size: 0.95rem; margin-bottom: 5px; height: 40px; display: flex; align-items: center; justify-content: center;'>{rec_names[i]}</p>", 
                    unsafe_allow_html=True
                )
                
                # Details Button 
                if st.button("ℹ️ Details", key=f"detail_{rec_ids[i]}", use_container_width=True):
                    show_movie_popup(rec_ids[i], rec_names[i])

    st.subheader("Recommendations For You:")
    render_row(0, min(5, len(rec_names)))
    if len(rec_names) > 5:
        render_row(5, min(10, len(rec_names)))
