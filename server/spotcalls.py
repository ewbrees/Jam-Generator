import spotipy
import pprint
import requests
import random
import sys
import os
import time
import pickle
import json
from spotipy.oauth2 import SpotifyClientCredentials
#need to install: spotipy, requests
#credentials go here (will need a workflow to )

#Add your client ID
CLIENT_ID = '9e1c093512b543f39810122114e8e68d'
CLIENT_SECRET = '916e504c1c9e48d6baac51600e9d8c2b'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))
#current redirect URI is same as for local machine, may need to change
REDIRECT_URI = "http://localhost:3000/callback"
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


##THIS IS CURRENTLY UGLY AND BAD- need to make caching work but currently "good enough"
def acquire_token():
   token_cache_dir = os.path.join(ROOT_PATH, "cache")
   token_cache_file = os.path.join(token_cache_dir, "token.p")
   if os.path.exists(token_cache_file):
      current_time = time.time()
      if current_time - os.path.getmtime(token_cache_file) < 3600:
         #with open(token_cache_file, "rb") as fid:
         #      token = pickle.load(fid)
         return token
      else:
         grant_type = 'client_credentials'
         body_params = {'grant_type' : grant_type}
         url = 'https://accounts.spotify.com/api/token'
         response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
         token_raw = json.loads(response.text)
         token = token_raw["access_token"]
         #with open(token_cache_file, "wb") as fid:
         #      pickle.dump(token, fid)
         return token
   else:
      grant_type = 'client_credentials'
      body_params = {'grant_type' : grant_type}
      url = 'https://accounts.spotify.com/api/token'
      response = requests.post(url, data=body_params, auth=(CLIENT_ID , CLIENT_SECRET))
      token_raw = json.loads(response.text)
      token = token_raw["access_token"]
      #with open(token_cache_file, "wb") as fid:
      #   pickle.dump(token, fid)
      return token

#import startup
def define_settings():
    """
    Sets the endpoint as well as defines the token.
    """
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    #token = startup.getAccessToken()
    token=acquire_token()
    settings = [endpoint_url, token]
    return settings

def fetch_artist_genre(artist_id):
   endpoint_url = f'https://api.spotify.com/v1/artists/{artist_id}'
   query = f'{endpoint_url}'
   settings = define_settings()
   #response = requests.get(query,
   #                        headers={"Content-Type":"application/json",
   #                               "Authorization":f"Bearer {settings[1]}"})
   response = requests.get(query, headers={"Content-Type":"application/json",
                                  "Authorization":f"Bearer {settings[1]}"})
   json_response = response.json()
   genres = json_response['genres']
   try:
      index = random.randint(0, len(genres)-1)
   except:
      print("Spotify doesn't store genres for this artist, please try another one!")
      sys.exit()
   for g in genres:
       genre = genres[index]
   return genre
   #return genres


def get_artistID(artists):
   if isinstance(artists, str):
      results = sp.search(q='artist:' + artists, type='artist')
      items = results['artists']['items']
      artist_ID = items[0]['id']
   else:
      placeholder=[]
      for artist in artists:
         results = results = sp.search(q='artist:' + artist, type='artist')
         items = results['artists']['items']
         placeholder.append(items[0]['id'])
      artist_ID = ','.join(placeholder)
   return artist_ID

def get_trackID(tracks):
   if isinstance(tracks, str):
      results = sp.search(q='track:' + tracks, type='track')
      items = results['tracks']['items']
      track_ID = items[0]['id']
   else: 
      placeholder=[]
      for track in tracks:
         results = sp.search(q='track:' + track, type='track')
         items = results['tracks']['items']
         placeholder.append(items[0]['id'])
      track_ID = ','.join(placeholder)
   return track_ID

def query_api(filters):
    settings = define_settings()
    artist_id=get_artistID(filters[3])
    track_id = get_trackID(filters[4])
    query = f'{settings[0]}limit={filters[0]}&market={filters[1]}&seed_genres={filters[2]}'
    query += f'&seed_artists={artist_id}'
    query += f'&seed_tracks={track_id}'
    query += f'&target_popularity={filters[5]}'
    query += f'&target_danceability={filters[6]}'
    query += f'&target_acousticness={filters[7]}'
    query += f'&target_energy={filters[8]}'
    query += f'&target_speechiness={filters[9]}'
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {settings[1]}"})
    json_response = response.json()
   #  for idx, vals in enumerate(json_response['tracks']):
   #     print(f"{idx+1} {vals['name']} by {vals['artists'][0]['name']} {vals['external_urls']}")
    return json_response

# query_api([10, "US", "random", ["Rooftops", "cassiopeia"], "Rhythm"])
# query_api([10,"US", "", "Drake", "Only", 80, 0.5, 0.5, 0.5, 0.5])

def get_user_id(token):
   endpoint = f'https://api.spotify.com/v1/me'
   response = requests.get(endpoint,
                            headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {token}"})
   jsr = response.json()
   #output = f"Logged in with display name {jsr['display_name']} and the unique id {jsr['id']}"
   output = {"display_name" : jsr['display_name'], "spotify_id" : jsr['id']}
   return output

def make_playlist(token, user_id, playlist_info):
   endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
   body=json.dumps(playlist_info)
   response = requests.post(endpoint,
                           headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {token}"},
                           data=body)
   txtresp=json.loads(response.text)
   result= {'id': txtresp['id'], 'url': txtresp['external_urls']}
   return result

def fill_playlist(token, playlist_id, uris):
   endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
   result=requests.post(endpoint,
                           headers={"Content-Type":"application/json",
                                     "Authorization":f"Bearer {token}"},
                           data=json.dumps(uris))
   return json.loads(result.text)
   
