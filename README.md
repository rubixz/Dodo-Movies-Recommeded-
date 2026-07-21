    # 🎬 Dodo Movies Recommender

*Not sure what to watch tonight? Let Dodo figure it out for you.* 🍿

Pick any movie you love, and this little app digs through thousands of films to find 10 others you'll probably fall for too — genre, plot, cast, and director all taken into account. Posters included, because a recommendation without a poster is just a suggestion. 😄

---

## ✨ What it does
- 🔍 Type or select a movie from the dropdown
- 🧠 The app finds movies most *similar* to it using content-based filtering (genres + keywords + cast + crew + plot)
- 🖼️ Get 10 recommendations, complete with posters, pulled live from **TMDB**

## 🛠️ Built with
- **Python** 🐍
- **Streamlit** — for the clean, interactive web UI
- **Scikit-learn** — cosine similarity to find "movies like this one"
- **Pandas** — for wrangling the data
- **TMDB API** — for fetching those lovely posters

## 🚀 Try it live
👉 [Launch the app](https://dodo-movies-recommeded-git-cwwpurusvv7y3qn5tykh8h.streamlit.app/)

## 💻 Run it yourself
```bash
git clone https://github.com/rubixz/Dodo-Movies-Recommeded-.git
cd Dodo-Movies-Recommeded-
pip install -r requirements.txt
streamlit run app.py
```

## 📊 The data
Built on the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — ~5,000 movies, tagged and vectorized so similar films naturally cluster together.

## 🙌 A note
This is a project made for learning and fun — think of Dodo as that one friend who's watched *everything* and always has a decent suggestion. 🦤🎥

---
Made with ☕ and a mild movie obsession.

    
