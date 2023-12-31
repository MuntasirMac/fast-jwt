from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import Auth
from user_model import AuthModel
from dbconnection import connect_db
import os


deta = connect_db()
users_db = deta.users

app = FastAPI()

security = HTTPBearer()
auth_handler = Auth()

@app.post('/signup')
def signup(user_details: AuthModel):
    # user_details = dict(user_details)
    if users_db.find_one({'key':user_details.username}) != None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        print(hashed_password)
        user = {'key': user_details.username, 'password': hashed_password}
        result = users_db.insert_one(user).inserted_id
        return str(result)
    except:
        error_msg = 'Failed to signup user'
        return error_msg

@app.post('/login')
def login(user_details: AuthModel):
    user = users_db.find_one({'key': user_details.username})
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user['password'])):
        return HTTPException(status_code=401, detail='Invalid password')
    print("Passed password issue")
    access_token = auth_handler.encode_token(user['key'])
    refresh_token = auth_handler.encode_refresh_token(user['key'])
    return {'access_token': access_token, 'refresh_token': refresh_token}

@app.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

@app.post('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@app.get('/notsecret')
def not_secret_data():
    return 'Not secret data'