import requests


API_URL = "http://localhost:5000"
TMDB_URL = "https://api.themoviedb.org/3"
TMDB_AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"



class Client:
    def __init__(self, isMongoDBClient: bool):
        self.user_name = None
        self.user_password = None
        self.wallet_address = None
        #self.search_history_manager = MongoDBClient if isMongoDBClient else Web3HistoryManager

    def login(self, user_name: str, user_password: str) -> int:
        """
        Logs in the user.

        Args:
            user_name (str): The user's name.
            user_password (str): The user's password.

        Returns:
            0 (int): if the user name does not exist.
            1 (int): if the user was logged in successfully.
            2 (int): if the password is incorrect.
        """
        response = requests.post(f"{API_URL}/login_mongoDB", json={"user_name": user_name, "user_password": user_password})
        if response.status_code == 400:
            return 0
        elif response.status_code == 401:
            return 2
        elif response.status_code == 200:
            self.user_name = user_name
            self.user_password = user_password
            return 1


    def register_user(self, user_name: str, user_password: str) -> dict:
        """
        Registers a new user in the database and logs them in.
        
        Returns:
            True : if the user was added successfully.
            False : if the user name already exists or failed to add.
        """
        response = requests.post(f"{API_URL}/register_mongoDB", json={"user_name": user_name, "user_password": user_password})
        self.login(user_name, user_password)
        return response.json()['success']

    def remove_user(self, user_name: str, user_password: str) -> dict:
        """
        Removes a user from the database.
        
        Returns:
            True : if the user was removed successfully.
            False : if the user name does not exist or failed to remove.
        """
        response = requests.post(f"{API_URL}/remove_user_from_mongoDB", json={"user_name": user_name, "user_password": user_password})
        return response.json()['success']

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
        #TMDB_API_KEY = "bf2a409e2a9c66f245a0b3d223179222" #TODO: remove

        headers = {
            "accept": "application/json",
            "Authorization": TMDB_AUTH_TOKEN
            #'api_key': TMDB_API_KEY,
        }
        response = requests.get(url ,headers=headers)
        if response.status_code != 200:
            return None
        data = response.json()
        return [language['english_name'] for language in data]





