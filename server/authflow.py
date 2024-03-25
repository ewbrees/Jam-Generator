from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.jose import jwt, JsonWebKey
import startup
from spotcalls import *
from spotauth import  *
app = Flask(__name__)
app.secret_key='not_secure'

jwk={
  "alg": "RS256",
  "d": "SCSLEO5fCrvtwQU_R8v0H_ihZSlKqZNozT9KkPWhJlhoYfXyJBJWvfTn1KeRHJnNBiTxdod0weoB8tt3qvH_zwedq9N3itiWCwxLOnZjxYzyPdh4DkMqUG_8lKLegl6bSHlyCSthf1FGOMkayI-H5db47fmHLHwKwIM0vQLZS5uutkqYjiUCnF1CbludZ6CYv3HYbgsbytjBA99h9t_gPTgDgQj2htnRV-UGQdNjAkCR9nl970ERm1d5sDpmFWj6Qg1xScl1Z4RCv3jrfH8RgYFLa9L11NW7aEVmtqLQSNhmipyLeDJmJOQz2V5zSbYgqlZ8bD0EP3QiIxd6-NKFUCP9D24cGFaTJ_KFAxOa_vqZiGRLF23DBkPpUkJspJG9AQQkp_bimzYlin_I0g7wOyIVGdQ7IsvP8unwGcF6yWZ8HKnnfaGH6X6vpS6Akn1CuDexF3KGZw_NFOycQTb4K9dO8eECYxxV7VpTA7gTTYPwHJOU2tZs9_h7aDjdqsXr",
  "dp": "O-Zj3xbVSfQCIxeDCs8zwMbs1jX-mrw4ZwZ4qQbz3BdPqQ0QWtm4EohOSXE3SY7c5vnj8tx4IGXkWViLJ1szcIyuWh-yM8sErOl7Pgp5i3nu7OrBiqtVvArQpftD6uilgr8an7rfhpkX4hFeDnH6NPns4gxFjrHhRsCRm2o0gWXbDDGFb67qmkSrC7jIP5xOCMqTpVYbxw_ncsNqiS8KA7l9Jn9wxANszAfgRuR6-dEL_KOvF9o8jUiWA8UwRIBp",
  "dq": "r_XONiTu8nSvApLRTj0aXfewKLiVeGgeHlOqjifomBYxmak0Pt3yhbC-B71RYmjbWw_8-ymed8o3ldf5qrOIebbgXOxPfqz02tPYzt9JIop9sulGn4X1vJIQmCJic2aZx0aPpbipSx1RPFY2N9AFyx4_f4AUz5Y1yQ1cEYfsk68WSnN_zAHdmZhRJdgy1Vp0zZ_nG-FIFJuKQHkii0RwCwslw6lqH7XQxQb9RXxpiJLorrx5JPuigqZvc0Gzw_Cb",
  "e": "AQAB",
  "key_ops": [
    "sign"
  ],
  "kty": "RSA",
  "n": "wJFWzS4PNACmy1xzbwp5BWys6cW5Q6oWpKCMIvkVQ84VuPd82pwgY2IOGkd-NgJSO_vt9Ne4PMDphiNHXpJDJdkQVoLhBUBLcX4DlY-XxlPL9V9LEFNAlWq2K5aJPOXiA4rPVw_BopiGxnwf5uqyrLnvkStsW-RnNWj2XOL4YK-b12mNbe3ANre3F8yddIXcb2eFAZh-OXIvlVGc4GvYCSLpI94Gg8PXH-TJvlGjixJBCrUqxcsYAvjyWokPt1Zh_l_kH3DQmgR0qZqSRFGg_GfFFym6sn5IJ9mXyqjJV6Ra0segab9AVWUTA05SmNKn74SVTCjEFdXj_-qMsBx38p5zt3DwGck_pSfE04r6xmXCBBDTi2jPXvoS1Ar9SvaElQg0G2TZROHdA57WRH3MJiIGdzVHfSx6K5E_ykDb6UqbUfV4T4QCUR05_eX-0qJwuJLyjGfjIrL6GehuNEfkPvoYQsAUsgygrpkUKTosfwfMbljW_GsBXgCnRPsx65ih",
  "p": "3v-W6S3XpHYkSLwXEYqYSPt8f1BmnrmafB2LigdIsmQaw0hS8noUiYQc4IYH84ZnvcldMnAxSArFpVQAslIsul-6wxGwIIiz-P4y8uD9eA1p6IY7D9WovPCJhauRGqZAgAm77QAp5xzjQKS8OxmLpchNMHiizIM6WjArOBJhT285jvyXfRFPL0fMlapRNYXtk5UmkIQs3XF3HCMYNPTR6ZkN5vAb-J2IR_bfO7Emin_wYI4aHGfWOlwSGHo2eGs7",
  "q": "3RDeMSO6Ij4lYbjoxyiLOy4MOMEIYcjwvCSTNucMjGhXgonmgsGqsisToyWVEGqypIGT9ka5o2ENezDhmfCJjb2DdNOTDGTHOVj-7cTiXNukN4c-X5dbyaS8ZmynsDqP6DXH7aC4imyQx45azv_vLEBNGH3FZJgZohh5bQUrCrOdU9L1y3zwMLYkCqBe6zQTBZpZe31NmhG66YaI0DryEKbwCjQd3N8tEdtzS1pqfOXuvlQarzEi6JJBA1uD6DXT",
  "qi": "zycp3yqPVqbkT4i_xvu4qCmplngwFUcAMrB3NngQE1IQTwm1Poxi4lSG7mW1p14k1Ez_0BOkj-RyJOyvdHLaRbA7cS1iXt_CJGWZh47cnd7BEE2LpT8s6sFQbPJRjeDfF7qeyl4SWE4kpwxs8e6eBZCQ3ppG-PZFvD1S_fgs2sMIgyc4sAmgSFWc78q7M-5mnX0F7V7GMIZ4wQgpscM8hca-cnqAxmeErVt8RfNll__5JKRv7KH6-T72ewarHc6V",
  "use": "sig",
  "kid": "efc8429a5e545dad6d4d81f41c3acd3a"
}
jwk2={
  "alg": "RS256",
  "e": "AQAB",
  "key_ops": [
    "verify"
  ],
  "kty": "RSA",
  "n": "wJFWzS4PNACmy1xzbwp5BWys6cW5Q6oWpKCMIvkVQ84VuPd82pwgY2IOGkd-NgJSO_vt9Ne4PMDphiNHXpJDJdkQVoLhBUBLcX4DlY-XxlPL9V9LEFNAlWq2K5aJPOXiA4rPVw_BopiGxnwf5uqyrLnvkStsW-RnNWj2XOL4YK-b12mNbe3ANre3F8yddIXcb2eFAZh-OXIvlVGc4GvYCSLpI94Gg8PXH-TJvlGjixJBCrUqxcsYAvjyWokPt1Zh_l_kH3DQmgR0qZqSRFGg_GfFFym6sn5IJ9mXyqjJV6Ra0segab9AVWUTA05SmNKn74SVTCjEFdXj_-qMsBx38p5zt3DwGck_pSfE04r6xmXCBBDTi2jPXvoS1Ar9SvaElQg0G2TZROHdA57WRH3MJiIGdzVHfSx6K5E_ykDb6UqbUfV4T4QCUR05_eX-0qJwuJLyjGfjIrL6GehuNEfkPvoYQsAUsgygrpkUKTosfwfMbljW_GsBXgCnRPsx65ih",
  "use": "sig",
  "kid": "efc8429a5e545dad6d4d81f41c3acd3a"
}
@app.route('/')
def login():
    response = startup.getUser()
    #print("went through login")
    return redirect(response)


@app.route('/callback')
def callback():
    print("went to /callback")
    #print(request.args['code'])
    #startup.getUserToken(request.args['code'])
    creds=startup.getUserToken(request.args['code'])
    info=get_user_id(creds['access_token'])
    creds.update(info)
    header = {'alg': 'RS256'}
    payload = info
    #private_key = app.secret_key
    user_info = jwt.encode(header=header, payload=payload, key=jwk)
    #print(user_info.decode("utf-8"))
    session['user']=user_info
    session['test']=creds
    #print(startup.TOKEN_DICT["access_token"])
    #test=spotcalls.query_api([10,"US", "", "Drake", "Only", 80, 0.5, 0.5, 0.5, 0.5])
    #test = spotcalls.get_user_id()
    #return test
    songs=query_api([10,"US", "math rock", "Thank You Scientist", "Get Up", 50, 0.5, 0.5, 0.5, 0.5])
    return redirect('/nextpage')

@app.route('/nextpage')
def checkpage():
    print(session['test']['spotify_id'])
    #print("went to nextpage")
    #return spotcalls.get_user_id(session.get("user"))
    #session.get('user')s
    #info = session.get('creds')s
    #temp = jwt.decode(session['user'], jwk2)
    #temp.validate()
    songs=query_api([10,"US", "math rock", "Thank You Scientist", "Get Up", 50, 0.5, 0.5, 0.5, 0.5])
    urilist=[]
    for vals in songs['tracks']:
        urilist.append(vals['uri'])
    urijson={"uris": urilist}
    playlist_info=(make_playlist(session.get('test')['access_token'], session.get('test')['spotify_id'], {"name": "gjTest3"}))
    check=fill_playlist(session['test']['access_token'],playlist_info['id'],urijson)
    #return playlist_info['external_urls']
    return session['test']['spotify_id']

if __name__ == '__main__':
    app.run(debug=True)