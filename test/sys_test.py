from io import BytesIO
from tkinter import Image
import tkinter as tk
import requests
import sys
import os
import pytest
from deepdiff import DeepDiff

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_client import Client

GENRE_LIST = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}
LANGUAGE_LIST = ['Abkhazian', 'Afar', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Aragonese', 'Armenian', 'Assamese', 'Avaric', 'Avestan', 'Aymara', 'Azerbaijani', 'Bambara', 'Bashkir', 'Basque', 'Belarusian', 'Bengali', 'Bislama', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Cantonese', 'Catalan', 'Chamorro', 'Chechen', 'Chichewa; Nyanja', 'Chuvash', 'Cornish', 'Corsican', 'Cree', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'Dzongkha', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Faroese', 'Fijian', 'Finnish', 'French', 'Frisian', 'Fulah', 'Gaelic', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian; Haitian Creole', 'Hausa', 'Hebrew', 'Herero', 'Hindi', 'Hiri Motu', 'Hungarian', 'Icelandic', 'Ido', 'Igbo', 'Indonesian', 'Interlingua', 'Interlingue', 'Inuktitut', 'Inupiaq', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kalaallisut', 'Kannada', 'Kanuri', 'Kashmiri', 'Kazakh', 'Khmer', 'Kikuyu', 'Kinyarwanda', 'Kirghiz', 'Komi', 'Kongo', 'Korean', 'Kuanyama', 'Kurdish', 'Lao', 'Latin', 'Latvian', 'Letzeburgesch', 'Limburgish', 'Lingala', 'Lithuanian', 'Luba-Katanga', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Mandarin', 'Manx', 'Maori', 'Marathi', 'Marshall', 'Moldavian', 'Mongolian', 'Nauru', 'Navajo', 'Ndebele', 'Ndonga', 'Nepali', 'No Language', 'Northern Sami', 'Norwegian', 'Norwegian Bokmål', 'Norwegian Nynorsk', 'Occitan', 'Ojibwa', 'Oriya', 'Oromo', 'Ossetian; Ossetic', 'Pali', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Pushto', 'Quechua', 'Raeto-Romance', 'Romanian', 'Rundi', 'Russian', 'Samoan', 'Sango', 'Sanskrit', 'Sardinian', 'Serbian', 'Serbo-Croatian', 'Shona', 'Sindhi', 'Sinhalese', 'Slavic', 'Slovak', 'Slovenian', 'Somali', 'Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swati', 'Swedish', 'Tagalog', 'Tahitian', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tigrinya', 'Tonga', 'Tsonga', 'Tswana', 'Turkish', 'Turkmen', 'Twi', 'Uighur', 'Ukrainian', 'Urdu', 'Uzbek', 'Venda', 'Vietnamese', 'Volapük', 'Walloon', 'Welsh', 'Wolof', 'Xhosa', 'Yi', 'Yiddish', 'Yoruba', 'Zhuang', 'Zulu']


def test_direct_api_calls():
    '''
    Test the API calls that are called directly from the TMDB API without using the server as an intermediary.
    '''
    client = Client(True)
    assert client.get_list_for_gui_dropdown('language') == sorted(LANGUAGE_LIST)
    assert client.get_list_for_gui_dropdown('genre') == sorted(list(GENRE_LIST.keys()))
    assert client.get_list_for_gui_dropdown('sort_by') == ['popularity', 'release date', 'vote average']
   
    movie_recomend = client.get_movie_recommendations(user_input={'language': 'en', 'genre': 'comedy', 'with_cast': 'Tom Cruise'})
    assert type(movie_recomend) == list
    assert len(movie_recomend) == 10
    


def test_get_requests_from_server():
    '''
    Test the API calls that are made through the server.
    '''
    client = Client(True)
    assert client.get_genre_dict() == GENRE_LIST


def test_user_authentication():
    '''
    Test the registration of a new user and the removal of the same user.
    '''
    client = Client(True)
    assert client.register_user('test_user', 'test_password') == True
    assert client.register_user('test_user', 'test_password') == False

    client_2 = Client(True)
    assert client_2.login('rong_name', 'test_password') == 0
    assert client_2.login('test_user', 'rong_password') == 2
    assert client_2.login('test_user', 'test_password') == 1

    assert client.remove_user('test_user', 'test_password') == True 
    assert client.remove_user('test_user', 'test_password') == False

    assert client_2.login('test_user', 'test_password') == 0

def test_user_history():
    '''
    test the user history
    '''
    client = Client(True)
    client.register_user('test_user', 'test_password')
    assert client.get_user_history() == None
    client.get_movie_recommendations(user_input={'language': 'en', 'genre': 'comedy', 'with_cast': 'Tom Cruise'}) 
    assert client.get_user_history() == {'language': {'en': 1}, 'genre': {'comedy': 1}, 'with_cast': {'Tom Cruise': 1}}
    client.get_movie_recommendations(user_input={'language': 'en', 'genre': 'comedy', 'with_cast': 'Leonardo DiCaprio'})
    assert client.get_user_history() == {'language': {'en': 2}, 'genre': {'comedy': 2}, 'with_cast': {'Tom Cruise': 1, 'Leonardo DiCaprio': 1}}
    client.get_movie_recommendations(user_input={'with_cast': 'Tom Cruise'})
    assert client.get_user_history() == {'language': {'en': 2}, 'genre': {'comedy': 2}, 'with_cast': {'Tom Cruise': 2, 'Leonardo DiCaprio': 1}}
    
    movie_recomend = client.get_movie_recommendations_by_histoy()
    assert type(movie_recomend) == list
    assert len(movie_recomend) == 10

    client.remove_user('test_user', 'test_password')

if __name__ == '__main__':
    pytest.main()
    #test_user_history()

