import requests
import argparse

API_KEY= "bf2a409e2a9c66f245a0b3d223179222"
BASE_URL = 'https://api.themoviedb.org/3'
user_input = {}

def get_genre_list() -> dict:
    url = BASE_URL + '/genre/movie/list'
    params = {
        'api_key': API_KEY,
        'language': 'en-US' 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data:", response.status_code)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--api_key', help='API key for the movie database')
    # args = parser.parse_args()
    # API_KEY = args.api_key

    # Get the list of genres
    genre_list = get_genre_list()

    user_input = {
    "language": "en-US",  # Language of the results
    "region": "",  # ISO 3166-1 code to filter release dates. Must be uppercase.
    "sort_by": "popularity.desc",  # Criteria for sorting the results
    "certification_country": "",  # Country code for filtering by certification
    "certification": "",  # Certification filter
    "certification.lte": "",  # Movies with certification lower than or equal to the specified value
    "certification.gte": "",  # Movies with certification greater than or equal to the specified value
    "include_adult": False,  # Include adult (pornographic) content in the results
    "include_video": False,  # Include video results
    "page": 1,  # Page number for pagination
    "primary_release_year": "",  # Filter by primary release year
    "primary_release_date.gte": "",  # Movies with primary release date greater than or equal to the specified date
    "primary_release_date.lte": "",  # Movies with primary release date less than or equal to the specified date
    "release_date.gte": "",  # Movies with release date greater than or equal to the specified date
    "release_date.lte": "",  # Movies with release date less than or equal to the specified date
    "vote_count.gte": "",  # Movies with vote count greater than or equal to the specified number
    "vote_count.lte": "",  # Movies with vote count less than or equal to the specified number
    "vote_average.gte": "",  # Movies with vote average greater than or equal to the specified number
    "vote_average.lte": "",  # Movies with vote average less than or equal to the specified number
    "with_cast": "",  # Filter by one or more cast member IDs
    "with_crew": "",  # Filter by one or more crew member IDs
    "with_people": ""  # Filter by one or more people IDs associated with the movie
    }

    url = "https://api.themoviedb.org/3/discover/movie"

    # Adding the API key to the dictionary
    user_input['api_key'] = API_KEY

    # Make the GET request
    response = requests.get(url, params=user_input)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()        
    else:
        print("Failed to fetch data:", response.status_code)
    # print the movie titles    
    for movie in data['results']:
        print(movie['title'])


if __name__ == '__main__':
    main()




