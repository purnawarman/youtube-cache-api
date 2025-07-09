[Ifrom flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Simpan cache di memory
cached_video_id = None
last_updated = 0
CACHE_DURATION = 60  # detik

# Ganti dengan channelId dan API key Mas
CHANNEL_ID = "UC7ijSJ_SyRqg_MqoGedoZTA"
YOUTUBE_API_KEY = "AIzaSyDGkN89EiV9KZDeul-1f7R-iFmXjbl2M18"

def get_live_video_id():
    global cached_video_id, last_updated
    now = time.time()
    if cached_video_id and now - last_updated < CACHE_DURATION:
        return cached_video_id

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        "?part=snippet"
        f"&channelId={CHANNEL_ID}"
        "&eventType=live"
        "&type=video"
        f"&key={YOUTUBE_API_KEY}"
    )

    resp = requests.get(url)
    data = resp.json()
    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"]["videoId"]
        cached_video_id = video_id
        last_updated = now
        return video_id
    return None

@app.route("/video-id", methods=["GET"])
def video_id():
    vid = get_live_video_id()
    if vid:
        return jsonify({"videoId": vid})
    return jsonify({"message": "No live video"}), 404

