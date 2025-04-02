import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env (utile pour exécuter en local)
load_dotenv()

def get_env_variable(var_name):
    """Récupère une variable d'environnement et affiche une alerte si elle est manquante."""
    value = os.getenv(var_name)
    if not value:
        print(f"⚠️ ERREUR : La variable {var_name} est manquante ou non définie !")
    return value

# Configuration Sellsy
SELLSY_CONSUMER_TOKEN = get_env_variable('SELLSY_CONSUMER_TOKEN')
SELLSY_CONSUMER_SECRET = get_env_variable('SELLSY_CONSUMER_SECRET')
SELLSY_USER_TOKEN = get_env_variable('SELLSY_USER_TOKEN')
SELLSY_USER_SECRET = get_env_variable('SELLSY_USER_SECRET')

# Configuration Airtable
AIRTABLE_API_KEY = get_env_variable('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = get_env_variable('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = get_env_variable('AIRTABLE_TABLE_NAME')

# Debug : Vérifier que toutes les variables sont bien chargées
if __name__ == "__main__":
    print("✅ Vérification des variables d'environnement :")
    print("🔹 AIRTABLE_BASE_ID :", AIRTABLE_BASE_ID if AIRTABLE_BASE_ID else "❌ NON DÉFINI")
    print("🔹 AIRTABLE_TABLE_NAME :", AIRTABLE_TABLE_NAME if AIRTABLE_TABLE_NAME else "❌ NON DÉFINI")
