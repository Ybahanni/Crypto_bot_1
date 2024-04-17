import requests
import json
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

API_KEY = "B2D1D322-1C25-4DDF-A8EE-D7B289AA1ADA"
BASE_URL = "https://rest.coinapi.io/v1/"

def create_alert(currency, threshold):
    alert = {"currency": currency, "threshold": threshold}
    try:
        with open("alerts.json", "r+") as file:
            data = json.load(file)
            data.append(alert)
            file.seek(0)
            json.dump(data, file)
    except FileNotFoundError:
        with open("alerts.json", "w") as file:
            json.dump([alert], file)

def list_alerts(currency):
    try:
        with open("alerts.json", "r") as file:
            data = json.load(file)
            alerts = [alert for alert in data if alert["currency"] == currency]
            if alerts:
                print(f"Liste des alertes pour {currency}:")
                for index, alert in enumerate(alerts, 1):
                    print(f"{index}. Seuil: {alert['threshold']}")
            else:
                print(f"Aucune alerte trouvée pour {currency}.")
    except FileNotFoundError:
        print("Le fichier alerts.json n'existe pas.")



def delete_alert(currency, threshold):
    try:
        with open("alerts.json", "r+") as file:
            data = json.load(file)
            data = [alert for alert in data if not (alert["currency"] == currency and alert["threshold"] == threshold)]
            file.seek(0)
            json.dump(data, file)
    except FileNotFoundError:
        print("Le fichier alerts.json n'existe pas.")



def get_current_price(currency):
    url = BASE_URL + f"exchangerate/{currency}/USD"
    headers = {"X-CoinAPI-Key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["rate"]
    else:
        print("Erreur:", response.status_code)



def check_alerts():
    while True:
        try:
            with open("alerts.json", "r") as file:
                data = json.load(file)
                for alert in data:
                    currency = alert["currency"]
                    threshold = alert["threshold"]
                    price = get_current_price(currency)
                    if price and price < threshold:
                        print(f"Alerte ! {currency} est tombée en dessous de {threshold}$ ! Prix actuel : {price}$")
            time.sleep(2)
        except FileNotFoundError:
            print("Le fichier alerts.json n'existe pas.")
            break
        
def get_historical_data(currency, timeframe):
    url = f"https://rest.coinapi.io/v1/ohlcv/{currency}/USD/history?period_id={timeframe}"
    headers = {"X-CoinAPI-Key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        prices = [entry['price_close'] for entry in data]
        return prices
    else:
        print("Erreur lors de la récupération des données historiques:", response.status_code)
        return None
    
    
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_USERNAME = 'bahannisyoussef@gmail.com'  
EMAIL_PASSWORD = 'xxxxx'  

def send_email_alert(currency, threshold, current_price):
    sender_email = EMAIL_USERNAME
    receiver_email = 'sollasilalala@gmail.com'  # The recipient's email address
    subject = f'Alert: {currency} Price Fell Below {threshold}'
    message = f"The price of {currency} has fallen below {threshold}. Current Price: {current_price}"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(sender_email, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email notification sent successfully.")
    except Exception as e:
        print("An error occurred while sending email notification:", str(e))
   
        

    

def main():
    print("Bienvenue dans l'application de notification de cryptomonnaie !")
    while True:
        print("\nChoisissez une option :")
        print("1. Créer une alerte")
        print("2. Lister toutes les alertes pour une devise")
        print("3. Supprimer une alerte")
        print("4. Démarrer l'écoute des changements de cryptomonnaie")
        print("5. Quitter")
        choice = input("Entrez votre choix : ")

        if choice == "1":
            currency = input("Entrez la devise (par exemple, BTC) : ")
            threshold = float(input("Entrez le seuil de prix : "))
            create_alert(currency, threshold)
            print("Alerte créée avec succès !")

        elif choice == "2":
            currency = input("Entrez la devise (par exemple, BTC) : ")
            list_alerts(currency)

        elif choice == "3":
            currency = input("Entrez la devise (par exemple, BTC) : ")
            threshold = float(input("Entrez le seuil de prix : "))
            delete_alert(currency, threshold)
            print("Alerte supprimée avec succès !")

        elif choice == "4":
            
            print("Démarrage de l'écoute des changements de cryptomonnaie...")
            check_alerts()
            send_email_alert(currency, threshold, get_current_price(currency))

        elif choice == "5":
            print("Fermeture de l'application...")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
    
    


