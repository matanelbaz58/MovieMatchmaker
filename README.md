# Movie Recommendation System



## Overview

The **Movie Recommendation System** is a comprehensive web application designed to provide users with personalized movie recommendations based on their preferences. The application integrates with The Movie Database (TMDB) API for fetching movie data and leverages MongoDB for storing user information and search history. Additionally, it offers an optional feature for storing user search history on the Ethereum blockchain using Solidity smart contracts.

This project serves as the final submission for a computer science course, demonstrating practical knowledge in web development, API integration, blockchain technology, and GUI design.

## Features

- **User Registration & Authentication**: Users can register and log in securely. User credentials are stored securely using SHA-256 encryption.
- **Movie Recommendations**: Users can receive movie recommendations based on various filters, including genre, language, release date, and more.
- **Search History**: Users can choose to store their search history in either MongoDB or on the Ethereum blockchain.
- **Graphical User Interface (GUI)**: The application features a user-friendly GUI built with Tkinter, providing easy navigation and interaction.
- **Blockchain Integration**: Offers optional blockchain integration to store search history securely on the Ethereum network.

## Project Structure

- **main.py**: The entry point for the application.
- **api_endpoints.py**: Contains Flask API endpoints for user management, fetching movie recommendations, and handling user preferences.
- **gui.py**: Defines the graphical user interface using Tkinter.
- **python_client.py**: Handles API interactions and manages user sessions.
- **web3_utils.py**: Contains functions and utilities for interacting with the Ethereum blockchain.

## Installation

### Prerequisites

- Python 3.8+
- Pip (Python package manager)
- MongoDB
- Infura account (for Ethereum blockchain integration)


### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   Ensure MongoDB is running on your local machine or on a remote server.

4. **Configure API keys**:
   Replace placeholders in `web3_utils.py` and `api_endpoints.py` with your TMDB API Key and Infura project URL.

5. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### GUI Mode
- Run `python gui.py` to launch the graphical user interface.
- Register or log in to your account.
- Input your preferences and receive personalized movie recommendations.

### API Mode
- Access the Flask API via `localhost:5000`.
- Endpoints include:
  - `/register_mongoDB`: Register a new user.
  - `/login_mongoDB`: Log in as an existing user.
  - `/get_movie_recommendations`: Fetch movie recommendations based on user input.
-

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api) for providing movie data.
- [Infura](https://infura.io/) for blockchain connectivity.
- [MongoDB](https://www.mongodb.com/) for data storage.
 T