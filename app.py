from flask import Flask, json, request, jsonify, make_response
from flask.wrappers import Response
import jwt
import datetime
from functools import wraps
import os
from dotenv import load_dotenv
import unittest

load_dotenv() 


app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')

@app.errorhandler(405)
def error(e):
    return 'ERROR', 405

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


password = 'esto es una prueba'

@app.route('/get_token', methods=['POST'])
def get_token():
    """
    Generates the Auth Token
    :return: string
    """
    request_data = request.get_json()
    if request_data != None and 'apikey' in request_data:
        api_key_base = os.getenv('API_KEY') 
        api_key_request = request_data['apikey']
        if api_key_base == api_key_request:
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=20),
                    'iat': datetime.datetime.utcnow(),
                    'sub': api_key_base
                }
                encoded_jwt = jwt.encode(
                    payload,
                    app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                )
                return jsonify({'token': encoded_jwt })

            except Exception as e:
                return e,401
        else:
            return jsonify({'message': 'invalid apikey'}),401
    else:
        return jsonify({'message': 'you must provide an apikey'}),401


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'X-JWT-KWY' in request.headers:
           token = request.headers['X-JWT-KWY']
 
       if not token:
           return jsonify(message='a valid token is missing'),401
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
       except:
           return jsonify(message='token is invalid'),401
 
       return f(*args, **kwargs)
   return decorator

    
@app.route('/DevOps', methods=['POST'])
@token_required
def devops():
   request_data = request.get_json()
   if request_data != None and 'to' in request_data:
      sender = request_data['to'] 
      return jsonify({'message':f'Hello {sender} your message will be send'})
   else: 
       return jsonify(message='Invalid request')


#route added for liveness probe kubernetes
@app.route('/is_alive', methods=['GET'])
def is_alive():
    return "i am alive!!"
