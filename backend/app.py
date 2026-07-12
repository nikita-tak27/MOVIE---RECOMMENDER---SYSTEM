
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import uvicorn
import os

app = FastAPI(title="StreamFlix Enterprise API", version="1.0.0")

# CORS setup for smooth communication between Streamlit and FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust Path Resolution for pickle files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

def get_valid_path(filename):
    path_backend = os.path.join(BACKEND_DIR, filename)
    path_root = os.path.join(BASE_DIR, filename)
    if os.path.exists(path_backend):
        return path_backend
    elif os.path.exists(path_root):
        return path_root
    raise FileNotFoundError(f"Missing data resource: {filename}")

try:
    movies_dict = pickle.load(open(get_valid_path('movie_dict.pkl'), 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(get_valid_path('similarity.pkl'), 'rb'))
    print("✅ System Core Loaded: pkl vectors mapped successfully!")
except Exception as e:
    print(f"❌ System Init Failed: {str(e)}")

@app.get("/")
def check_health():
    return {"status": "Online", "engine": "FastAPI Core Ready"}

@app.get("/movies")
def list_movies():
    return {"movies": movies['title'].tolist()}

@app.get("/recommend")
def get_ai_recommendations(movie: str):
    if movie not in movies['title'].values:
        raise HTTPException(status_code=404, detail="Movie not found in database.")
        
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # Extract top 5 recommended movie items
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_pool = []
    for i in movies_list:
        # CRITICAL FIXED LINE: Passing actual TMDB database ID string/int instead of matrix index
        actual_movie_id = int(movies.iloc[i[0]]['movie_id'])
        
        recommended_pool.append({
            "movie_id": actual_movie_id,
            "title": str(movies.iloc[i[0]]['title'])
        })
        
    return {"source": movie, "recommendations": recommended_pool}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)