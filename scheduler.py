# scheduler.py
import schedule
import time
from main import sync_emails_to_airtable

def job():
    print(f"Exécution de la synchronisation... {time.strftime('%Y-%m-%d %H:%M:%S')}")
    sync_emails_to_airtable()
    print(f"Synchronisation terminée à {time.strftime('%Y-%m-%d %H:%M:%S')}. En attente de la prochaine exécution.")

# Planifier l'exécution quotidienne à 3h du matin
schedule.every().day.at("03:00").do(job)

print("Planificateur démarré. La synchronisation s'exécutera tous les jours à 03:00.")
print("Appuyez sur Ctrl+C pour arrêter.")

# Première exécution immédiate
job()

# Boucle pour maintenir le planificateur actif
while True:
    schedule.run_pending()
    time.sleep(60)