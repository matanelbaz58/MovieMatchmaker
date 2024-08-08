import hashlib
from flask import Blueprint, request, jsonify
import requests
from pymongo import MongoClient


MONGO_STR = "mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/"
TMDB_API_KEY = "bf2a409e2a9c66f245a0b3d223179222"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
api_endpoints = Blueprint('api_endpoints', __name__)


@api_endpoints.route('/get_genre_list', methods=['GET'])
def get_genre_list():
    """
    Fetches a list of movie genres and their corresponding IDs from the TMDB API.
    
    Returns:
        dict: A dictionary containing movie genres and their corresponding IDs.
    """
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    
    data = response.json()
    genre_dict = {genre['name']: genre['id'] for genre in data['genres']}
    return jsonify(genre_dict), 200


@api_endpoints.route('/register_mongoDB', methods=['POST'])
def register():
    """
    Registers a new user in the database.
    
    Returns:
        JSON response indicating success or failure.
    """
    user_name = request.json.get('user_name')
    user_password = request.json.get('user_password')
    password_hash = hashlib.sha256(user_password.encode()).hexdigest()
    

    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': user_name})
    if user is not None:
        return jsonify({'success': False, 'message': 'User name already exists'}), 400
    
    collection.insert_one({'user_name': user_name, 'password': password_hash})            
    user = collection.find_one({'user_name': user_name})
    return jsonify({'success': user is not None}), 201


@api_endpoints.route('/remove_user_from_mongoDB', methods=['POST'])
def remove_user():
    '''
    Removes a user from the database.

    Parameters:
        user_name (str): The user name to remove.
        user_password (str): The user password for verification.


    Returns:
        JSON response indicating success or failure.
    '''
    user_name = request.json.get('user_name')
    user_password = request.json.get('user_password')
    password_hash = hashlib.sha256(user_password.encode()).hexdigest()


    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': user_name})
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 400
    if user['password'] != password_hash:
        return jsonify({'success': False, 'message': 'Incorrect password'}), 401
    collection.delete_one({'user_name': user_name})
    user = collection.find_one({'user_name': user_name})
    return jsonify({'success': True}), 200


@api_endpoints.route('/login_mongoDB', methods=['POST'])
def login_user():
    '''
    Logs in the user.

    Parameters:
        user_name (str): The user's name.
        user_password (str): The user's password.

    Returns:
        JSON response indicating success or failure.
    '''
    user_name = request.json.get('user_name')
    user_password = request.json.get('user_password')
    password_hash = hashlib.sha256(user_password.encode()).hexdigest()

    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': user_name})
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 400
    if user['password'] != password_hash:
        return jsonify({'success': False, 'message': 'Incorrect password'}), 401
    
    return jsonify({'success': True}), 200


