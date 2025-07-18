
## Mood-Based Weather & Spotify Suggestion API

An advanced, beginner-friendly Flask API that combines weather data and user mood to provide personalized outfit recommendations, music playlist suggestions, and food ideas. It integrates with OpenWeatherMap for real-time weather data and uses the Spotify Web API to fetch mood-based playlists, supporting both regional and international scopes with randomized results.

----------

### 🏗️ Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Environment Variables](#environment-variables)  
5. [Running the Application](#running-the-application)  
6. [API Endpoints](#api-endpoints)  
   - [GET `/`](#get-)  
   - [GET `/suggestion`](#get-suggestion)  
7. [Request Parameters](#request-parameters)  
8. [Response Schema](#response-schema)  
9. [Error Handling](#error-handling)  
10. [Examples](#examples)  
11. [Deployment](#deployment)  
12. [Contributing](#contributing)  
13. [License](#license)  

----------

## Features

-   🔄 **Real-time Weather Data** via OpenWeatherMap
    
-   🎶 **Spotify Integration** using Client Credentials Flow
    
-   🌍 **Regional & International** playlist scope
    
-   🔀 **Randomized** playlist selection on each request
    
-   🧥 Outfit suggestions based on temperature and conditions
    
-   🍲 Food recommendations warming or cooling based on weather and mood
    

----------

## Prerequisites

-   Python 3.7+ installed
    
-   pip (Python package manager)
    
-   A free account and API key from [OpenWeatherMap](https://openweathermap.org/api)
    
-   A free Spotify account and [Spotify Developer App](https://developer.spotify.com/dashboard) credentials
    

----------

## Installation

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/Devang-IO/mood_weather_spotify_api.git
    cd mood_weather_spotify_api
    
    ```
    
2.  Create and activate a virtual environment:
    
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    
    ```
    
3.  Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

----------

## Environment Variables

Create a `.env` file in the project root with the following:

```ini
OPENWEATHER_API_KEY=your_openweather_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

```

Load these variables in `app.py` using `python-dotenv` or manually set them in your environment.

----------

## Running the Application

Start the Flask server in development mode:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
# or
python app.py

```

The API will be available at `http://127.0.0.1:5000/` (for local development)  
The live version is available at `https://mood-weather-api.onrender.com/`

----------

## API Endpoints

### GET `/`

-   **Description:** Health check endpoint
    
-   **Response:**
    
    ```json
    { "message": "Mood‑Based Weather & Spotify API" }
    
    ```
    

### GET `/suggestion`

-   **Description:** Provides personalized outfit, playlist, and food suggestions
    
- **Query Parameters:** see [Request Parameters](#request-parameters)
  
- **Response:** see [Response Schema](#response-schema)

    

----------

## Request Parameters

| Parameter | Type   | Required | Default    | Description                                           |
|-----------|--------|----------|------------|-------------------------------------------------------|
| city      | string | yes      | -          | Name of the city (e.g., `Delhi`, `Paris`)           |
| mood      | string | yes      | -          | User's mood (e.g., `excited`, `tired`, `romantic`)  |
| scope     | string | no       | `regional` | `regional` or `international` for playlist market selection |

----------

## Response Schema

```json
{
  "city": "Delhi",
  "country": "IN",
  "mood": "excited",
  "scope": "regional",
  "temperature": 34.5,
  "weather_description": "clear sky",
  "outfit": "T-shirt and shorts, sunglasses recommended. Wear vibrant colors",
  "food": "Cold salad or smoothie. Try tacos or fruity treats",
  "basic_playlist": "EDM party mix",
  "spotify_playlists": [
    { "name": "Playlist 1", "url": "https://open.spotify.com/..." },
    { "name": "Playlist 2", "url": "https://open.spotify.com/..." },
    { "name": "Playlist 3", "url": "https://open.spotify.com/..." }
  ]
}

```

----------

## Error Handling

-   **400 Bad Request:** Missing `city` or `mood` parameter
    
-   **500 Internal Server Error:** Issues fetching from OpenWeather or Spotify APIs
    

Responses include an `error` field with details.

----------

## Examples

```bash
# Default regional scope
curl "http://127.0.0.1:5000/suggestion?city=Berlin&mood=motivated"

# International playlists
curl "http://127.0.0.1:5000/suggestion?city=Tokyo&mood=lazy&scope=international"

```

----------

## Deployment

You can deploy this Flask app to platforms like:

-   **Heroku**
    
-   **Render**
    
-   **AWS Elastic Beanstalk**
    

Make sure to set environment variables and adjust the start command (e.g., `gunicorn app:app`).

----------

## Contributing

1.  Fork the repository
    
2.  Create a feature branch: `git checkout -b feature/YourFeature`
    
3.  Commit your changes: `git commit -m "Add YourFeature"`
    
4.  Push to the branch: `git push origin feature/YourFeature`
    
5.  Open a Pull Request
    

Please adhere to the code style and add tests where appropriate.

----------

## License

This project is licensed under the MIT License. See [MIT License](https://opensource.org/licenses/MIT) for details.
