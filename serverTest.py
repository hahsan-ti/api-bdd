from flask import Flask, json, request
import jwt
from datetime import datetime, timedelta

api = Flask(__name__)

api.config["JWT_SECRET_KEY"] = "secret"

@api.route('/', methods=['GET'])
def get_root():
    
    return 'Hello World!'

@api.route('/login', methods=['POST'])
def login():
    if auth_user(request.json):
        access_token = generate_access_token(request.json['username'])
        return json.dumps({'access_token': access_token})
    else:
        return json.dumps({'message': 'Invalid credentials'}), 401

@api.route('/fedramp', methods=['POST'])
def fedramp():
    try:
        access_token = request.headers.get('Authorization')
        decode_access_token(access_token)
    except (IndexError, jwt.exceptions.DecodeError):
        return json.dumps({'message': 'Invalid or missing token'}), 401

    recv_data = request.get_json()
    data = recv_data
    if data is None:
        return return_status(message='Data not received')

    try:
        csp_id = data['cspId']
    except:
        return return_status(message='CSP ID not found')

    if csp_id != '3fa85f64-5717-4562-b3fc-2c963f66afa6':
        return return_status(message='Incorrect CSP ID')

    try:
        system_id = data['systemId']
    except:
        return return_status(message='System ID not found')

    if system_id != '3ff933ac-57d7-40ea-8829-5b52c3dbf66e':
        return return_status(message='Incorrect System ID')

    try:
        local_timestamp = data['localTimestamp']
    except:
        return return_status(message='Local timestamp not found')

    try:
        poams = data['poams']
    except:
        return return_status(message='POA&Ms data not found')

    return return_status(status="SUCCESS")

def auth_user(user_data):
    if user_data['username'] == 'admin' and user_data['password'] == 'password':
        return True
    return False

def generate_access_token(username):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, api.config["JWT_SECRET_KEY"], algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, api.config["JWT_SECRET_KEY"], algorithms=['HS256'])
        return payload
    except jwt.exceptions.DecodeError:
        raise jwt.exceptions.DecodeError('Invalid token')

def return_status(status='FAILED', message=''):
    return json.dumps({
        'status': status,
        'message': message
    })

if __name__ == '__main__':
    api.run()