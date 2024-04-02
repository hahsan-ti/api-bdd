from datetime import datetime, timezone
from flask import Flask, request
from jwt import JWT, jwk_from_pem

TOKEN = ''

app = Flask(__name__)

@app.route('/')
def route_root():
    return 'Welcome to the server!'

@app.route('/alive')
def route_alive():
    return {
        'status': 'alive',
        'time': datetime.now(timezone.utc).isoformat()
    }

@app.route('/token')
def route_token():
    user_id = None
    jwtoken = None

    if 'user_id' in request.args:
        user_id = request.args['user_id']
        jwtoken = encode_token(user_id)

    global TOKEN
    TOKEN = jwtoken
    return {
        'token': jwtoken
    }

@app.route('/secret')
def route_secret():
    token = request.args['token']
    if token == TOKEN:
        return 'banana'
    return 'deadbeef'

def encode_token(user_id):
    if user_id is None:
        return None

    with open('./key.pem', 'rb') as f:
        secret_key = jwk_from_pem(f.read())

    token = ''
    if user_id in ['hahsan', 'psrity', 'admin']:
        payload = {
            'user_id': user_id,
            'message': 'Hey Pranav, this is a secret message!',
            'exp': datetime.now(timezone.utc).timestamp() + 60 * 60
        }
        token = JWT().encode(payload, secret_key, alg='RS256')

    return token