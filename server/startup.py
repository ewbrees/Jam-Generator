
from spotauth import getAuth, refreshAuth, getToken, refreshUserAuth
import os
from datetime import datetime, timedelta


CLIENT_ID= '9e1c093512b543f39810122114e8e68d'
CLIENT_SECRET= '916e504c1c9e48d6baac51600e9d8c2b'
#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"
#Add needed scope from spotify user
SCOPE = "user-read-recently-played playlist-modify-public"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
#TOKEN_DATA = []
TOKEN_DICT = dict

def getUser():
    return getAuth(CLIENT_ID, "https://jam-gen-backend-t6vk3.ondigitalocean.app/callback", SCOPE)
    #return getAuth(CLIENT_ID, "{}:{}/callback".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    #global TOKEN_DICT
    TOKEN_DICT = getToken(code, CLIENT_ID, CLIENT_SECRET, "https://jam-gen-backend-t6vk3.ondigitalocean.app/callback")
    expire_time=datetime.now() + timedelta(hours=1)
    timeCheck={'expires_in': expire_time}
    TOKEN_DICT.update(timeCheck)
    #TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback".format(CALLBACK_URL, PORT))
    return TOKEN_DICT

def refreshToken(time):
    time.sleep(time)
    TOKEN_DICT = refreshAuth()


def refresh_user_token(re_token):
    newToken=refreshUserAuth(re_token, CLIENT_ID, CLIENT_SECRET)
    token_time=(datetime.now() + timedelta(hours=1))
    timeCheck={'expires_in': token_time}
    newToken.update(timeCheck)
    print(newToken)
    return newToken
# def getAccessToken():
#     return TOKEN_DICT["access_token"]

