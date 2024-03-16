import json
from pymongo import MongoClient
from makeAPICall import TMDB_API_caller


class User:
    
    def __init__(self, user_name, user_password):
        self.API_caller = TMDB_API_caller()
        self.user_name = user_name
        self.user_password = user_password    
        self.user_input = self.API_caller.user_input
        self.client = MongoClient('mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/')

        
    
    def check_user(self):
        '''Check if user exists in MongoDB, and if password is correct  
        Returns:
        0: if user does not exist
        1: if user exists and password is correct
        2: if user exists and password is incorrect
        '''
        db = self.client['user_search_history']
        collection = db['user_data']
        user = collection.find_one({'user_name': self.user_name})
        if user is None:
            return 0
        elif (user['password'] == self.user_password):
            return 1  
        return 2


    
    #add new user to MongoDB, if user does not exist already 
    def add_user(self):
        db = self.client['user_search_history']
        collection = db['user_data']
        
        collection.insert_one({'user_name': self.user_name, 'password': self.user_password, 'history': self.user_input})            
        # check if user was added
        user = collection.find_one({'user_name': self.user_name})
        if user is None:
            print('Failed to add user')
    
    
    def store_history(self):    
        db = self.client['user_search_history'] 
        collection = db['history_data']         
        collection.replace_one({'user_name': self.user_name, 'password': self.user_password},
                                {'user_name': self.user_name,'password': self.user_password, 'history': self.user_input}, upsert=True)

    def get_history(self):
        # Get user search history from MongoDB
        db = self.client['user_search_history']
        collection = db['history_data']
        history = collection.find({'user_name': self.user_name})
        return history

    def make_API_call(self) -> None:
        return self.API_caller.make_API_call(self.user_input)
    
    def get_genre_list(self):
        return self.API_caller.get_genre_list()
    
    def get_language_list(self):
        return self.API_caller.get_language_list()
    

#test the class
if __name__ == "__main__":
    u = User('simmeryaniv', '1234')
    print(u.check_user())
    #u.add_user()
    u.store_history()
    print(u.get_history()[3])
    #print([(i,'\n\n') for i in u.get_history()])
    #print(u.make_API_call())
    #print(u.get_genre_list())
    #print(u.get_language_list())
   # print(u.get_movie_images(550))
    
