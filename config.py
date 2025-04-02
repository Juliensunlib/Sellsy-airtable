# config.py
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env si présent
load_dotenv()

# Configuration Sellsy
SELLSY_CONSUMER_TOKEN = os.environ.get('SELLSY_CONSUMER_TOKEN')
SELLSY_CONSUMER_SECRET = os.environ.get('SELLSY_CONSUMER_SECRET')
SELLSY_USER_TOKEN = os.environ.get('SELLSY_USER_TOKEN')
SELLSY_USER_SECRET = os.environ.get('SELLSY_USER_SECRET')

# Configuration Airtable
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME')  # Assurez-vous d'ajouter cette variable à GitHub Actions
