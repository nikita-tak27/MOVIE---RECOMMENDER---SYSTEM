# 🎬 Movie Recommendation System

A Machine Learning-based Movie Recommendation System that suggests similar movies based on user preferences using **Content-Based Filtering**. The application provides an interactive interface built with **Streamlit** and displays official movie posters using the **TMDB API**, delivering a smooth and engaging user experience.

---

## ✨ Features

- 🎥 Recommends similar movies based on the selected movie.
- 🤖 Content-Based Recommendation using Machine Learning.
- 🖼️ Displays official movie posters using the TMDB API.
- 📊 Uses the TMDB 5000 Movies Dataset.
- ⚡ Interactive and user-friendly Streamlit interface.
- 🔍 Fast movie search and recommendation generation.
- 📱 Clean and responsive application design.

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Programming Language** | Python |
| **Framework** | Streamlit |
| **Machine Learning** | Content-Based Filtering, Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **API Integration** | TMDB (The Movie Database) API |
| **Data Serialization** | Pickle |
| **Dataset** | TMDB 5000 Movies Dataset, TMDB 5000 Credits Dataset |
| **Development Tools** | VS Code, Git, GitHub |

---

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── backend/
│   ├── app.py
│   ├── movie_dict.pkl
│   ├── requirements.txt
│
├── frontend/
│
├── preprocessing.py
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
└── README.md
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nikita-tak27/movie-Recommendation-System.git
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

---

## 📊 How It Works

1. Load the TMDB movie dataset.
2. Preprocess movie metadata.
3. Apply Content-Based Filtering to calculate movie similarity.
4. Recommend the most similar movies.
5. Fetch official movie posters using the TMDB API.
6. Display recommendations through the Streamlit web interface.



## ⚠️ Note

The large generated file `similarity.pkl` is not included in this repository because it exceeds GitHub's file size limit. It can be generated locally by running the preprocessing script.

---

## 🚀 Future Enhancements

- Collaborative Filtering based recommendations.
- Hybrid Recommendation System.
- Genre and language-based filtering.
- User authentication.
- Personalized recommendations.
- Real-time movie updates using live APIs.
- Improved recommendation accuracy.

---

## 👩‍💻 Developed By

**Nikita Tak**

- B.Tech (Information Technology)
- Machine Learning & Python Developer
- Passionate about AI, Full Stack Development, and Data Science




 
