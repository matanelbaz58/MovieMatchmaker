import requests
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', help='API key for the movie database')
    args = parser.parse_args()

    API_KEY = args.api_key
    BASE_URL = 'https://api.themoviedb.org/3'

    # Step 1: Find Bruce Willis's ID
    search_response = requests.get(f"{BASE_URL}/search/person", params={
        'api_key': API_KEY,
        'query': 'Bruce Willis'
    })
    bruce_willis_id = search_response.json()['results'][0]['id']

    # Step 2: Discover movies from the 1990s featuring Bruce Willis
    discover_response = requests.get(f"{BASE_URL}/discover/movie", params={
        'api_key': API_KEY,
        'with_cast': bruce_willis_id,
        'release_date.gte': '1990-01-01',
        'release_date.lte': '1999-12-31'
    })

    movies = discover_response.json()['results']
    for movie in movies:
        print(movie['title'], movie['release_date'])


if __name__ == '__main__':
    main()