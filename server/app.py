import logging
from flask import Flask, make_response, request, jsonify, redirect, session
#from flask_session import Session
from flask_cors import CORS
import sqlite3
import os
import uuid
from datetime import datetime
import random
import pprint
# import rsa

from spotcalls import *
import startup
import spotauth

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG) 

app.secret_key='not_secure'
SESSION_TYPE = 'filesystem'
#app.config.from_object(__name__)
#Session(app)

# public_key, private_key = rsa.newkeys(512)



@app.route('/flask_register')
def flask_register():
    # get username
    username = request.args.get('username')
    if username == "":
        return jsonify("username already taken")
    # get password
    password = request.args.get('password')
    if password == "":
        return jsonify("username already taken")
    # if username is not in database, add username and password to database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS userInfo (
                    username TEXT,
                    password TEXT,
                    token TEXT
                );''')


    c.execute("SELECT * FROM userInfo WHERE username = ?", (username,))
    if c.fetchone() is None:
        # generate token
        token = str(uuid.uuid4())
        c.execute("INSERT INTO userInfo (username, password, token) VALUES (?, ?, ?)", (username, password, token))
        conn.commit()
        return jsonify(token)
    # else, return error message
    else:
        return jsonify("username already taken")


@app.route('/display_user_info')
def display_user_info():
    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the users table
    c.execute('SELECT * FROM userInfo')
    users_data = c.fetchall()

    # Close the database connection
    conn.close()

    # Convert the user data to a list of dictionaries
    users = []
    for user in users_data:
        users.append({
            'username': user[0],
            'password': user[1],
            'token': user[2]
        })

    # Return a JSON response with the user data
    return jsonify(users)

@app.route('/flask_login')
def flask_login():
    # get username
    username = request.args.get('username')
    # get password
    if username == "":
        return jsonify("username or password incorrect")
    password = request.args.get('password')
    if password == "":
        return jsonify("username or password incorrect")
    # check if username is in database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    c.execute("SELECT * FROM userInfo WHERE username = ?", (username,))
    user = c.fetchone()
    if user is None:
        return jsonify("username or password incorrect")
    elif user[1] != password:
        return jsonify("username or password incorrect")
    else:
        #return token
        return jsonify(user[2])
    

    

@app.route('/token_to_username')
def token_username():
    #this will take token and return username
    token = request.args.get('token')
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    c.execute("SELECT * FROM userInfo WHERE token = ?", (token,))
    user = c.fetchone()
    if user is None:
        return jsonify("token not found")
    else:
        return jsonify(user[0])
    


@app.route('/login')
def login():
    session['token']=request.args.get('token')
    #print(request.args.get('token'))
    response = startup.getUser()
    #print("went through login")
    #session['token']=str(uuid.uuid4())
    return redirect(response)


@app.route('/callback', methods=["GET", "POST"])
def callback():
    #print("went to /callback")
    creds=startup.getUserToken(request.args['code'])
    #TODO: add timer for refresh
    info= get_user_id(creds['access_token'])
    creds.update(info)
   # print('User object:', creds)
    # saving user info to database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()
    """
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    display_name TEXT,
                    spotify_id TEXT
                );''')

    c.execute("INSERT INTO users (display_name, spotify_id) VALUES (?, ?)", (session['user']['display_name'], session['user']['spotify_id']))
    """
    c.execute('''CREATE TABLE IF NOT EXISTS userData (
                    user_ID TEXT,
                    access_token TEXT,
                    token_type TEXT,
                    expires_in TEXT,
                    refresh_token TEXT,
                    scope TEXT,
                    display_name TEXT,
                    spotify_id TEXT
                );''')

    c.execute("INSERT INTO userData (user_ID, access_token, token_type, expires_in, refresh_token, scope, display_name, spotify_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (session.get('token'), creds['access_token'],creds['token_type'], creds['expires_in'],creds['refresh_token'],creds['scope'], creds['display_name'], creds['spotify_id']) )
    conn.commit()

    # Send user data as message to parent window
    user_data = {
        'display_name': creds['display_name'],
        'spotify_id': creds['spotify_id'],
        'token': session.get('token')
    }
    #return user_data
    #return f'<script>window.opener.postMessage({json.dumps(user_data)}, "https://rgkeeney-ideal-memory-9xgqqr67p4wfpgp7-5000.preview.app.github.dev/");window.close();</script>'
    return f'<script>window.close();</script>'


@app.route('/display_user_creds')
def display_user_creds():
    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the users table
    c.execute('SELECT * FROM userData')
    users_data = c.fetchall()

    # Close the database connection
    conn.close()

    # Convert the user data to a list of dictionaries
    users = []
    for user in users_data:
        users.append({
            'jg token': user[0],
            'access token': user[1],
            #'token': user[2]
        })

    # Return a JSON response with the user data
    return jsonify(users)


@app.route('/users')
def users(): 
    # Connect to the SQLite database
    conn = sqlite3.connect('backend.db')

    # Retrieve the most recently created user from the 'users' table
    c = conn.cursor()
    c.execute("SELECT display_name, spotify_id FROM users ORDER BY rowid DESC LIMIT 1")
    user = c.fetchone()

    # Close the database connection
    conn.close()

    # Convert the user data to a JSON object
    user_data = {'display_name': user[0], 'spotify_id': user[1]}
    json_data = json.dumps(user_data)

    # Return the JSON object
    return json_data

@app.route('/api/save-playlist', methods=['POST'])
#will need to tweak parameters
def save_playlist():
    info=request.get_json()
    # Connect to the database
    appToken= info['token']
    #print(appToken)
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()
    # Query the users table
    c.execute('SELECT * FROM userData WHERE user_ID = ?', (appToken,))
    user_tuple = c.fetchone()
    user_data=list(user_tuple)
    token_time=datetime.strptime(user_data[3],"%Y-%m-%d %H:%M:%S.%f")
    if token_time<datetime.now():
        newCreds=startup.refresh_user_token(user_data[4])
        user_data[1]=newCreds['access_token']
        newtoken=newCreds['access_token']
        newexpire=newCreds['expires_in']
         # Update the token and expire time in the database
        c.execute('UPDATE userData SET access_token = ?, expires_in = ? WHERE user_ID = ?', (newtoken, newexpire, appToken))
    # Close the database connection
    conn.close()
    playlist_name=info['playlist_name']
    songs= info['song_list'].split(", ")
    urilist  = [val for val in songs if val.startswith("spotify")]
    result = ', '.join(urilist)
    urijson={"uris": urilist}
    #print(urijson)
    playlist_info=make_playlist(user_data[1], user_data[7], {"name": playlist_name})
    #checkID is the unique number associated with the playlist, kept for debugging
    checkID=fill_playlist(user_data[1] ,playlist_info['id'], urijson)
    #returning link to playlist
    #print(playlist_info['url'])
    #return jsonify(playlist_info['url'])
    return playlist_info['url']


@app.route('/api/submit-genre', methods=['GET','POST'])
def submit_genre():
    #print("got to submit genre")
    #name=session.get('user')
    #print(name)
    try:
        genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]

        # Retrieve the genre data from the request body
        genre = request.get_json()['genre']
        #print(f"Received genre: {genre}")
        if genre == 'random':
            genre = random.choice(genres)
            #print(f"Random genre: {genre}")

        # Retrieve the playlistname data from the request body
        playlistname = request.get_json()['playlistname']
        # print(f"Received playlistname: {playlistname}")
        # Retrieve popularity target from the request body
        popularity = request.get_json()['popularity']
        # print(f"Received popularity: {popularity}")
        popularity = str(popularity)
        if not popularity.isnumeric():
            popularity = "50"
        if int(popularity) > 100 or int(popularity) < 0:
            popularity = "50"

        # Retrieve the number of songs data from the request body
        numSongs = request.get_json()['numSongs']
        # print(f"Received numSongs: {numSongs}")
        numSongs = str(numSongs)
        if not numSongs.isnumeric():
            numSongs = "10"
    

        # Retrieve the seed artist data from the request body
        seedArtist = request.get_json()['seedArtist']
        # print(f"Received seedArtist: {seedArtist}")

        # Retrieve the seed track data from the request body
        seedTrack = request.get_json()['seedTrack']
        # print(f"Received seedTrack: {seedTrack}")

        # Retrieve the mood data from the request body
        mood = request.get_json()['mood']
        # print(f"Received mood: {mood}")

        owner = request.get_json()['owner'] 
        # print(f"Received owner: {owner}")

        # Define a dictionary to map moods to danceability and acousticness values
        mood_map = {
            'default': {'danceability': 0.5, 'acousticness': 0.5, 'energy': 0.5, 'speechiness': 0.5},
            'happy': {'danceability': 0.7, 'acousticness': 0.1, 'energy': 1.0, 'speechiness': 0.8},
            'party': {'danceability': 1.0, 'acousticness': 0.1, 'energy': 1.0, 'speechiness': 0.8},
            'focus': {'danceability': 0.1, 'acousticness': 1.0, 'energy': 0.3, 'speechiness': 0},
            'chill': {'danceability': 0.2, 'acousticness': 0.7, 'energy': 0.1, 'speechiness': 0.5},
            'sad': {'danceability': 0.1, 'acousticness': 0.5, 'energy': 0.1, 'speechiness': 0.5},
            'sleep': {'danceability': 0, 'acousticness': 1.0, 'energy': 0, 'speechiness': 0},
            'motivated': {'danceability': 0.5, 'acousticness': 0.3, 'energy': 1, 'speechiness': 0.9},
            'random': {'danceability': random.uniform(0, 1), 'acousticness': random.uniform(0, 1), 'energy': random.uniform(0, 1), 'speechiness': random.uniform(0, 1)},
            'relax': {'danceability': 0.3, 'acousticness': 0.8, 'energy': 0.2, 'speechiness': 0.2},
            'upbeat': {'danceability': 0.8, 'acousticness': 0.2, 'energy': 0.9, 'speechiness': 0.6},
            'romantic': {'danceability': 0.4, 'acousticness': 0.6, 'energy': 0.3, 'speechiness': 0.4},
            'energetic': {'danceability': 0.9, 'acousticness': 0.1, 'energy': 1.0, 'speechiness': 0.7},
            'calm': {'danceability': 0.2, 'acousticness': 0.9, 'energy': 0.3, 'speechiness': 0.2},
            'inpirational': {'danceability': 0.5, 'acousticness': 0.2, 'energy': 0.7, 'speechiness': 0.8},
            'confident': {'danceability': 0.7, 'acousticness': 0.1, 'energy': 0.9, 'speechiness': 0.8}
        }

        moods = list(mood_map.keys())

        if mood == 'random':
            mood = random.choice(moods)
            print(f"Random genre: {mood}")

        # Look up the danceability and acousticness values for the given mood
        danceability, acousticness, energy, speechiness = mood_map[mood]['danceability'], mood_map[mood]['acousticness'], mood_map[mood]['energy'], mood_map[mood]['speechiness']


        # TODO: incorporate popularity, mood, seedArtist, seedTrack into the query
        #queries api for 10 songs available in the US, with the given genre, and empty strings for seed artists and tracks
        data = query_api([numSongs, "US", genre, seedArtist, seedTrack, popularity, danceability, acousticness, energy, speechiness])

        # Create a unique ID for the playlist
        playlist_id = str(uuid.uuid4())

        # Get the current date and time
        now = datetime.now()

        # Connect to the database
        conn = sqlite3.connect('backend.db')
        c = conn.cursor()


        # Create the new table if it doesn't exist
        # need to add more fields
        # TODO: add img, link, album, popularity(maybe), explicit, change ms to seconds
        c.execute('''CREATE TABLE IF NOT EXISTS generated_playlists (
                    playlist_id TEXT UNIQUE, 
                    playlist_name TEXT, 
                    song_list TEXT
                );''')

        # Create the new table if it doesn't exist
        c.execute(''' CREATE TABLE IF NOT EXISTS playlist_info (
            id TEXT UNIQUE,
            name TEXT,
            genre TEXT,
            owner TEXT,
            created_at TEXT
        );''')

        
        # Initialize the list for storing song names
        song_info_list = []

        
        

        c.execute('INSERT INTO playlist_info (id, name, genre, owner, created_at) VALUES (?, ?, ?, ?, ?)',
                  (playlist_id, playlistname, genre, owner, now))
        
        # Insert the tracks data into the songs table
        for track in data['tracks']:
            seconds, _ = divmod(track['duration_ms'], 1000)
            minutes, seconds = divmod(seconds, 60)
            duration_formatted = '{:d}:{:02d}'.format(minutes, seconds)

            # add song info to list
            # print()
            song_info = f"{track['name']}|| {track['artists'][0]['name']}|| {duration_formatted}|| {track['popularity']}|| {track['explicit']}|| {track['album']['name']}|| {track['external_urls']['spotify']}|| {track['album']['images'][0]['url']}|| {track['uri']}"
            song_info_list.append(song_info)
       
        # Join the song names into a single string
        song_list = '|| '.join(song_info_list)

        # Insert the data into the generated_playlists table
        c.execute('INSERT INTO generated_playlists (playlist_id, playlist_name, song_list) VALUES (?, ?, ?)',
                  (playlist_id, playlistname, song_list))
        
        # Save the changes to the database and close the connection
        conn.commit()
        conn.close()


        """
        Example data:

        playlist_info table:
        id                                      name            genre        owner     created_at
        --------------------------------------------------  ------------  --------  -------------------
        a039b7e6-4925-4de9-b5b5-2e6602a0c2b7    My Playlist     Rock        Alice     2023-04-12 10:30:00

        generated_playlists table:
        playlist_id                             playlist_name   song_list
        --------------------------------------  --------------  --------------------------------------------------
        a039b7e6-4925-4de9-b5b5-2e6602a0c2b7    My Playlist     Song 1 by Artist 1 (180 ms), Song 2 by Artist 2 (240 ms), Song 3 by Artist 3 (210 ms)
        
        """

        # print(data['tracks'] + "was stored in the db")
        return jsonify(data['tracks'])
    except Exception as e:
        logging.exception("Error submitting the genre")  # Log the error
        return make_response(jsonify({"error": str(e)}), 500)  # Return a 500 Internal Server Error response with the error message




@app.route('/api/display_playlist_info', methods=['GET']) 
def display_playlists():
    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the playlists table
    c.execute('SELECT * FROM playlist_info')
    playlists_data = c.fetchall()

    # Close the database connection
    conn.close()

    # Convert the playlist data to a list of dictionaries
    playlists = []
    for playlist in playlists_data:
        playlists.append({
            'id': playlist[0],
            'name': playlist[1],
            'genre': playlist[2],
            'owner': playlist[3],
            'created_at': playlist[4]
        })

    # Return a JSON response with the playlist data
    return jsonify(playlists)

    

@app.route('/api/display_generated_playlists', methods=['GET'])
# Displays the playlists and their songs

def display_playlist_data():
    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the generated_playlists table
    c.execute('SELECT * FROM generated_playlists')
    results = c.fetchall()

    # Close the connection
    conn.close()

    # Prepare the results as a list of dictionaries
    output = []
    for row in results:
        output.append({
            'playlist_id': row[0],
            'playlist_name': row[1],
            'song_list': row[2]
        })

    # Return the results as a JSON object
    return jsonify(output)

@app.route('/api/get_data_by_id', methods=['GET'])
# return the playlist data for a specific playlist
def get_data_by_id():
    # Get the playlist name query parameter from the request
    playlist_id = request.args.get('Id')

    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the generated_playlists table and filter by playlist_name
    c.execute('SELECT * FROM generated_playlists WHERE playlist_id = ?', (playlist_id,))

    results = c.fetchall()

    # Close the connection
    conn.close()

    # Prepare the results as a list of dictionaries
    output = []
    for row in results:
        output.append({
            'playlist_id': row[0],
            'playlist_name': row[1],
            'song_list': row[2]
        })

    # Return the results as a JSON object
    return jsonify(output)

@app.route('/api/get_data_by_owner', methods=['GET'])
# return the playlist data for a specific playlist
def get_data_by_owner():
    # Get the playlist name query parameter from the request
    owner = request.args.get('owner')
    # print(owner)
    if owner == "":
        #print("owner is empty")
        owner = "guest"

    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Query the generated_playlists table and filter by playlist_name
    c.execute('SELECT * FROM playlist_info WHERE owner = ? ORDER BY created_at DESC', (owner,))
    results = c.fetchall()

    # Close the connection
    conn.close()

    # Prepare the results as a list of dictionaries
    output = []
    for row in results:
        output.append({
            'playlist_id': row[0],
            'playlist_name': row[1],
            'song_list': row[2]
        })

    # Return the results as a JSON object
    return jsonify(output)


@app.route('/api/delete_data_by_id', methods=['GET'])
# return the playlist data for a specific playlist
def delete_data():
    # Get the playlist ID query parameter from the request
    playlist_id = request.args.get('Id')

    # Connect to the database
    conn = sqlite3.connect('backend.db')
    c = conn.cursor()

    # Delete the record from the playlist_info table
    c.execute('DELETE FROM playlist_info WHERE id = ?', (playlist_id,))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    # Return a success message
    return jsonify({'message': 'Successfully deleted playlist'})






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

