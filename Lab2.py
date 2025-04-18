import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack

# Med hjälp av chat gpt
def load_data():
    # Läs in datan
    movies = pd.read_csv("movies.csv", index_col=0)
    tags = pd.read_csv("tags.csv", index_col=0)

    # Dela upp genrer som är separerade med "|" till listor
    movies["genres"] = movies["genres"].fillna("").str.split("|")

    # Omvandla genrer till binär one-hot encoding
    mlb = MultiLabelBinarizer()
    genre_encoding = pd.DataFrame(mlb.fit_transform(movies["genres"]), columns=mlb.classes_)
    movies = movies.join(genre_encoding)

    # Se till att alla taggar är strängar
    tags["tag"] = tags["tag"].astype(str)

    # Slå ihop alla taggar för samma film till en sträng
    combined_tags = tags.groupby("movieId")["tag"].apply(" ".join).reset_index()

    # Räkna hur många taggar varje film har
    combined_tags["tag_count"] = combined_tags["tag"].apply(lambda x: len(x.split()))

    # Ta bort filmer med färre än 3 taggar
    filtered_tags = combined_tags[combined_tags["tag_count"] >= 3]

    # Slå ihop taggar med film datan
    movies = movies.merge(filtered_tags[["movieId", "tag"]], on="movieId", how="left")

    # Fyll i tomma taggar med en tom sträng istället för NaN värde
    movies["tag"] = movies["tag"].fillna("")

    return movies

def compute_similarity(movies):
    # Skapa en TF-IDF-vektorisering av taggarna och ta bort vanliga ord samt begränsa till de 10 000 vanligaste orden
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10_000)
    tfidf_matrix = vectorizer.fit_transform(movies["tag"])

    # Extrahera genre kolumnerna
    genre_matrix = movies.iloc[:, 3:-1].fillna(0).values.astype(np.float32)

    # Vikta upp genre dubbelt för bättre resultat av rekommendationer
    genre_matrix *= 2

    # Kombinera genre och taggar till en gemensam matris
    final_matrix = hstack((genre_matrix, tfidf_matrix))

    # Beräkna likheten mellan alla filmer
    return cosine_similarity(final_matrix, dense_output=False)

# Returnerar 5 rekommenderade filmer baserat på likhet i genrer och taggar
def recommend_movies(movie_title, movies, cosine_sim, num_recommendations=5):
    # Om titeln inte finns i datasetet, returnera felmeddelande
    if movie_title not in movies["title"].values:
        return f"Filmen '{movie_title}' finns inte med."

    # Hämta index för den givna filmen
    idx = movies.index[movies["title"] == movie_title][0]

    # Hämta genrer för filmen
    movie_genres = set(movies.iloc[idx]["genres"])

    # Hämta similarity score mellan filmen och alla andra
    sim_scores = list(enumerate(cosine_sim[idx].toarray()[0]))

    # Sortera filmerna efter högst likhet men ta inte med den första angivna filmen
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]

    # Lista för att lagra rekommendationer med delade genrer
    filtered_recommendations = []

    # Gå igenom filmerna och kolla om de delar någon genre
    for movie_idx, score in sim_scores:
        recommended_genres = set(movies.iloc[movie_idx]["genres"])
        # Kolla om det finns någon gemensam genre
        if movie_genres & recommended_genres:
            filtered_recommendations.append((movie_idx, score))
        # Avsluta om antal rekommendationer nåtts
        if len(filtered_recommendations) == num_recommendations:
            break

    # Visa de rekommenderade filmerna och lägg till similarity score
    recommendations = movies.iloc[[i[0] for i in filtered_recommendations]][["title", "genres", "tag"]].copy()
    recommendations["similarity_score"] = [i[1] for i in filtered_recommendations]

    return recommendations