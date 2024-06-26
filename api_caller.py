import requests
from typing import Optional
"""
handles all API calls to the movie database API.
"""



MONGO_STR = "mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/"
API_KEY = "bf2a409e2a9c66f245a0b3d223179222"
BASE_URL = 'https://api.themoviedb.org/3'

DEFAULT_USER_INPUT = {
    "api_key": API_KEY,
    "page": 1,
    "with_original_language": "",
    "language": "", # TODO make same as with_original_language
    "region" : "",
    "sort_by": "popularity.desc",
    "certification_country": "US",
    "certification": "",
    "certification.lte": "",
    "certification.gte": "",
    "include_adult": False,

    "release_date.gte": "",
    "release_date.lte": "",
    "watch_region": "",
    "with_cast": "",
    "with_companies": "",
    "with_crew": "",
    "with_genres": "",  # # Filters movies by their genre IDs
    "with_keywords": "",
    "with_people": "",
    # Filter movies by their runtime, specifying a minimum (gte) and maximum (lte) duration in minutes.
    "with_runtime.gte": "",
    "with_runtime.lte": "",
    "without_companies": "",  # Filter to exclude specific genres
    # Filters movies by their genre IDs, or excludes specific genres.
    "without_genres": "",
    # Filters movies based on specific keywords or excludes them.
    "without_keywords": "",
    "year": ""  # Filters movies released in a specific year.
}


def get_movie_recommendations(user_input: dict[str, str], user_preference: dict) -> dict:
    """
    Fetch movie recommendations based on user input.

    Parameters:
    user_input (dict): A dictionary containing user preferences.
    user_preference (dict): A dictionary containing user preferences.

    Returns:
    list : A list of dictionaries containing movie recommendations, the important ones are: 
    'backdrop_path' (path to imaage)
    'genre_ids'
    'id'
    'original_language'
    'overview' (a short description of the movie)
    'popularity'
    'poster_path'
    'release_date'
    'title'

    .Returns None if the request fails.
    """
    url = f"{BASE_URL}/discover/movie"

    # Make the GET request
    response = requests.get(url, params=user_input)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

    return data['results']  # = dict keys ['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count']


def get_genre_list(API_KEY: str) -> dict[str, int]:
    '''
    Fetches a list of movie genres from the API.
    
    returns:
    dict: A dictionary containing movie genres and their corresponding IDs. 
    '''
    url = f"{BASE_URL}/genre/movie/list"
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        genre_dict = {genre['name']: genre['id'] for genre in data['genres']}
        return genre_dict
    else:
        print("Failed to fetch data:", response.status_code)


def get_language_list() -> dict:
    """
    Fetches a list of languages from the API.

    Returns:
    dict: A dictionary containing languages and their corresponding ISO 639-1 codes.
    """

    url = "https://api.themoviedb.org/3/configuration/languages"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"
    }
    response = requests.get(url ,headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data:", response.status_code)
        exit()
    data = response.json()
    return [language['english_name'] for language in data]


# def get_movie_images(self, movie_id: int) -> dict:
#     url = f"{self.BASE_URL}/movie/{movie_id}/images"
#     params = {
#         'api_key': self.API_KEY
#     }
#     response = requests.get(url, params=params)
#     if response.status_code != 200:
#         print("Failed to fetch data:", response.status_code)
#         exit()

#     data = response.json()
#     return data.keys()


#print(get_language_list())
