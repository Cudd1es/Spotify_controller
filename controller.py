import json
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#get user credential
with open("credentials.json", "r") as creds:
    data = json.load(creds)
    CLIENT_ID = data.get("CLIENT_ID")
    CLIENT_SECRET = data.get("CLIENT_SECRET")
    REDIRECT_URI = data.get("SPOTIPY_REDIRECT_URI")
scope = ""
scope += "user-read-currently-playing "
scope += "user-read-playback-state "
scope += "user-modify-playback-state "

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-modify-playback-state user-read-playback-state"))


#tool to get info from returned json
#usage: get_basic_info(info["FIELD_TO_COLLECT_INFO"])
def get_basic_info(info):
    if info:
        track_id = info["id"]
        track_name = info["name"]
        track_artist = info["artists"][0]["name"]
        track_album = info["album"]["name"]
    else:
        track_id = None
        track_name = None
        track_artist = None
        track_album = None
    ret_info = {
        "track_id": track_id,
        "track_name": track_name,
        "track_artist": track_artist,
        "track_album": track_album
    }
    return ret_info


#get information of the track playing now
def get_track_info():
    info = sp.current_user_playing_track()
    if not info:
        is_playing = False
        return None
    else:
        is_playing = info["is_playing"]
        ret_info = get_basic_info(info["item"])
        ret_info["is_playing"] = is_playing
        return ret_info


#get the information of current queue
def get_queue():
    info = sp.queue()
    if info:
        ret_info = {}
        current_info = get_basic_info(info["currently_playing"])
        queue_infos = []
        index = 0
        for queue_item_info in info["queue"]:
            index += 1
            queue_item = get_basic_info(queue_item_info)
            queue_item["track_index"] = index
            queue_infos.append(queue_item)
        ret_info["current_info"] = current_info
        ret_info["queue"] = queue_infos
        return ret_info
    else:
        return None


user_profile = sp.current_user()
print(f"Welcome, {user_profile['display_name']}")

input_val = "-1"
track_info = get_track_info()
while input_val != "0":
    if not track_info:
        print("Nothing playing now")
        break
    prompt = f"|now playing {track_info['track_name']} by {track_info['track_artist']}|"

    input_val = input("_"*len(prompt)+f"\n{prompt}\n" +"-"*len(prompt)+
                      "\nenter your command\n"
                      "0. exit 1. PREVIOUS ⏮  2. PLAY/PAUSE ⏯ 3. NEXT ⏭ \n")
    if input_val == "1":
        sp.previous_track()
    elif input_val == "2":
        if track_info["is_playing"]:
            sp.pause_playback()
        else:
            sp.start_playback()
    elif input_val == "3":
        sp.next_track()
    else:
        continue
    track_info = get_track_info()


