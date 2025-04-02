# sellsy_client.py
import time
import random
import hashlib
import hmac
import base64
import urllib.parse
import requests
import json

class SellsyClient:
    """Client personnalisé pour l'API Sellsy v1"""
    
    def __init__(self, consumer_token, consumer_secret, user_token, user_secret):
        """Initialisation du client avec les informations d'authentification"""
        self.consumer_token = consumer_token
        self.consumer_secret = consumer_secret
        self.user_token = user_token
        self.user_secret = user_secret
        self.api_url = "https://apifeed.sellsy.com/0/"  # URL de l'API v1
    
    def _get_oauth_header(self):
        """Générer l'en-tête d'authentification OAuth pour l'API Sellsy v1"""
        oauth_data = {
            'oauth_consumer_key': self.consumer_token,
            'oauth_token': self.user_token,
            'oauth_nonce': str(random.getrandbits(64)),
            'oauth_timestamp': str(int(time.time())),
            'oauth_signature_method': 'PLAINTEXT',
            'oauth_version': '1.0',
            'oauth_signature': f"{self.consumer_secret}&{self.user_secret}"
        }
        
        # Convertir les données OAuth en chaîne de requête
        authorization_header = "OAuth " + ", ".join([f'{key}="{urllib.parse.quote(value)}"' for key, value in oauth_data.items()])
        
        return authorization_header
    
    def api(self, method, params):
        """Envoyer une requête à l'API Sellsy v1"""
        # Préparer les données de la requête
        request_data = {
            'request': 1,
            'io_mode': 'json',
            'do_in': json.dumps({
                'method': method,
                'params': params
            })
        }
        
        # Définir les en-têtes de la requête
        headers = {
            'Authorization': self._get_oauth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Envoyer la requête POST
        response = requests.post(
            self.api_url, 
            data=request_data, 
            headers=headers
        )
        
        # Vérifier le code de statut
        response.raise_for_status()
        
        # Analyser la réponse JSON
        response_data = response.json()
        
        # Vérifier les erreurs dans la réponse
        if response_data.get('status') == 'error':
            error_message = response_data.get('error', 'Unknown API error')
            raise Exception(f"Sellsy API error: {error_message}")
        
        # Retourner les données de la réponse
        return response_data.get('response', {})
