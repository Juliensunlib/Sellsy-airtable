# sellsy_client.py
import requests
import hashlib
import time
import random
import string
import json
import urllib.parse

class SellsyClient:
    def __init__(self, consumer_token, consumer_secret, user_token, user_secret, api_url="https://api.sellsy.com/v2/"):
        self.consumer_token = consumer_token
        self.consumer_secret = consumer_secret
        self.user_token = user_token
        self.user_secret = user_secret
        self.api_url = api_url
    
    def get_nonce(self, length=10):
        """Generate a random nonce string."""
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    
    def api(self, method, params=None):
        """Make an API request to Sellsy."""
        if params is None:
            params = {}
            
        # Current unix timestamp
        timestamp = str(int(time.time()))
        nonce = self.get_nonce()
        
        # Prepare the OAuth parameters
        oauth_params = {
            'oauth_consumer_key': self.consumer_token,
            'oauth_token': self.user_token,
            'oauth_nonce': nonce,
            'oauth_timestamp': timestamp,
            'oauth_signature_method': 'PLAINTEXT',
            'oauth_version': '1.0',
            'oauth_signature': f"{self.consumer_secret}&{self.user_secret}"
        }
        
        # Prepare the request data
        request_data = {
            'request': 1,
            'io_mode': 'json',
            'do_in': json.dumps({
                'method': method,
                'params': params
            })
        }
        
        # Make the HTTP request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Combine OAuth and request data
        data = {**oauth_params, **request_data}
        encoded_data = urllib.parse.urlencode(data)
        
        response = requests.post(self.api_url, data=encoded_data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        result = json.loads(response.text)
        
        # Check for API errors
        if result.get('status') == 'error':
            raise Exception(f"API error: {result.get('error')}")
        
        return result.get('response')
