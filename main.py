# main.py
import time
import json
from datetime import datetime
from pyairtable.api import Api
from sellsy_client import SellsyClient  # Import notre client personnalisé
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
    # Utilisation de la nouvelle méthode recommandée pour pyairtable
    api = Api(AIRTABLE_API_KEY)
    airtable = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    return airtable

def get_sellsy_emails(sellsy, days_back=30):
    """Récupérer les emails envoyés depuis Sellsy"""
    print(f"Récupération des emails des {days_back} derniers jours...")
    
    # Utilisation de la méthode Mails.getList selon la documentation Sellsy
    current_time = int(time.time())
    start_time = current_time - (days_back * 86400)
    
    response = sellsy.api(
        method="Mails.getList",
        params={
            "search": {
                "box": "outbox",  # Pour les emails envoyés
                "period": {
                    "type": "range",
                    "start": start_time,
                    "end": current_time
                }
            },
            "pagination": {
                "nbperpage": 100,
                "pagenum": 1
            }
        }
    )
    
    # Vérifier la structure de la réponse selon la documentation
    if isinstance(response, dict) and "result" in response:
        return response["result"]
    elif isinstance(response, list):
        return response
    else:
        print(f"Format de réponse inattendu: {response}")
        return []

def format_email_for_airtable(email):
    """Formater les données d'email pour Airtable"""
    # Adapter le format selon les données réelles retournées par l'API
    email_data = {
        "email_id": str(email.get("id", "")),
        "sujet": email.get("subject", ""),
        "date_envoi": datetime.fromtimestamp(int(email.get("created_date", 0))).isoformat(),
        "statut": email.get("status", ""),
    }
    
    # Traiter les destinataires (qui peuvent être un tableau ou une chaîne JSON)
    recipients = email.get("recipients", "")
    if isinstance(recipients, str):
        try:
            # Si c'est une chaîne JSON, essayez de la parser
            recipients_data = json.loads(recipients.replace("'", "\""))
            recipients_list = []
            if isinstance(recipients_data, list):
                for recipient in recipients_data:
                    if isinstance(recipient, dict) and "email" in recipient:
                        recipients_list.append(recipient["email"])
            email_data["destinataire"] = ", ".join(recipients_list)
        except:
            email_data["destinataire"] = recipients
    elif isinstance(recipients, list):
        recipients_list = [r.get("email", "") for r in recipients if isinstance(r, dict)]
        email_data["destinataire"] = ", ".join(recipients_list)
    
    # Traiter le contenu du message
    message = email.get("message", "")
    if message:
        email_data["contenu"] = message
    
    # Ajouter l'ID client si disponible
    if "linkedid" in email and email.get("linkedtype") == "third":
        email_data["client_id"] = str(email.get("linkedid", ""))
    
    return email_data

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
