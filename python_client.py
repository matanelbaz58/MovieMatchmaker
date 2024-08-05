import requests


API_URL = "http://localhost:5000"
TMDB_URL = "https://api.themoviedb.org/3"
TMDB_AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"


class MongoDBHistoryManager:
    pass

class Web3HistoryManager:
    pass

class MongoDBClient:
    def __init__(self, isMongoDBClient: bool):
        self.user_name = None
        self.user_password = None
        self.wallet_address = None
        self.search_history_manager = MongoDBClient if isMongoDBClient else Web3HistoryManager

    def login(self, user_name: str, user_password: str) -> bool:
        """
        Logs in the user.

        Args:
            user_name (str): The user's name.
            user_password (str): The user's password.

        Returns:
            bool: True if the user was logged in successfully, False otherwise.
        """
        
        pass
    


    def register(self, user_name: str, user_password: str) -> dict:
        """
        Registers a new user.

        Args:
            user_name (str): The user's name.
            user_password (str): The user's password.

        Returns:
            dict: A dictionary containing the status of the registration.
        """
        pass

    def store_preference_to_history(self):
        """
        Stores the user's search history in MongoDB.
        """
        pass

    def get_preference_history(self) -> dict:
        """
        Retrieves the user's search history from MongoDB.

        Returns:
        dict: The user's search history.
        """
        pass
    
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

            .Returns None if the GET request fails.
        """
        
        
        #TODO WTF to do  with user preferences
        url = f"{TMDB_URL}/discover/movie"
        response = requests.get(url, params=user_input)

        if response.status_code == 200:
            data = response.json()
        else:
            print("Failed to fetch data:", response.status_code)
            return None
        # all dict keys: ['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 'original_title', 'overview',
        #    'popularity', 'poster_path', 'release_date', 'title', 'video', 'vote_average', 'vote_count']
       
        return data['results']  


    def get_genre_list(self) -> dict[str, int]:
        '''
        Fetches a list of movie genres from the API.
        
        returns:
            dict: A dictionary containing movie genres and their corresponding IDs. 
        '''
        url = f"{API_URL}/get_genre_list"
        response = requests.get(url)
        
        if response.status_code != 200:
            return None
        else:
            return response.json()


    def get_language_list(self) -> dict:
        """
        Fetches a list of languages from the API.

        Returns:
            dict: A dictionary containing languages and their corresponding ISO 639-1 codes.
        """
        
        url = f"{TMDB_URL}/configuration/languages"
        
        headers = {
            "accept": "application/json",
            "Authorization": TMDB_AUTH_TOKEN
        }
        response = requests.get(url ,headers=headers)
        if response.status_code != 200:
            return None
        data = response.json()
        return [language['english_name'] for language in data]


class Web3Client(MongoDBClient):
    pass



