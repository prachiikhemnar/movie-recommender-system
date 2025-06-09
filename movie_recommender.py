import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load and preprocess data
df = pd.read_csv('movies.csv')
df['genres'] = df['genres'].fillna('')
df['keywords'] = df['keywords'].fillna('')
df['overview'] = df['overview'].fillna('')
df['combined_features'] = df['genres'] + ' ' + df['keywords'] + ' ' + df['overview']

# Content-based filtering
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(movie_id, cosine_sim=cosine_sim):
    idx = df.index[df['id'] == movie_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()

# Function to get movie details
def get_movie_details(movie_title):
    movie = df[df['title'] == movie_title].iloc[0]
    return {
        'title': movie['title'],
        'genres': movie['genres'],
        'overview': movie['overview'],
        'vote_average': movie['vote_average'],
        'release_date': movie['release_date']
    }