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


print(get_genre_list())
