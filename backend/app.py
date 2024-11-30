from flask import Flask, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

app = Flask(__name__)
CORS(app)  # Reactからのリクエストを許可

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_youtube_client():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def classify_genre(description):
    keywords = {
        "gaming": ["game", "gaming", "play", "stream"],
        "music": ["music", "song", "band", "album"],
        "education": ["tutorial", "lesson", "learn", "how to"],
        "technology": ["tech", "gadget", "review", "unboxing"],
        "cooking": ["recipe", "cook", "kitchen", "food"]
    }
    for genre, words in keywords.items():
        if any(word.lower() in description.lower() for word in words):
            return genre
    return "other"

@app.route('/fetch-subscriptions', methods=['GET'])
def fetch_subscriptions():
    youtube = get_youtube_client()
    subscriptions = []
    next_page_token = None

    while True:
        request = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            genre = classify_genre(description)
            subscriptions.append({"title": title, "genre": genre})
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return jsonify(subscriptions)

if __name__ == '__main__':
    app.run(debug=True)
