
import requests


class utils:
    API_KEY= "bf2a409e2a9c66f245a0b3d223179222"
    BASE_URL = 'https://api.themoviedb.org/3'
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

    def get_response(self, url, params):
        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()        
        else:
            print("Failed to fetch data:", response.status_code)
            return None

    def make_API_call(self, user_input: dict) -> None:

        # parser = argparse.ArgumentParser()
        # parser.add_argument('--api_key', help='API key for the movie database')
        # args = parser.parse_args()
        # API_KEY = args.api_key
    
    

        url = f"{self.BASE_URL}/discover/movie"

        # Adding the API key to the dictionary
        user_input['api_key'] = self.API_KEY

        # Make the GET request
        data = self.get_response(url, params=user_input)
        print(data)
    