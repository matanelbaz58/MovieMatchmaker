from typing import List, Optional, Tuple
import requests
from web3_utils import Web3UserHistoryHandler

SERVER_URL = "http://localhost:5000"
TMDB_URL = "https://api.themoviedb.org/3"
SEPOLIA_URL = "https://sepolia.etherscan.io/tx/"
TMDB_AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"
SORT_BY_OPTIONS = {'popularity' : 'popularity.desc', 'release date' : 'releasedate.desc', 'vote average' : 'vote_average.desc'}


class Client:
    def __init__(self, is_mongo_db_client: bool, wallet_address: str = None, wallet_private_key: str = None):    
        self.public_identifier = None
        self.private_identifier = None
        self.genre_dict = self.get_genre_dict()
        self.language_dict = self.get_language_dict()
        self.web3_history_manager = Web3UserHistoryHandler() if not is_mongo_db_client else None
        #TODO: add monoDB self.history_manager session !

    
    def is_MongoDB_client(self):
        '''
        Returns:
            bool: True if the client is a MongoDB client, False if the client is a web3 client.
        '''
        return self.web3_history_manager == None


    def login(self, public_identifier: str, private_identifier: str) -> int:
        """
        Logs in the user.

        Args:
            public_identifier (str): The user's name / wallet address.
            private_identifier (str): The user's password / wallet private key.

        Returns:
            0 (int): if the user name does not exist.
            1 (int): if the user was logged in successfully.
            2 (int): if the password is incorrect. 
            **Note:** in case of a web3 client, 2 is returned if the wallet address or private key are incorrect.
            
        """
        if self.is_MongoDB_client():
            response = requests.post(f"{SERVER_URL}/login_mongoDB", json={"user_name": public_identifier, "user_password": private_identifier})
            if response.status_code == 400:
                return 0
            elif response.status_code == 401:
                return 2
            elif response.status_code == 200:
                self.public_identifier = public_identifier
                self.private_identifier = private_identifier
                return 1
        
        if self.web3_history_manager.authenticate_wallet(public_identifier, private_identifier):
            self.public_identifier = public_identifier
            self.private_identifier = private_identifier
            return 1
        
        return 2


    def register_user(self, public_identifier: str, private_identifier: str) -> bool:
        """
        Registers a new user. And logs in the user.

        Args:
            public_identifier (str): The user's name / wallet address.
            private_identifier (str): The user's password / wallet private key.

        Returns:
            bool: True if the user was registered successfully
        """
        #TODO: return rc indicating the reason for failure
        if self.is_MongoDB_client():
            response = requests.post(f"{SERVER_URL}/register_mongoDB", json={"user_name": public_identifier,
                                                                             "user_password": private_identifier})
            self.login(public_identifier, private_identifier)
            return response.json()['success']
        else:
            return self.login(public_identifier, private_identifier) == 1
        

    def remove_user(self) -> dict:
        """
        Removes a user from the database.
        If the user is a web3 client, will return False and and clear the user's history. (False because user cannot be removed from the blockchain)
          
        Returns:
            True : if the user was removed successfully.
            False : if the user name does not exist or failed to remove.
        """
        if not self.is_MongoDB_client():
            self.clear_user_history() #TODO: test this on sys_test.pt
            return False 
        response = requests.post(f"{SERVER_URL}/remove_user_from_mongoDB", json={"user_name": self.public_identifier, "user_password": self.private_identifier})
        return response.json()['success']


    def get_list_for_gui_dropdown(self, field: str) -> list:
        """
        Fetches a list of items for a dropdown menu in the GUI.

        Args:
            field (str): The field for which to fetch the list. Options are :'genre', 'language', 'sort_by'

        Returns:
            list: A list of items for the dropdown menu.
        """
        switcher = {
            'genre': list(self.genre_dict.keys()),
            'language': list(self.language_dict.keys()),
            'sort_by': list(SORT_BY_OPTIONS.keys())
        }
        return sorted(switcher.get(field, []))


    def prase_user_input_to_tmdb_format(self, user_input: dict) -> dict:
        """
        Prases user input to the format required by the TMDB API.

        Args:
            user_input (dict): A dictionary containing user input.

        Returns:
            dict: A dictionary containing user input in the format required by the TMDB API.
        """
        for key in user_input.keys():
            if key == 'language':
                user_input[key] = self.language_dict[user_input[key]]
            if key == 'sort_by':
                user_input[key] = SORT_BY_OPTIONS[user_input[key]]
            if key == 'genre':
                user_input[key] = self.genre_dict[user_input[key].capitalize()]
            if key == 'with_cast':
                user_input[key] = requests.get(f"{SERVER_URL}/get_cast_id_by_name", params={"actor_name": user_input[key]}).json()
        return user_input

    
    def get_movie_recommendations(self, user_input, poster_image_size=500, store_data=True) -> Tuple[List[dict], Optional[str]]:
        """
        Fetch movie recommendations based on user input.

        Parameters:
            poster_image_size (int): The size of the poster image to fetch. default is 500.
                other options are: 92, 154, 185, 342, 500, 780.
        
            user_input (dict): 
                A dictionary containing user preferences. if a key is missing, the default value is used.
                user_input = {
                    "language": "",
                    "sort_by": "popularity.desc",
                    "certification_country": "",
                    "certification": "",
                    "certification.lte": "",
                    "certification.gte": "",
                    "include_adult": False,
                    "include_video": False,
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
            Tuple[List[dict], Optional[str]]: A tuple containing a list of movie recommendations and a link to the transaction hash on Etherscan.
                The list contains dictionaries with movie data. Each dictionary contains the following keys:
                    - title (str): The title of the movie. #TODO: should this be original_title?
                    - release_date (str): The release date of the movie.
                    - genre_ids (list): A list of genres of the movie.
                    - overview (str): A brief description of the movie.
                    - popularity (float): The popularity of the movie.
                    - original_language (str): The original language of the movie.
                    - backdrop_path (str): The URL of the backdrop image of the movie. (could be used for text backround)
                    - cast (list): A list of main actors in the movie. #TODO: this isnt implemented yet
                    
                The link to the transaction hash on Etherscan is only returned if the client is a web3 client and store_data is True.
            
            .Returns None if the GET request fails.

            
        Example return value:
            ([
                {
                    'title': 'Movie Title 1',
                    'release_date': '2023-01-01',
                    'genre_ids': ['Comedy', 'Family']
                    ...
                },
                {
                    'title': 'Movie Title 2',
                    'release_date': '2023-02-01',
                    ...
                },
                ...
            ],
            'https://sepolia.etherscan.io/tx/0x123456...')         

              
        Example python usage:
            user_input = {'genre': 'Comedy', 'language': 'English'}
            recommendations = client.get_movie_recommendations(user_input)
        """
        #TODO: Add a list of main actors cast to the output
        if store_data:
            tx_hash = self.store_input_to_history(user_input)

        user_input = self.prase_user_input_to_tmdb_format(user_input)
        url = f"{SERVER_URL}/get_movie_recommendations"
        response = requests.get(url, params=user_input)

        if response.status_code != 200:
            return None
        else:
            data = response.json()['results'][:10]           
            movie_resaults = [self.format_tmdb_results(movie_dict, poster_image_size) for movie_dict in data]
            if not self.is_MongoDB_client() and store_data:
                return movie_resaults, SEPOLIA_URL + tx_hash 
            return movie_resaults
                
        
    def format_tmdb_results(self, data: dict, poster_image_size) -> dict:
        """
        Formats the data fetched from the TMDB API to a more readable user-friendly format.

        Parameters:
            data (dict): A dictionary containing movie data fetched from the TMDB API.
            poster_image_size (int): The size of the poster image to fetch.

        Returns:
            dict: A dictionary containing formatted movie data.
        """
        keys_to_keep = ['backdrop_path', 'genre_ids', 'title', 'original_language', 'overview', 'popularity', 'poster_path', 'release_date']
        
        return_dict = {}
        for key in keys_to_keep:
            if key == 'poster_path':
                return_dict['poster_url'] =  f"https://image.tmdb.org/t/p/w{poster_image_size}{data['poster_path']}"    
            elif key == 'genre_ids':
                return_dict[key] = [k for k, v in self.genre_dict.items() if v in data[key]]
            elif key == 'language':
                return_dict[key] = self.language_dict[data[key]]
            else:
                return_dict[key] = data[key]
                
        return return_dict
          

    def get_genre_dict(self) -> dict[str, int]:
        '''
        Fetches a dictionary of movie genres from the API.
        
        returns:
            dict: A dictionary containing movie genres and their corresponding IDs.      
            None: If the GET request fails.
        '''
        url = f"{SERVER_URL}/get_genre_dict"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None


    def get_language_dict(self) -> dict:
        """
        Fetches a dictionary of languages from the API.

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
        return {language['english_name']: language['iso_639_1'] for language in data}


    def get_movie_images(self, movie_title: int) -> dict:
        """
        Fetches images of a movie from the API.

        Parameters:
            movie_id (int): The ID of the movie.

        Returns:
            dict: A dictionary containing images of the movie.
        """
        url = f"{SERVER_URL}/get_movie_id_by_name"
        response = requests.get(url, params={"movie_title": movie_title})
        if response.status_code != 200:
            return None
        movie_id = response.json()
        url = f"{SERVER_URL}/get_movie_images"
        response = requests.get(url, params={"movie_id": movie_id})
        if response.status_code != 200:           
            return None
        return response.json()
    

    def update_user_preferences(self, user_input: dict, user_history: dict) -> dict:
        '''
        Updates the user's search history with the new input. 

        Parameters:
            user_input (dict): A dictionary containing the user's input.
            user_history (dict): A dictionary containing the user's search history.
        
        Returns:
            dict: The updated user's search history.
        '''
        for key, value in user_input.items():
            if key not in user_history:
                user_history[key] = {value: 1}
            elif value not in user_history[key]:
                user_history[key][value] = 1
            else:
                user_history[key][value] += 1
        return user_history


    def store_input_to_history(self, user_input: dict) -> bool | str:
        """
        Stores the user's search history in MongoDB or the blockchain. 

        Parameters:
            user_input (dict): A dictionary containing the user's input.
        
        Returns:
            bool: True if the user's search history was stored successfully.
            str: The transaction hash if the client is a web3 client.

        """
        # TODO: make sure language is stored correctly
        
        user_history = self.get_user_history()
        updated_user_history = self.update_user_preferences(user_input, user_history)

        
        if self.is_MongoDB_client():
            url = f"{SERVER_URL}/store_user_to_mongoDB_history"
            response = requests.post(url, json={"updated_user_history": updated_user_history, "user_name": self.public_identifier})
            return response.status_code == 200
        return self.web3_history_manager.update_user_history(updated_user_history, self.public_identifier, self.private_identifier)
    
    
    def get_user_history(self) -> dict:
        """
        Fetches the user's search history from MongoDB or the blockchain.

        
        Returns:
            dict: The user's search history.
        
            
        Example return value example:
            {
                'language': {'English': 1},
                'genre': {'Comedy': 2, 'Family': 1},
                'with_cast': {'Tom Cruise': 1}
            }
        """
        if self.is_MongoDB_client():
            url = f"{SERVER_URL}/get_user_history_from_mongoDB"
            response = requests.get(url, params={"user_name": self.public_identifier})
            return response.json() if response.status_code == 200 else None
        
        return self.web3_history_manager.get_user_history(self.public_identifier)


    def get_movie_recommendations_by_histoy(self) -> Tuple[List[dict], Optional[str]]:
        """
        Fetch movie recommendations based on user search history.

        
        Returns:
            same as get_movie_recommendations()
        """
        input = self.get_user_history()
        prosessed_input = {}
        for key in input.keys():
            # take the most common value
            prosessed_input[key] = max(input[key], key=input[key].get)
        return self.get_movie_recommendations(prosessed_input, store_data=False)

            
    def clear_user_history(self) -> bool:
        """
        Clears the user's search history from MongoDB or the blockchain.
        
        Returns:
            bool: True if the user's search history was cleared successfully.
        """
        if self.is_MongoDB_client():
            url = f"{SERVER_URL}/clear_user_history_from_mongoDB"
            response = requests.get(url, params={"user_name": self.public_identifier})
            return response.status_code == 200

        return self.web3_history_manager.clear_user_history(self.public_identifier ,self.private_identifier)