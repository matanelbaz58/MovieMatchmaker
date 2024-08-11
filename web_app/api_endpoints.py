import hashlib
from flask import Blueprint, request, jsonify
import requests
from pymongo import MongoClient

ABI = '[{"inputs":[],"name":"num","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"person","outputs":[{"internalType":"uint256","name":"num","type":"uint256"},{"internalType":"string","name":"name","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"retrive","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_num","type":"uint256"}],"name":"store","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stru","outputs":[{"internalType":"uint256","name":"num","type":"uint256"},{"internalType":"string","name":"name","type":"string"}],"stateMutability":"view","type":"function"}]'
MONGO_STR = "mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/"
TMDB_API_KEY = "bf2a409e2a9c66f245a0b3d223179222"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
api_endpoints = Blueprint('api_endpoints', __name__)


@api_endpoints.route('/get_genre_dict', methods=['GET'])
def get_genre_list():
    '''
    Fetches a list of movie genres from the API.
    
    returns:
        dict: A dictionary containing movie genres and their corresponding IDs.      
    '''
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
    return jsonify({'success': user is None}), 200


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


@api_endpoints.route('/get_movie_recommendations', methods=['GET'])
def get_movie_recommendations():
    """
    Fetch movie recommendations based on user input.
    Parameters:
        user_input (dict): A dictionary containing user preferences. if a key is missing, the default value is used.
            user_input = {
                "language": "",
                "region": "",
                "sort_by": "popularity.desc",
                "certification_country": "",
                "certification": "",
                "certification.lte": "",
                "certification.gte": "",
                "include_adult": False,
                "include_video": False,
                "page": 1,
                "primary_release_year": "",
                "primary_release_date.gte": "",
                "primary_release_date.lte": "",
                "release_date.gte": "",
                "release_date.lte": "",
                "vote_average.gte": "",
                "vote_average.lte": "",
                "vote_count.gte": "",
                "vote_count.lte": "",
                "watch_region": "",
                "with_cast": "",
                "with_companies": "",
                "with_crew": "",
                "with_genres": "",
                "with_keywords": "",
                "with_origin_country": "",
                "with_original_language": "",
                "with_people": "",
                "with_release_type": "",
                "with_runtime.gte": "",
                "with_runtime.lte": "",
                "with_watch_monetization_types": "",
                "with_watch_providers": "",
                "without_companies": "",
                "without_genres": "",
                "without_keywords": "",
                "without_watch_providers": "",
                "year": ""
            }

    Returns:
        A list of dictionaries. each dictionarie contains data about a movie recommendation.
        Each dictionarie contains the next keys:
            'backdrop_path' (path to a backround imaage, could be used for text backround)
            'genre_ids'
            'title'
            'original_language'
            'overview' (a short description of the movie)
            'popularity'
            'poster_path' (path to the movie's main cover  image)
            'release_date'
            'title'
    """
    user_input = request.args.to_dict()
    user_input['api_key'] = TMDB_API_KEY

    url = f"{TMDB_BASE_URL}/discover/movie"
    response = requests.get(url, params=user_input)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    return jsonify(response.json()), 200
   
@api_endpoints.route('/get_movie_images', methods=['GET'])    
def get_movie_images(movie_id: int) -> dict:
    url = f"{    git add -ABASE_URL}/movie/{movie_id}/images"
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}, response.status_code
    return response.json() 


@api_endpoints.route('/get_movie_id_by_name', methods=['GET'])
def get_movie_id_by_name(self):
    '''
    Fetches the ID of a movie by its title.
    
    Parameters:
        movie_title (str): The title of the movie to search for.
        
    Returns:
        int: The ID of the movie.
    '''
    movie_title = request.args.get('movie_title')
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_title
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']  # Returns the ID of the first result
        else:
            return None  # No results found
    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
        return None