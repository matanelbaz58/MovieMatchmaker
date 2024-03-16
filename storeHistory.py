import json
import make_api_call

from pymongo import MongoClient


DEFAULT_USER_PREFERENCE = {
    "language":{},
    "region":{},
    "sort_by":{},
    "certification_country":{},
    "certification":{},
    "certification.lte":{},
    "certification.gte":{},
    "include_adult":{},
    "page":{},
    "release_date.gte":{},
    "release_date.lte":{},
    "watch_region":{},
    "with_cast":{},
    "with_companies":{},
    "with_genres": {},
    "with_keywords":{},
    "with_people":{},
    "with_runtime.gte": {},
    "with_runtime.lte": {},
    "without_companies": {},
    "without_genres": {},
    "without_keywords": {},
    "year": {},
}

class User:
    """
    A class to represent a user.

    Attributes:
    user_name (str): The user's name.
    user_password (str): The user's password.
    user_input (dict): The default user input for API calls.
    user_preference (dict): The user's preferences.
    client (MongoClient): The MongoDB client.

    Methods:
    check_user(): Checks if the user exists and if the password is correct.
    add_user(): Adds a new user to MongoDB.
    store_history(): Stores the user's search history in MongoDB.
    get_history(): Retrieves the user's search history from MongoDB.
    make_api_call(): Makes an API call to get movie recommendations.
    remove_user(): Removes a user from MongoDB.
    """
    
    def __init__(self, user_name, user_password):
        """
        Constructs all the necessary attributes for the user object.

        Parameters:
        user_name (str): The user's name.
        user_password (str): The user's password.
        """
        self.user_name = user_name
        self.user_password = user_password    
        self.user_input = make_api_call.DEFAULT_USER_INPUT
        self.user_preference = DEFAULT_USER_PREFERENCE
        self.client = MongoClient(make_api_call.MONGO_STR)
        
    def check_user(self):
        """
        Checks if the user exists in MongoDB and if the password is correct.

        Returns:
        int: 0 if the user does not exist, 1 if the user exists and the password is correct, 2 if the user exists but the password is incorrect.
        """
        db = self.client['user_search_history']
        collection = db['user_data']
        user = collection.find_one({'user_name': self.user_name})
        if user is None:
            return 0
        elif user['password'] == self.user_password:
            self.user_preference = user['user_preference']
            return 1  
        return 2

    def add_user(self) -> bool:
        """
        Adds a new user to MongoDB.

        Returns:
        bool: True if the user was added, False if the user already exists or failed to add.
        """
        db = self.client['user_search_history']
        collection = db['user_data']
        user = collection.find_one({'user_name': self.user_name})
        if user is not None:
            return False
        collection.insert_one({'user_name': self.user_name, 'password': self.user_password, 'user_preference': self.user_preference})            
        user = collection.find_one({'user_name': self.user_name})
        return user is not None
    
    def store_history(self):
        """
        Stores the user's search history in MongoDB.
        """
        db = self.client['user_search_history']
        collection = db['history_data']
        collection.replace_one({'user_name': self.user_name, 'password': self.user_password},
                               {'user_name': self.user_name, 'password': self.user_password, 'user_preference': self.user_preference}, upsert=True)

    def get_history(self) -> dict:
        """
        Retrieves the user's search history from MongoDB.

        Returns:
        dict: The user's search history.
        """
        db = self.client['user_search_history']
        collection = db['history_data']
        history = collection.find_one({'user_name': self.user_name})
        return history['user_preference'] if history else None

    def make_api_call(self) -> list:
        """
        Makes an API call to get movie recommendations based on the user's input and preferences.

        Returns:
        list: A list of dictionaries containing movie recommendations.
        """
        return make_api_call.get_movie_recommendations(self.user_input, self.user_preference)
    
    def remove_user(self) -> bool:
        """
        Removes a user from MongoDB.

        Returns:
        bool: True if the user was removed, False if the user does not exist or failed to remove.
        """
        db = self.client['user_search_history']
        collection = db['user_data']
        result = collection.delete_one({'user_name': self.user_name, 'password': self.user_password})
        return result.deleted_count > 0

# Test the class with assert statements
def test_user():
    """
    Tests the User class.
    """
    user = User('test_user4', 'password')
    assert user.check_user() == 0
    assert user.add_user() is True
    assert user.check_user() == 1

    user2 = User('test_user4', 'worng_password')
    assert user2.check_user() == 2
    assert user2.add_user() is False

    assert user.make_api_call() is not None
    assert user.store_history() is None
    assert user.get_history() == user.user_preference
    assert user.remove_user() is True
    print('All tests passed')

# if __name__ == "__main__":
#     test_user()
