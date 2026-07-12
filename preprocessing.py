
import numpy as np
import pandas as pd

print("1. Files load ho rhi hain...")
# Step 1: Dono files ko read karna
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

print("2. Files ko merge kiya ja rha hai...")
# Step 2: Dono ko jodna
movies = movies.merge(credits, on='title')

print("3. Faltu columns hataye ja rhe hain...")
# Step 3: Kaam ke columns select karna
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

print("4. Missing values clean ho rhi hain...")
# Step 4: Missing data hatana
movies.dropna(inplace=True)
import ast

# Yeh function genres aur keywords me se 'name' nikalega
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
print("\n5. Columns ko format kiya ja rha hai...")

# Genres aur Keywords ko list me convert kar rahe hain
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Check karne ke liye ki kaisa dikh rha hai
print(movies[['title', 'genres', 'keywords']].head(4))
    


# Final check ke liye print
print("\nSuccess! Humara data ready hai. Shape of data:", movies.shape)
print(movies.head(4))
import ast

# 1. Yeh function har movie se top 3 main actors ke naam nikalega
def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

print("\n6. Cast se top 3 actors nikale ja rhe hain...")
movies['cast'] = movies['cast'].apply(convert3)


# 2. Yeh function poori crew mein se sirf 'Director' ka naam dhoondega
def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break  # Ek director milte hi loop rok denge
    return L

print("7. Crew se director ka naam nikala ja rha hai...")
movies['crew'] = movies['crew'].apply(fetch_director)


# 3. Final check karne ke liye ki ab charo columns kaise dikh rhe hain
print("\n--- HAR COLUMN KI CLEAN LIST TAIYAR HAI ---")
print(movies[['title', 'genres', 'keywords', 'cast', 'crew']].head(2))
print("\n8. Names aur words ke beech se spaces hataye ja rhe hain...")

# Har list ke andar se spaces gayab karna
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Check karne ke liye print
print(movies[['title', 'genres', 'keywords', 'cast', 'crew']].head(2))
print("\n9. Saare columns ko jodkar 'tags' column banaya ja rha hai...")

# Overview ko string se list me convert karna
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Saare columns ko merge karke ek bada 'tags' column banana
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
# Sirf kaam ke 3 columns select karna
new_df = movies[['movie_id', 'title', 'tags']]

# Tags ki list ko wapas paragraph (string) banana
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Saare words ko lowercase me convert karna
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# Helper function jo har word ko uske root word me badlega
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

print("\n9.5 Words ki stemming ki ja rha hai...")
new_df['tags'] = new_df['tags'].apply(stem)

print("\n--- DETAILED FINAL DATASET READY ---")
print(new_df.head(2))
from sklearn.feature_extraction.text import CountVectorizer

print("\n10. Text ko vectors (numbers) me badla ja rha hai...")

# CountVectorizer ka object banana, jo stop_words (and, to, is, the) ko khud hata dega
cv = CountVectorizer(max_features=5000, stop_words='english')

# Tags ko numbers me convert karna aur numpy array banana
vectors = cv.fit_transform(new_df['tags']).toarray()

# Check karne ke liye vectors ka shape print karte hain
print("Vectors ka shape hai:", vectors.shape)
from sklearn.metrics.pairwise import cosine_similarity

print("\n11. Movies ke beech ki Cosine Similarity nikaali ja rha hai...")

# Har movie ka baaki saari movies ke sath similarity score matrix banana
similarity = cosine_similarity(vectors)

# Check karne ke liye similarity matrix ka shape print karte hain
print("Similarity matrix ka shape hai:", similarity.shape)
# Yeh hamara main recommendation function hai
def recommend(movie):
    # 1. Movie ka index nikalna
    movie_index = new_df[new_df['title'] == movie].index[0]
    
    # 2. Similarity scores nikalna aur index ke sath bind karna (enumerate)
    distances = similarity[movie_index]
    
    # 3. Scores ke basis par sort karna aur top 5 nikalna
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    print(f"\n--- Movies recommended for '{movie}': ---")
    # 4. Top 5 movies ke naam print karna
    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# --- TESTING OUR MODEL ---
# Chaliye check karte hain ki model kaam kar rha hai ya nahi
recommend('Avatar')
import pickle

print("\n[VITAL] Exporting fresh pickle structures with true movie_id tags...")

# Strict dict conversion keeping dataframe columns intact
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("\n🎉 MUBARAK HO! Saari files safely export ho gayi hain.")

