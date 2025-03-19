from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# 1. Load the dataset
data = pd.read_csv('./SpotifyFeatures.csv')  # Adjust the path if necessary
data = data.drop(columns=['genre', 'track_id', 'popularity', 'duration_ms', 'key', 'mode', 'time_signature', 'liveness', 'speechiness'])

# Drop rows to keep only the first 10,000 rows
data = data.iloc[:10000]

# 2. Select relevant features (numerical and categorical)
numerical_features = ['danceability', 'energy', 'tempo', 'loudness', 'valence', 'acousticness', 'instrumentalness']
metadata_features = ['artist_name', 'track_name']  # Keep for display but won't use in similarity calculation

# Normalize numerical features to bring them to the same scale
scaler = MinMaxScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# 3. Calculate similarity using only numerical features
similarity_matrix = cosine_similarity(data[numerical_features])

# 4. Recommendation function
def recommend_songs(song_title, data, similarity_matrix, top_n=5):
    # Find the song index
    idx = data[data['track_name'].str.lower() == song_title.lower()].index[0]

    # Get pairwise similarity scores
    similarity_scores = list(enumerate(similarity_matrix[idx]))

    # Sort based on similarity scores
    sorted_songs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Recommend top N songs (ignoring the first, which is the same song)
    recommended_indices = [i[0] for i in sorted_songs[1:top_n+1]]

    return data.iloc[recommended_indices][['track_name', 'artist_name']]

@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.json.get('song_name')
    # Get recommendations
    recommendations = recommend_songs(song_name, data, similarity_matrix)
    return jsonify({"recommendations": recommendations.to_dict(orient="records")})

if __name__ == '__main__':
    app.run(debug=True)
