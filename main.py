from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your actual TMDB API key
TMDB_API_KEY = '8869a76543d94698b7af7935fc80defa'
PREFERENCES_FILE = 'user_preferences.json'

def save_user_preferences(user_id, data):
    """Save user preferences to a JSON file."""
    try:
        with open(PREFERENCES_FILE, 'r+') as file:
            preferences = json.load(file)
            preferences[user_id] = data
            file.seek(0)
            json.dump(preferences, file, indent=4)
    except FileNotFoundError:
        with open(PREFERENCES_FILE, 'w') as file:
            json.dump({user_id: data}, file, indent=4)
    except json.JSONDecodeError:
        with open(PREFERENCES_FILE, 'w') as file:
            json.dump({user_id: data}, file, indent=4)

def load_user_preferences(user_id):
    """Load user preferences from a JSON file."""
    try:
        with open(PREFERENCES_FILE, 'r') as file:
            preferences = json.load(file)
            return preferences.get(user_id, {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def fetch_movies_from_tmdb(genre_id):
    """Fetch movies from TMDB based on the genre ID."""
    response = requests.get(f"https://api.themoviedb.org/3/discover/movie",
                            params={
                                'api_key': TMDB_API_KEY,
                                'with_genres': genre_id,
                                'sort_by': 'popularity.desc'
                            })
    movies = response.json().get('results', [])
    return movies

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    """Endpoint to submit user movie preferences."""
    user_data = request.json
    user_id = user_data['user_id']
    save_user_preferences(user_id, user_data)
    return jsonify({"message": "Preferences saved successfully"}), 200

@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    """Endpoint to get a movie recommendation based on user preferences."""
    user_id = request.args.get('user_id')
    preferences = load_user_preferences(user_id)
    genre_id = preferences.get('genre_id', '')
    movies = fetch_movies_from_tmdb(genre_id)
    if movies:
        # Return the most popular movie for simplicity
        return jsonify(movies[0]), 200
    else:
        return jsonify({"message": "No movies found for the selected preferences"}), 404

if __name__ == '__main__':
    app.rgitun(debug=True)
