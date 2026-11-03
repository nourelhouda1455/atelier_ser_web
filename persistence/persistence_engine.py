from django.utils.dateparse import parse_datetime

from asgiref.sync import sync_to_async
import json

from django.apps import apps
import pyrebase
import firebase_admin
from firebase_admin import credentials 

firebase_config = {
"apiKey": "AIzaSyBoM78IR4AKFKAskCCpH2E2Tb-0iCagRoA",
  "authDomain": "gestion-grandeur2026.firebaseapp.com",
  "databaseURL": "https://gestion-grandeur2026-default-rtdb.firebaseio.com",
  "projectId": "gestion-grandeur2026",
  "storageBucket": "gestion-grandeur2026.firebasestorage.app",
  "messagingSenderId": "526793620908",
  "appId": "1:526793620908:web:dbafab38977f1d5a8a8e09"
}
firebase = pyrebase.initialize_app(firebase_config)
database = firebase.database() #get database instance

cred = credentials.Certificate("certificat_firebase.json")
firebase_admin.initialize_app(cred)

@sync_to_async
def persist_to_firebase(message):
    message = json.loads(message)
    print(f"Persisting to firebase: {message}")
    try:
        database.child("mesures").push(message)
    except Exception as e:
        print(f"Error occurred while persisting to firebase: {e}")   

@sync_to_async
def persist_mesure(message):
    #from grandeurs.models import Grandeur, Mesure
    Grandeur = apps.get_model("grandeurs", "Grandeur")
    Mesure = apps.get_model("grandeurs", "Mesure")

    message = json.loads(message)

    grandeur = Grandeur.objects.get(nom="Temperature")
    print(f"Persisting mesure: {message}")
    Mesure.objects.create(
        valeur = float(message["valeur"]),
        date_prise = parse_datetime(message["date_prise"]),
        grandeur = grandeur
    )

buffer = []

@sync_to_async
def persist_mesure_bulk(message):
    from grandeurs.models import Grandeur, Mesure

    message = json.loads(message)

    global buffer

    buffer.append(
        Mesure(
            valeur = float(message["valeur"]),
            date_prise = parse_datetime(message["date_prise"])
        )
    )

    if len(buffer) >= 100:
        Mesure.objects.bulk_create(buffer)
        print(f"Inserted {len(buffer)} rows")
        buffer.clear()