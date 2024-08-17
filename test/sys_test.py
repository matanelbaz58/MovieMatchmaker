import requests
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python_client import Client

GENRE_LIST = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}
LANGUAGE_LIST = ['Abkhazian', 'Afar', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Aragonese', 'Armenian', 'Assamese', 'Avaric', 'Avestan', 'Aymara', 'Azerbaijani', 'Bambara', 'Bashkir', 'Basque', 'Belarusian', 'Bengali', 'Bislama', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Cantonese', 'Catalan', 'Chamorro', 'Chechen', 'Chichewa; Nyanja', 'Chuvash', 'Cornish', 'Corsican', 'Cree', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'Dzongkha', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Faroese', 'Fijian', 'Finnish', 'French', 'Frisian', 'Fulah', 'Gaelic', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian; Haitian Creole', 'Hausa', 'Hebrew', 'Herero', 'Hindi', 'Hiri Motu', 'Hungarian', 'Icelandic', 'Ido', 'Igbo', 'Indonesian', 'Interlingua', 'Interlingue', 'Inuktitut', 'Inupiaq', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kalaallisut', 'Kannada', 'Kanuri', 'Kashmiri', 'Kazakh', 'Khmer', 'Kikuyu', 'Kinyarwanda', 'Kirghiz', 'Komi', 'Kongo', 'Korean', 'Kuanyama', 'Kurdish', 'Lao', 'Latin', 'Latvian', 'Letzeburgesch', 'Limburgish', 'Lingala', 'Lithuanian', 'Luba-Katanga', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Mandarin', 'Manx', 'Maori', 'Marathi', 'Marshall', 'Moldavian', 'Mongolian', 'Nauru', 'Navajo', 'Ndebele', 'Ndonga', 'Nepali', 'No Language', 'Northern Sami', 'Norwegian', 'Norwegian Bokmål', 'Norwegian Nynorsk', 'Occitan', 'Ojibwa', 'Oriya', 'Oromo', 'Ossetian; Ossetic', 'Pali', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Pushto', 'Quechua', 'Raeto-Romance', 'Romanian', 'Rundi', 'Russian', 'Samoan', 'Sango', 'Sanskrit', 'Sardinian', 'Serbian', 'Serbo-Croatian', 'Shona', 'Sindhi', 'Sinhalese', 'Slavic', 'Slovak', 'Slovenian', 'Somali', 'Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swati', 'Swedish', 'Tagalog', 'Tahitian', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tigrinya', 'Tonga', 'Tsonga', 'Tswana', 'Turkish', 'Turkmen', 'Twi', 'Uighur', 'Ukrainian', 'Urdu', 'Uzbek', 'Venda', 'Vietnamese', 'Volapük', 'Walloon', 'Welsh', 'Wolof', 'Xhosa', 'Yi', 'Yiddish', 'Yoruba', 'Zhuang', 'Zulu']

@pytest.mark.parametrize("use_cache", [True, False])
def test_direct_api_calls(use_cache):
    '''
    Test the API calls that are called directly from the TMDB API without using the server as an intermediary.
    '''
    client = Client(use_cache)
    assert client.get_list_for_gui_dropdown('language') == sorted(LANGUAGE_LIST)
    assert client.get_list_for_gui_dropdown('genre') == sorted(list(GENRE_LIST.keys()))
    assert client.get_list_for_gui_dropdown('sort_by') == ['popularity', 'release date', 'vote average']
   

    

@pytest.mark.parametrize("use_cache", [True, False])
def test_get_requests_from_server(use_cache):
    '''
    Test the API calls that are made through the server.
    '''
    client = Client(use_cache)
    assert client.get_genre_dict() == GENRE_LIST



@pytest.mark.parametrize("is_mongo_db_client, register_data, login_data, expected_login_results, allow_duplicate_registration", [
    # MongoDB test case
    (True, 
     ('test_user', 'test_password'), 
     [('rong_name', 'test_password', 0), ('test_user', 'rong_password', 2), ('test_user', 'test_password', 1)], 
     True,
     False),  # Duplicate registration should fail for MongoDB

    # Web3 test case
    (False, 
     ('0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B', '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a'), # Correct credentials
     [('0x5551f3581Ba3c9193832Bb5b2c44487E5BB0190B', '7bdf8381908bee6ee141616efb1f74b5f76278f66b1a83b1178e364db0d3969b', 2), # Wrong address
      ('0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B', '7bdf8381908bee6ee141616efb1f74b5f76278f66b1a83b1178e364db0d3969a', 2), # Wrong private key
      ('0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B', '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a', 1)], # Correct credentials
     False,
     True)  # Duplicate registration should not fail for Web3
])
def test_authentication(is_mongo_db_client, register_data, login_data, expected_login_results, allow_duplicate_registration):
    '''
    Test user registration, login, and removal for both MongoDB and Web3 clients.
    '''
    client = Client(is_mongo_db_client=is_mongo_db_client)
    
    # Registration tests
    assert client.register_user(*register_data) == True
    if not allow_duplicate_registration:
        assert client.register_user(*register_data) == False  # Duplicate registration should fail for MongoDB
    else:
        assert client.register_user(*register_data) == True  # Duplicate registration should pass for Web3

    # Login tests
    for username, password, expected_result in login_data:
        client_2 = Client(is_mongo_db_client=is_mongo_db_client)
        assert client_2.login(username, password) == expected_result

    # User removal tests
    assert client.remove_user() == expected_login_results
    assert client.remove_user() == False  # Trying to remove non-existent user

    client_2 = Client(is_mongo_db_client=is_mongo_db_client)
    if is_mongo_db_client:
        assert client_2.login(register_data[0], register_data[1]) == 0
    else:
        assert client_2.login(register_data[0], register_data[1]) == 1



def test_user_history():
    '''
    test the user history
    '''
    # TODO: test getting recommendations by history before adding any history

    client = Client(True)
    client.register_user('test_user', 'test_password')
    assert client.get_user_history() == {}
    movie_recomend = client.get_movie_recommendations(user_input={'language': 'English', 'genre': 'Comedy', 'with_cast': 'Tom Cruise'}) 
    assert type(movie_recomend) == list
    assert len(movie_recomend) == 10

    assert client.get_user_history() == {'language': {'English': 1}, 'genre': {'Comedy': 1}, 'with_cast': {'Tom Cruise': 1}}
    client.get_movie_recommendations(user_input={'language': 'English', 'genre': 'Comedy', 'with_cast': 'Leonardo DiCaprio'})
    assert client.get_user_history() == {'language': {'English': 2}, 'genre': {'Comedy': 2}, 'with_cast': {'Tom Cruise': 1, 'Leonardo DiCaprio': 1}}
    client.get_movie_recommendations(user_input={'with_cast': 'Tom Cruise', 'sort_by': 'popularity'})
    assert client.get_user_history() == {'language': {'English': 2}, 'genre': {'Comedy': 2}, 'with_cast': {'Tom Cruise': 2, 'Leonardo DiCaprio': 1}, 'sort_by': {'popularity': 1}}
    
    movie_recomend = client.get_movie_recommendations_by_histoy()
    assert type(movie_recomend) == list
    assert len(movie_recomend) == 10

    client.clear_user_history()
    assert client.get_user_history() == {}

    client.remove_user()


def test_web3_history():
    '''
    test the user history
    '''
    wallet_address = '0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B'
    private_key = '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a'
    
    client = Client(is_mongo_db_client=False)
    client.login(wallet_address, private_key)
    
    client.clear_user_history()
    assert client.get_user_history() == {}

    movie_resaults, tx_hash_link = client.get_movie_recommendations(user_input={'language': 'English', 'genre': 'Comedy', 'with_cast': 'Tom Cruise'}) 
    print(tx_hash_link)
    assert client.get_user_history() == {'language': {'English': 1}, 'genre': {'Comedy': 1}, 'with_cast': {'Tom Cruise': 1}}
    movie_resaults, tx_hash_link = client.get_movie_recommendations(user_input={'language': 'English', 'genre': 'Comedy', 'with_cast': 'Leonardo DiCaprio', 'sort_by': 'popularity'})
    assert client.get_user_history() == {'language': {'English': 2}, 'genre': {'Comedy': 2}, 'with_cast': {'Tom Cruise': 1, 'Leonardo DiCaprio': 1}, 'sort_by': {'popularity': 1}}
    
    assert type(movie_resaults) == list
    assert len(movie_resaults) == 10

    assert type(tx_hash_link) == str
    assert len(tx_hash_link) == 98
    assert tx_hash_link[:34] == 'https://sepolia.etherscan.io/tx/0x'

    movie_recomend = client.get_movie_recommendations_by_histoy() 
    assert type(movie_recomend) == list
    assert len(movie_recomend) == 10

    client.clear_user_history()
    assert client.get_user_history() == {}

    assert client.remove_user() == False

    

     


if __name__ == '__main__':
    # pytest.main(['-k', 'test_direct_api_calls'])
    # pytest.main(['-k', 'test_get_requests_from_server'])
    # pytest.main(['-k', 'test_authentication'])
    # pytest.main(['-k', 'test_user_history'])
    # pytest.main(['-k', 'test_web3_history'])

    # test_web3_history()
    # test_web3_history()

    pytest.main()
    
    
    