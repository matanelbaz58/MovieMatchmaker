import hashlib
from flask import Blueprint, request, jsonify
import requests
from pymongo import MongoClient
from web3 import Web3

MONGO_STR = "mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/"
TMDB_API_KEY = "bf2a409e2a9c66f245a0b3d223179222"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
ETHERSCAN_API_KEY = 'FFSTMK324RTQAE1DI3935W2RAYHQX32DRI'
ETHERSCAN_API_ENDPOINT = 'https://api-sepolia.etherscan.io/api'

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
def get_movie_images() -> dict:
    movie_id = request.args.get('movie_id')
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/images"
    params = {
        'api_key': TMDB_API_KEY,
        'movie_id': movie_id
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}, response.status_code
    return jsonify(response.json()), 200


@api_endpoints.route('/get_movie_id_by_name', methods=['GET'])
def get_movie_id_by_name():
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
            return jsonify(data['results'][0]['id']), 200
        else:
            return {"error": "Failed to fetch data"}, response.status_code  # No results found
    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
        return {"error": "Failed to fetch data"}, response.status_code


@api_endpoints.route('/get_cast_id_by_name', methods=['GET'])
def get_cast_id_by_name():
    '''
    Fetches the ID of an actor by their name.
    
    Parameters:
        actor_name (str): The name of the actor to search for.
        
    Returns:
        int: The ID of the actor.
    '''
    actor_name = request.args.get('actor_name')
    url = f"{TMDB_BASE_URL}/search/person"
    params = {
        'api_key': TMDB_API_KEY,
        'query': actor_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data['results'][0]['id']), 200
    else:
        return {"error": "Failed to fetch data"}, response.status_code
    

@api_endpoints.route('/store_user_to_mongoDB_history', methods=['POST'])
def store_user_to_mongoDB_history():
    """
    Stores the user's search history in MongoDB.

    Parameters:
        user_name (str): The user's name.
        user_input (dict): A dictionary containing user preferences.

    Returns:
        JSON response indicating success or failure.
    """
    user_name = request.json.get('user_name')
    user_input = request.json.get('user_input')

    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']

    user = collection.find_one({'user_name': user_name})
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 400
    
    if 'user_preference_history' not in user.keys():
        user['user_preference_history'] = {}

    history_dict = user['user_preference_history']

    for key, value in user_input.items():
        if key not in history_dict:
            history_dict[key] = {value: 1}
        elif value not in history_dict[key]:
            history_dict[key][value] = 1
        else:
            history_dict[key][value] += 1

    collection.update_one(
        {'user_name': user_name},
        {'$set': {'user_preference_history': history_dict}}
    )

    return jsonify({'success': True}), 200
       
@api_endpoints.route('/get_user_history_from_mongoDB', methods=['GET'])
def get_user_history_from_mongoDB():
    '''
    Fetches the user's search history from MongoDB.

    Parameters:
        user_name (str): The user's name.

    Returns:
        dict: A dictionary containing the user's search history.
    '''
    user_name = request.args.get('user_name')
    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': user_name})
    if user is None:
        return jsonify({'error': 'User does not exist'}), 400
    return jsonify(user['user_preference_history']), 200


@api_endpoints.route('/clear_user_history_from_mongoDB', methods=['GET'])
def clear_user_history_from_mongoDB():
    '''
    Clears the user's search history from MongoDB.

    Parameters:
        user_name (str): The user's name.

    Returns:
        JSON response indicating success or failure.
    '''
    user_name = request.args.get('user_name')
    db = MongoClient(MONGO_STR)['user_management']
    collection = db['users']
    user = collection.find_one({'user_name': user_name})
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 400
    
    collection.update_one({'user_name': user_name}, {'$set': {'user_preference_history': {}}})
    return jsonify({'success': True}), 200


@api_endpoints.route('/get_contract_abi', methods=['GET'])
def get_contract_abi():
    '''
    Fetches the ABI of the smart contract.

    Returns:
        JSON response containing the ABI.
    '''
    contract_address = request.args.get('contract_address')
    
    response = requests.get(ETHERSCAN_API_ENDPOINT, params={
            "module": "contract",
            "action": "getabi",
            "address": contract_address,
            "apikey": ETHERSCAN_API_KEY
    }) 
    return jsonify(response.json()['result']), 200 if response.status_code == 200 else None