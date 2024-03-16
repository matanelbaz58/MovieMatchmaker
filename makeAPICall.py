
import requests

API_KEY= "bf2a409e2a9c66f245a0b3d223179222"
BASE_URL = 'https://api.themoviedb.org/3'
    
DEFAULT_USER_INPUT = { "api_key": API_KEY,
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


class TMDB_API_caller:
    
    #constructor
    def __init__(self ):
        self.user_input = DEFAULT_USER_INPUT
        self.API_KEY = API_KEY
        self.BASE_URL = BASE_URL
       


    def make_API_call(self, user_input: dict) -> None:

        url = f"{self.BASE_URL}/discover/movie"        
        # Make the GET request
        response = requests.get(url, params=user_input)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()        
        else:
            print("Failed to fetch data:", response.status_code)
            return None
        return data['results'] # =dict keys ['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count']
    

    def get_genre_list(self) -> dict:
        url = self.BASE_URL + '/genre/movie/list'
        params = {
            'api_key': self.API_KEY,
            'language': 'en-US' 
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            genre_dict = {genre['name']: genre['id'] for genre in data['genres']}
            return genre_dict
        else:
            print("Failed to fetch data:", response.status_code)
            

    def get_language_list(self) -> dict:
        url = "https://api.themoviedb.org/3/configuration/languages"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"
        }
        response = requests.get(url ,headers=headers)

        print(response.text)


    def get_movie_images(self, movie_id: int) -> dict:
        url = f"{self.BASE_URL}/movie/{movie_id}/images"
        params = {
            'api_key': self.API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            exit()
       
        data = response.json()
        return data.keys()
        

#test the class
if __name__ == "__main__":
    u = TMDB_API_caller()
    print(u.make_API_call(u.user_input))
    #print(u.get_genre_list())
    #print(u.get_language_list())
    #print(u.get_movie_images(550))
    print(u.get_movie_images(550))