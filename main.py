# main.py
import time
import json
from datetime import datetime
from sellsy.client import Client as SellsyClient
from pyairtable import Table
from config import *

def connect_to_sellsy():
    """Établir la connexion avec l'API Sellsy"""
    print("Connexion à l'API Sellsy...")
    sellsy = SellsyClient(
        consumer_token=SELLSY_CONSUMER_TOKEN,
        consumer_secret=SELLSY_CONSUMER_SECRET,
        user_token=SELLSY_USER_TOKEN,
        user_secret=SELLSY_USER_SECRET
    )
    return sellsy

def connect_to_airtable():
    """Établir la connexion avec l'API Airtable"""
    print("Connexion à l'API Airtable...")
    airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    return airtable

def get_sellsy_emails(sellsy, days_back=30):
    """Récupérer les emails envoyés depuis Sellsy"""
    print(f"Récupération des emails des {days_back} derniers jours...")
    
    # Exemple d'appel API Sellsy pour récupérer les emails
    # Adaptez cette partie selon la structure de l'API Sellsy
    response = sellsy.api(
        method="Document.getList",
        params={
            "doctype": "email",
            "pagination": {"nbperpage": 100},
            "search": {
                "period": {
                    "type": "range", 
                    "start": int(time.time()) - (days_back * 86400),
                    "end": int(time.time())
                }
            }
        }
    )
    
    return response.get("result", [])

def format_email_for_airtable(email):
    """Formater les données d'email pour Airtable"""
    return {
        "email_id": str(email.get("id")),
        "sujet": email.get("subject", ""),
        "destinataire": email.get("recipient", ""),
        "date_envoi": datetime.fromtimestamp(int(email.get("date", 0))).isoformat(),
        "contenu": email.get("content", ""),
        "statut": email.get("status", ""),
        "client_id": str(email.get("clientid", ""))
    }

def sync_emails_to_airtable():
    """Synchroniser les emails de Sellsy vers Airtable"""
    try:
        # Connexion aux APIs
        sellsy = connect_to_sellsy()
        airtable = connect_to_airtable()
        
        # Récupération des emails depuis Sellsy
        emails = get_sellsy_emails(sellsy)
        print(f"Nombre d'emails récupérés: {len(emails)}")
        
        # Récupération des IDs d'emails déjà enregistrés dans Airtable
        existing_records = airtable.all(fields=["email_id"])
        existing_ids = {record["fields"].get("email_id") for record in existing_records if "email_id" in record["fields"]}
        
        # Synchronisation des emails
        new_count = 0
        for email in emails:
            email_id = str(email.get("id"))
            
            # Vérifier si l'email existe déjà dans Airtable
            if email_id not in existing_ids:
                # Formater les données pour Airtable
                email_data = format_email_for_airtable(email)
                
                # Ajouter l'enregistrement dans Airtable
                airtable.create(email_data)
                new_count += 1
                print(f"Email {email_id} ajouté à Airtable")
        
        print(f"Synchronisation terminée. {new_count} nouveaux emails ajoutés à Airtable.")
        
    except Exception as e:
        print(f"Erreur lors de la synchronisation: {str(e)}")

if __name__ == "__main__":
    sync_emails_to_airtable()
