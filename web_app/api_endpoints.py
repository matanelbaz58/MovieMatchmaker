from flask import Blueprint, request, jsonify
import requests
from pymongo import MongoClient


api_endpoints = Blueprint('api_endpoints', __name__)
MONGO_STR = "mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/"
API_KEY = "bf2a409e2a9c66f245a0b3d223179222"
BASE_URL = 'https://api.themoviedb.org/3'


@api_endpoints.route('/get_genre_list', methods=['GET'])
def get_genre_list():
    """
    Fetches a list of movie genres and their corresponding IDs from the TMDB API.
    
    Returns:
        dict: A dictionary containing movie genres and their corresponding IDs.
    """
    url = f"{BASE_URL}/genre/movie/list"
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    
    data = response.json()
    genre_dict = {genre['name']: genre['id'] for genre in data['genres']}
    return jsonify(genre_dict), 200


@api_endpoints.route('/register', methods=['POST'])
def register():
    """
    Registers a new user in the database.
    
    Returns:
        True : if the user was added
        False : if the user name already exists or failed to add.
    """
    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': self.user_name})
    if user is not None:
        return False
    collection.insert_one({'user_name': self.user_name, 'password': self.user_password, 'user_preference': self.user_preference})            
    user = collection.find_one({'user_name': self.user_name})
    return user is not None       



