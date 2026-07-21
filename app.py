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


@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    """Fetch title, genres and overview."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5).json()
        genres = [g["name"] for g in data.get("genres", [])]
        return {
            "title": data.get("title", ""),
            "genres": genres,
            "overview": data.get("overview", "No overview available."),
        }
    except Exception:
        return {"title": "", "genres": [], "overview": "No overview available."}


@st.cache_data(show_spinner=False)
def fetch_credits(movie_id):
    """Fetch top 3 cast (with character names) and the director."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5).json()
        cast_list = data.get("cast", [])[:3]
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
    # top-k neighbors: dict {movie_index: [(neighbor_index, score), ...]}
    top_k = pickle.load(open("model/similarity_topk.pkl", "rb"))
    return movies, top_k


st.header("🎬 Movie Recommender System")

movies, top_k = load_data()
movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    with st.spinner("Finding movies you'll like..."):
        index = movies[movies["title"] == selected_movie].index[0]
        neighbors = top_k[index][:10]
        recommended_movie_ids = [movies.iloc[n].movie_id for n, _ in neighbors]
        recommended_movie_names = [movies.iloc[n].title for n, _ in neighbors]
        recommended_movie_posters = [fetch_poster(mid) for mid in recommended_movie_ids]

    # store recommendations in session_state so the "Details" buttons
    # keep working even after Streamlit reruns the script on click
    st.session_state["rec_ids"] = recommended_movie_ids
    st.session_state["rec_names"] = recommended_movie_names
    st.session_state["rec_posters"] = recommended_movie_posters

# Only show the grid + details if we have recommendations stored
if "rec_ids" in st.session_state:
    rec_ids = st.session_state["rec_ids"]
    rec_names = st.session_state["rec_names"]
    rec_posters = st.session_state["rec_posters"]

    def render_row(start, end):
        cols = st.columns(end - start)
        for col, i in zip(cols, range(start, end)):
            with col:
                st.text(rec_names[i])
                st.image(rec_posters[i])
                if st.button("ℹ️ Details", key=f"detail_{rec_ids[i]}"):
                    st.session_state["selected_movie_id"] = rec_ids[i]
                    st.session_state["selected_movie_title"] = rec_names[i]

    render_row(0, min(5, len(rec_names)))
    if len(rec_names) > 5:
        render_row(5, min(10, len(rec_names)))

    # Show details panel if a movie was clicked
    if "selected_movie_id" in st.session_state:
        st.divider()
        movie_id = st.session_state["selected_movie_id"]
        with st.spinner("Loading movie details..."):
            details = fetch_movie_details(movie_id)
            credits = fetch_credits(movie_id)

        st.subheader(f"🎬 {details['title'] or st.session_state['selected_movie_title']}")

        if details["genres"]:
            st.markdown("**Genre:** " + ", ".join(details["genres"]))

        if credits["cast"]:
            cast_lines = [
                f"- **{c['actor']}** as *{c['character']}*"
                for c in credits["cast"] if c["actor"]
            ]
            st.markdown("**Cast:**")
            st.markdown("\n".join(cast_lines))

        st.markdown(f"**Director:** {credits['director']}")

        st.markdown("**Overview:**")
        st.write(details["overview"])
