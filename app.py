from flask import Flask, jsonify, request
import requests
import base64
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)

# ─── Load environment variables from .env ─────────────────────────────────
OPENWEATHER_API_KEY   = os.getenv("OPENWEATHER_API_KEY")
SPOTIFY_CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# ──────────────────────────────────────────────────────────────────────────────

def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers  = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )
    if resp.status_code == 200:
        return resp.json().get("access_token")
    print("Spotify token error:", resp.text)
    return None

@app.route('/')
def home():
    return jsonify({"message": "Mood‑Based Weather & Spotify API"})

@app.route('/suggestion', methods=['GET'])
def get_suggestion():
    city  = request.args.get('city')
    mood  = request.args.get('mood', '').lower()
    scope = request.args.get('scope', 'regional').lower()

    if not city or not mood:
        return jsonify({"error": "Provide both 'city' and 'mood'"}), 400

    # ─── 1. Fetch weather & country code ────────────────────────────────────────
    w_url  = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    w_resp = requests.get(w_url)
    if w_resp.status_code != 200:
        return jsonify({"error": "Could not fetch weather. Check city name."}), 500
    w = w_resp.json()
    temp    = w["main"]["temp"]
    w_main  = w["weather"][0]["main"].lower()
    desc    = w["weather"][0]["description"]
    country = w["sys"].get("country", None)

    # ─── 2. Base outfit & food by temperature & condition ──────────────────────
    if temp < 5:
        outfit = "Heavy coat, gloves, thermal wear"
        food   = "Hot stew or cocoa"
    elif temp < 15:
        outfit = "Warm jacket and jeans"
        food   = "Soup, hot chocolate"
    elif temp < 25:
        outfit = "Light sweater or hoodie"
        food   = "Warm pasta or toast"
    else:
        outfit = "T-shirt and shorts"
        food   = "Cold salad or smoothie"

    if "rain" in w_main:
        outfit += ", plus umbrella and waterproof shoes"
        food   += ", and hot chai"
    elif "snow" in w_main:
        outfit += ", layered with gloves and boots"
        food   += ", and warm cookies"
    elif "clear" in w_main:
        outfit += ", sunglasses recommended"
    elif "clouds" in w_main:
        outfit += ", maybe a light hoodie"

    # ─── 3. Mood‑based basics ───────────────────────────────────────────────────
    playlists_basic = {
        "tired":    "Lo‑fi chill beats",
        "excited":  "EDM party mix",
        "romantic": "Soft jazz & love songs",
        "lazy":     "Slow acoustic",
        "angry":    "Rock & metal",
        "sad":      "Piano & ballads",
        "motivated":"Gym/workout power mix",
        "anxious":  "Nature sounds & acoustic calm",
        "confident":"High‑energy rap & pop"
    }
    outfit_extras = {
        "tired":    "Add a cozy hoodie",
        "excited":  "Wear vibrant colors",
        "romantic": "Perfume or soft scarf",
        "lazy":     "Stay in pajamas",
        "angry":    "Dark hoodie and boots",
        "sad":      "Warm blanket or soft cardigan",
        "motivated":"Activewear and sneakers",
        "anxious":  "Loose tee and soft cap",
        "confident":"Bold accessories and sunglasses"
    }
    food_extras = {
        "tired":    "Add warm tea or comfort snack",
        "excited":  "Try tacos or fruity treats",
        "romantic": "Strawberries or candle‑lit dessert",
        "lazy":     "Mac & cheese or cereal",
        "angry":    "Spicy noodles or dark coffee",
        "sad":      "Soup or ice cream",
        "motivated":"Protein bar or green smoothie",
        "anxious":  "Herbal tea or oatmeal",
        "confident":"Coffee and energy bites"
    }

    outfit += f". {outfit_extras.get(mood, '')}"
    food   += f". {food_extras.get(mood, '')}"
    basic  = playlists_basic.get(mood, "Your favorite playlist")

    # ─── 4. Spotify search (with randomization & scope) ────────────────────────
    spotify_results = []
    token = get_spotify_token()
    if token:
        params = {"q": mood, "type": "playlist", "limit": 10}
        if scope == "regional" and country:
            params["market"] = country

        sp_resp = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )
        if sp_resp.status_code == 200:
            items = sp_resp.json().get("playlists", {}).get("items", []) or []
            if items:
                # pick up to 3 random playlists
                sample = random.sample(items, k=min(3, len(items)))
                for p in sample:
                    # guard against None entries
                    if not p or not isinstance(p, dict):
                        continue
                    name = p.get("name")
                    url  = p.get("external_urls", {}).get("spotify")
                    if name and url:
                        spotify_results.append({"name": name, "url": url})

    # ─── 5. Final Response ─────────────────────────────────────────────────────
    return jsonify({
        "city":                city.title(),
        "country":             country,
        "mood":                mood,
        "scope":               scope,
        "temperature":         temp,
        "weather_description": desc,
        "outfit":              outfit,
        "food":                food,
        "basic_playlist":      basic,
        "spotify_playlists":   spotify_results
    })

if __name__ == '__main__':
    app.run(debug=True)
