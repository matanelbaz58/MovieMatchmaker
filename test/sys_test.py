import requests
import sys
import os
import pytest
from deepdiff import DeepDiff


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_client import Client

GENRE_LIST = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}
LANGUAGE_LIST = ['Aragonese', 'Akan', 'Cree', 'Azerbaijani', 'Czech', 'Afar', 'Breton', 'Afrikaans', 'Tibetan', 'Chechen', 'Cornish', 'Faroese', 'Latin', 'Ndonga', 'Sardinian', 'Tigrinya', 'Tswana', 'Turkish', 'Punjabi', 'Estonian', 'French', 'Hausa', 'Icelandic', 'Limburgish', 'Lingala', 'Swati', 'Abkhazian', 'Serbo-Croatian', 'Basque', 'Frisian', 'Japanese', 'Ojibwa', 'Oriya', 'Pali', 'Sundanese', 'Thai', 'Igbo', 'Indonesian', 'Kazakh', 'Kikuyu', 'Uighur', 'Venda', 'Kinyarwanda', 'Maori', 'Navajo', 'Hindi', 'Portuguese', 'Sango', 'Slovak', 'Serbian', 'Tahitian', 'Xhosa', 'Arabic', 'Corsican', 'Bislama', 'Esperanto', 'Herero', 'Finnish', 'Inuktitut', 'Latvian', 'Italian', 'Dutch', 'Kannada', 'Sanskrit', 'Albanian', 'Tagalog', 'Letzeburgesch', 'Tsonga', 'Malayalam', 'Volapük', 'Zulu', 'Ossetian; Ossetic', 'Samoan', 'Zhuang', 'Bengali', 'Slavic', 'Irish', 'Manx', 'Hungarian', 'Javanese', 'Kanuri', 'Khmer', 'Kirghiz', 'Nauru', 'Ndebele', 'Occitan', 'Romanian', 'Russian', 'Armenian', 'Chamorro', 'No Language', 'Bashkir', 'Galician', 'Ido', 'Luba-Katanga', 'Marshall', 'Malagasy', 'Moldavian', 'Mongolian', 'Ndebele', 'Norwegian', 'Polish', 'Swahili', 'Tajik', 'Tonga', 'Walloon', 'Yiddish', 'English', 'Assamese', 'Gaelic', 'Kalaallisut', 'Burmese', 'Quechua', 'Shona', 'Ukrainian', 'Persian', 'Georgian', 'Gujarati', 'Avaric', 'Avestan', 'Guarani', 'Maltese', 'Nepali', 'Swedish', 'Tatar', 'Wolof', 'Cantonese', 'Chuvash', 'Danish', 'Dzongkha', 'Chichewa; Nyanja', 'Rundi', 'Sotho', 'Turkmen', 'Uzbek', 'Vietnamese', 'Greek', 'Catalan', 'Welsh', 'German', 'Kashmiri', 'Malay', 'Norwegian Bokmål', 'Raeto-Romance', 'Sinhalese', 'Spanish', 'Telugu', 'Twi', 'Pushto', 'Bulgarian', 'Macedonian', 'Inupiaq', 'Korean', 'Lithuanian', 'Oromo', 'Northern Sami', 'Somali', 'Tamil', 'Urdu', 'Amharic', 'Bosnian', 'Divehi', 'Aymara', 'Bambara', 'Yi', 'Interlingue', 'Komi', 'Kurdish', 'Norwegian Nynorsk', 'Mandarin', 'Hebrew', 'Ewe', 'Fijian', 'Fulah', 'Haitian; Haitian Creole', 'Croatian', 'Interlingua', 'Kuanyama', 'Lao', 'Ganda', 'Marathi', 'Sindhi', 'Belarusian', 'Hiri Motu', 'Kongo', 'Slovenian', 'Yoruba'] 


def test_direct_api_calls():
    '''
    Test the API calls that are called directly from the TMDB API without using the server as an intermediary.
    '''
    client = Client(True)
    assert client.get_language_list().sort() == LANGUAGE_LIST.sort()

def test_get_requests_from_server():
    '''
    Test the API calls that are made through the server.
    '''
    client = Client(True)
    assert client.get_genre_list() == GENRE_LIST


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

    assert client.remove_user('test_user', 'test_password') == True #TODO: fix bug
    assert client.remove_user('test_user', 'test_password') == False

    assert client_2.login('test_user', 'test_password') == 0


if __name__ == '__main__':
    #pytest.main()
    test_user_authentication()