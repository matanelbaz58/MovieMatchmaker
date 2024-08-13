import requests


SERVER_URL = "http://localhost:5000"
TMDB_URL = "https://api.themoviedb.org/3"
TMDB_AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZjJhNDA5ZTJhOWM2NmYyNDVhMGIzZDIyMzE3OTIyMiIsInN1YiI6IjY1ZGNmMzUyOGMwYTQ4MDEzMTFkYTI0OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_XHPeZXtKSrozDmPcZKEaIbz4W5CpfloqD0l0LDLtY"
SORT_BY_OPTIONS = {'popularity' : 'popularity.desc', 'release date' : 'releasedate.desc', 'vote average' : 'vote_average.desc'}


class Client:
    def __init__(self, isMongoDBClient: bool):
        self.user_name = None
        self.user_password = None
        self.wallet_address = None
        self.genre_dict = self.get_genre_dict()
        self.language_dict = self.get_language_dict()
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
        response = requests.post(f"{SERVER_URL}/login_mongoDB", json={"user_name": user_name, "user_password": user_password})
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
        response = requests.post(f"{SERVER_URL}/register_mongoDB", json={"user_name": user_name, "user_password": user_password})
        self.login(user_name, user_password)
        return response.json()['success']

    def remove_user(self, user_name: str, user_password: str) -> dict:
        """
        Removes a user from the database.
        
        Returns:
            True : if the user was removed successfully.
            False : if the user name does not exist or failed to remove.
        """
        response = requests.post(f"{SERVER_URL}/remove_user_from_mongoDB", json={"user_name": user_name, "user_password": user_password})
        return response.json()['success']

    def store_preference_to_history(self):
        """
        Stores the user's search history in MongoDB.
        """
        pass

    def get_list_for_gui_dropdown(self, field: str) -> list:
        """
        Fetches a list of items for a dropdown menu in the GUI.

        Args:
            field (str): The field for which to fetch the list.

        Returns:
            list: A list of items for the dropdown menu.
        """
        switcher = {
            'genre': list(self.genre_dict.keys()),
            'language': list(self.language_dict.keys()),
            'sort_by': list(SORT_BY_OPTIONS.keys())
        }
        return sorted(switcher.get(field, []))




    
    def get_movie_recommendations(self, user_input, poster_image_size=500) -> list[dict]:
        """
        Fetch movie recommendations based on user input.

        Parameters:
            poster_image_size (int): The size of the poster image to fetch. default is 500.
                other options are 92, 154, 185, 342, 500, 780.
        
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
            A list of 10 dictionaries. each dictionarie contains data about a movie recommendation.
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
            
            .Returns None if the GET request fails.

            
        Example return value:
            [
                {
                    'title': 'Movie Title 1',
                    'release_date': '2023-01-01',
                    'poster_path': '\\x81\\x0b\\x7 ...',
                    'genre_ids': ['Comedy', 'Family']
                    ...
                },
                {
                    'title': 'Movie Title 2',
                    'release_date': '2023-02-01',
                    'poster_path': '\\x81\\x0b\\x7 ...',
                    ...
                },
                ...
            ]         

              
        Example python usage:
            user_input = {'user_id': 123, 'genre': 'comedy'}
            recommendations = get_movie_recommendations(user_input)
        
        
        Example of poster_path image showing with tkinter:
            import requests
            from io import BytesIO
            import tkinter as tk
            from PIL import Image, ImageTk

            responce = Client(True).get_movie_recommendations(user_input={'language': 'en', 'genre': 'comedy'}, poster_image_size=185)
            img_data = img_data[0]['poster_path']
            root = tk.Tk()
            root.title("Movie Poster")
    
            # Load image data into PIL and then convert it to a format tkinter can use
            img = Image.open(BytesIO(img_data))
            img_tk = ImageTk.PhotoImage(img
            # Create a label and add the image to it
            label = tk.Label(root, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack(
            # Run the tkinter loop
            root.mainloop()
        """
        #TODO: Add a list of main actors cast to the output
        
        self.store_input_to_history(user_input)

        url = f"{SERVER_URL}/get_movie_recommendations"
        
        user_input['genre'] = self.genre_dict[user_input['genre'].capitalize()] if 'genre' in user_input else 28
        user_input['language'] = [k for k, v in self.language_dict.items() if v == user_input['language']][0] if 'language' in user_input else 'en'
        user_input['sort_by'] = SORT_BY_OPTIONS[user_input['sort_by']] if 'sort_by' in user_input else 'popularity.desc'
        user_input['with_cast'] = requests.get(f"{SERVER_URL}/get_cast_id_by_name", params={"actor_name": user_input['with_cast']}).json() if 'with_cast' in user_input else ''
        response = requests.get(url, params=user_input)

        if response.status_code != 200:
            return response
        else:
            data = response.json()['results'][:10]           
            return [self.process_movie_recommendations(movie_dict, poster_image_size) for movie_dict in data]
    
        
    def process_movie_recommendations(self, data: dict, poster_image_size) -> dict:
            keys_to_keep = ['backdrop_path', 'genre_ids', 'title', 'original_language', 'overview', 'popularity', 'poster_path', 'release_date']
            
            poster_url = f"https://image.tmdb.org/t/p/w{poster_image_size}{data['poster_path']}" if 'poster_path' in data else None
            
            return {
                key: (
                    requests.get(poster_url).content if key == 'poster_path' else
                    [k for k, v in self.genre_dict.items() if v in data[key]] if key == 'genre_ids' else
                    data[key]
                )
                for key in keys_to_keep if key in data
            } | {'poster_url': poster_url}  
            

    def get_genre_dict(self) -> dict[str, int]:
        '''
        Fetches a list of movie genres from the API.
        
        returns:
            dict: A dictionary containing movie genres and their corresponding IDs.      
        '''
        url = f"{SERVER_URL}/get_genre_dict"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        else:
            return response.json()


    def get_language_dict(self) -> dict:
        """
        Fetches a dictionary 
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
    
    def store_input_to_history(self, user_input: dict) -> bool:
        """
        Stores the user's search history in MongoDB.
        """
        
        url = f"{SERVER_URL}/store_user_to_mongoDB_history"
        response = requests.post(url, json={"user_input": user_input, "user_name": self.user_name})
        if response.status_code != 200:
            return False
        return True
    
    def get_user_history(self) -> dict:
        """
        Retrieves the user's search history from MongoDB.

        Returns:
            dict: The user's search history.
        """
        url = f"{SERVER_URL}/get_user_history_from_mongoDB"
        response = requests.get(url, params={"user_name": self.user_name})
        if response.status_code != 200:
            return None
        return response.json()
        

    def get_movie_recommendations_by_histoy(self):
        """
        Fetch movie recommendations based on user history.

        Returns:
            same as get_movie_recommendations()
        """
        input = self.get_user_history()
        prosessed_input = {}
        for key in input.keys():
            # take the most common value
            prosessed_input[key] = max(input[key], key=input[key].get)
        return self.get_movie_recommendations(prosessed_input)

            
        
        
