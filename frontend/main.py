
import streamlit as st
import requests

# 1. Page Config and Corporate Layout Setup
st.set_page_config(
    page_title="StreamFlix | Premium Recommendation Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend URL Setup
BACKEND_URL = "http://127.0.0.1:8000"

# 2. Premium Dark Red Theme CSS (Bina hover ke sab saaf dikhega)
st.markdown("""
    <style>
    .stApp {
        background-color: #141414 !important;
        color: #ffffff !important;
    }
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #E50914 !important;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .sub-title {
        text-align: center;
        color: #cccccc !important;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    /* Cards default visible block style */
    .movie-card {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        margin-bottom: 20px;
        background-color: #1f1f1f !important;
        border: 1px solid #2d2d2d;
        transition: transform .3s ease, border-color .3s ease;
    }
    .movie-card:hover {
        transform: scale(1.04);
        border-color: #E50914;
    }
    .movie-title {
        color: #ffffff !important;
        text-align: center;
        padding: 12px 8px;
        font-size: 14px;
        font-weight: 600;
        background-color: #1f1f1f;
    }
    /* Custom Red Accent Button styling */
    div.stButton > button:first-child {
        background-color: #E50914 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 4px !important;
        width: 100%;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #b80710 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">STREAMFLIX</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Hybrid Predictive Recommendation Engine Platform</div>', unsafe_allow_html=True)

# 3. TMDB Se Original Poster Fetch Karne Ka Function
def fetch_poster_from_tmdb(movie_id):
    api_keys = [
        "c7ec19ffdd327cd115422e786116674",
        "8265bd1679663a7ea12ac168da84d2e8",
        "a533b1a43a8b25d0458df589b25d0fcb"
    ]
    
    # Header add kiya hai taaki request 'bot' na lage, balki 'browser' jaisi lage
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for key in api_keys:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US"
            # Timeout 4 se badha kar 8 kar diya, kyuki server slow ho sakta hai
            response = requests.get(url, timeout=8, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    # Yahan slash check add kiya hai taaki path sahi bane
                    return f"https://image.tmdb.org/t/p/w500/{poster_path.lstrip('/')}"
        except Exception:
            continue
            
    # Agar ab bhi nahi aaya, toh return None karein (taaki hum UI mein handle kar sakein)
    return None
# 4. Backend Se Saari Movies Pool Load Karne Ka Function
@st.cache_data
def load_movie_pool():
    try:
        response = requests.get(f"{BACKEND_URL}/movies", timeout=5)
        if response.status_code == 200:
            return response.json().get("movies", [])
    except Exception:
        pass
    return ["Avatar", "Spider-Man 3", "Spectre", "John Carter"]

movie_list = load_movie_pool()

# Dropdown UI
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    selected_movie = st.selectbox(
        "🔍 Search or Select a Movie:",
        movie_list,
        index=0
    )
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_btn = st.button("Generate AI Recommendations")

# 5. Presentation Grid Render Layer
if recommend_btn:
    with st.spinner("Analyzing tags and semantic vectors..."):
        try:
            res = requests.get(f"{BACKEND_URL}/recommend", params={"movie": selected_movie}, timeout=5)
            if res.status_code == 200:
                recommendations = res.json().get("recommendations", [])
                
                if recommendations:
                    st.markdown("<h3 style='color: #fff; margin-top: 2rem; margin-bottom: 1.5rem;'>Trending Recommendations for You:</h3>", unsafe_allow_html=True)
                    
                    cols = st.columns(5)
                    for index, item in enumerate(recommendations[:5]):
                        with cols[index]:
                            movie_title = item.get('title', 'Unknown Movie')
                            real_movie_id = item.get('movie_id')
                            
                            # Original Poster Fetch Call
                            poster_url = fetch_poster_from_tmdb(real_movie_id)

                            if poster_url:
                                st.markdown(f'''
                                    <div class="movie-card">
                                        <img src="{poster_url}" style="width: 100%; border-radius: 8px;">
                                        <div class="movie-title">{movie_title}</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            else:
                                # Agar poster nahi mila to text dikhao, image mat dikhao
                                st.markdown(f'<div class="movie-card"><p style="padding:12px; text-align:center; color:#ccc;">Poster Not Available</p></div>', unsafe_allow_html=True)
                else:
                    st.warning("No recommendations found.")
            else:
                st.error("Backend error. Please try again.")
        except Exception as e:
            st.error("Could not connect to backend. Make sure app.py is running.")