from flask_testing import TestCase
from app import app
from flask import current_app, jsonify
import os
import json
from dotenv import load_dotenv


load_dotenv() 

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True        
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_devops_endpoint_is_protected(self): 
        with app.test_client() as client:
            sent = {
                "message": "This is a test",
                "to": "Kevo Rojas",
                "from": "Rita Asturia",
                "timeToLifeSec": 45
            }
            result = client.post('/DevOps',data=sent, content_type='application/json')
            expected = "a valid token is missing"
            data = json.loads(result.get_data(as_text=True))
            assert data['message'] == expected