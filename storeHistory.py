import json
from pymongo import MongoClient
import argparse

def main():
    
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://simmeryaniv:gSNjq96LSO7IMxt6@moviematchmakerdb.ql3efn4.mongodb.net/')
    db = client['user_search_history']  # replace 'your_database' with the name of your database
    collection = db['history_data']  # replace 'your_collection' with the name of your collection

    # Insert user input into MongoDB
    with open('history.json') as f:
        file_data = json.load(f)
    collection.insert_one(file_data)

if __name__ == "__main__":
    main()