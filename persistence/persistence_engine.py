from django.utils.dateparse import parse_datetime

from asgiref.sync import sync_to_async
import json

from django.apps import apps


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