🎬 Movie Recommender System 
A content-based movie recommendation web app built with Python and Streamlit. It suggests 10
movies similar to the one you select, complete with poster images fetched live from The Movie
Database (TMDB) API.

💻 How It Works:
1. Precomputed data — A dataset of movies and a precomputed similarity matrix are loaded
from pickle files ( model/movie_list.pkl and model/similarity.pkl ). The similarity
matrix is typically built using techniques like cosine similarity over vectorized movie metadata
(e.g., genres, cast, crew, keywords, overview).
2. Movie selection — The user picks a movie from a dropdown (populated with all movie titles
in the dataset).
3. Recommendation logic — When “Show Recommendation” is clicked, the app:
Finds the index of the selected movie.
Looks up its similarity scores against every other movie.
Sorts movies by similarity and picks the top 5 closest matches (excluding the movie
itself).
4. Poster retrieval — For each recommended movie, the app calls the TMDB API using the
movie’s ID to fetch its poster image URL.
5. Display — The 5 recommended movies are shown side-by-side, each with its title and poster.

👩‍💻 Tech Stack:
🐍 Python
🕸 Streamlit — web app UI
🐼 Pandas / Pickle — for loading the preprocessed movie data and similarity matrix
🫂 Requests — for calling the TMDB API
🧗‍♂️ TMDB API — for fetching movie posters

🏛 Project Structure:
├── app.py # Main Streamlit application
├── model/
│ ├── movie_list.pkl # Preprocessed movie dataset
│ └── similarity.pkl # Precomputed similarity matrix

👊 Getting Started:
Prerequisites
Python 3.7+
pip
Installation
Run the app
The app will open in your browser at http://localhost:8501 .

🖍 Usage
1. Select or type a movie title from the dropdown.
2. Click “Show Recommendation”.
3. View 5 similar movies along with their posters.
   
🗒 Notes:
This project uses TMDB’s API to fetch movie posters — an active internet connection is
required.
st.beta_columns is deprecated in newer Streamlit versions; consider updating it to
st.columns for compatibility with recent Streamlit releases.
The API key in app.py is currently hardcoded — for production use, move it to an
environment variable or Streamlit secrets file instead of committing it to the repository.

🏌️‍♀️ Future Improvements
Add movie overview/description on hover or click.
Add genre-based filtering.
Deploy the app (e.g., Streamlit Community Cloud, Heroku, or Docker).
Add a search/autocomplete-friendly UI.
🧩 License
This project is open-source. Feel free to use, modify, and distribute it.
