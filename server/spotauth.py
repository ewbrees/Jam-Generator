import base64, json, requests

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token'
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
    
def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri
    }
            
    #encoded = base64.b64encode("{}:{}".format(client_id, client_secret))
    #encoded = base64.urlsafe_b64encode("{}:{}".format(client_id, client_secret))
    encoded = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    #headers = {"Authorization" : "Basic {}".format(encoded), "Content-Type" : HEADER} 
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % encoded.decode('ascii')
    }
    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    #postjson = json.loads(post.text)
    #print("from spotauth getToken: ")
    #print(json.loads(post.text))
    #return postjson
    return json.loads(post.text)
    #return handleToken(json.loads(post.text))

def handleToken(response):
    #auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    auth_head = {"token_type": "Bearer"}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def refreshAuth():
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=HEADER)
    p_back = json.dumps(post_refresh.text)
    
    return handleToken(p_back)


def refreshUserAuth(re_token, client_id, client_secret):
    encoded = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % encoded.decode('ascii')
    }
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : re_token
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)
    p_back = json.loads(post_refresh.text)
    
    return p_back

