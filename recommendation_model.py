from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Load data and define your ML logic here (the code you shared)
def load_data():
    # Move the code to load and process your dataset here
    data = pd.read_csv('./SpotifyFeatures.csv')
    data = data.drop(columns=['genre', 'track_id', 'popularity', 'duration_ms', 'key', 'mode', 'time_signature', 'liveness', 'speechiness'])
    data = data.iloc[:27000]
    numerical_features = ['danceability', 'energy', 'tempo', 'loudness', 'valence', 'acousticness', 'instrumentalness']
    metadata_features = ['artist_name', 'track_name']
    scaler = MinMaxScaler()
    data[numerical_features] = scaler.fit_transform(data[numerical_features])
    similarity_matrix = cosine_similarity(data[numerical_features])
    return data, similarity_matrix

def recommend_songs(song_title, data, similarity_matrix, top_n=5):
    # The recommendation logic you already wrote
    idx = data[data['track_name'] == song_title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    sorted_songs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended_indices = [i[0] for i in sorted_songs[1:top_n+1]]
    return data.iloc[recommended_indices][['track_name', 'artist_name']]

# Save the above as a Python script

