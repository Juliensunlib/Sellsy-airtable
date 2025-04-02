# config.py
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Sellsy
SELLSY_CONSUMER_TOKEN = os.getenv("SELLSY_CONSUMER_TOKEN")
SELLSY_CONSUMER_SECRET = os.getenv("SELLSY_CONSUMER_SECRET")
SELLSY_USER_TOKEN = os.getenv("SELLSY_USER_TOKEN")
SELLSY_USER_SECRET = os.getenv("SELLSY_USER_SECRET")

# Configuration Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "Emails Sellsy"