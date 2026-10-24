"""Empfängt Browseranfragen zur Vorschau und Speicherung von Stellenanzeigen.

Version 01 – 18.10.2026:
Route für die Titelvorschau ergänzt; noch keine Speicherung. (LS)

Version 02 – 20.10.2026:
Vorschau um Firma, Arbeitsort, Adresse, Pensum und Beschreibung erweitert. (LS)

Version 03 – 20.10.2026:
Route zum Speichern bestätigter Formularangaben in PostgreSQL ergänzt. (LS)

Version 04 – 24.10.2026:
Beim Speichern wird die Fahrzeit berechnet und eingetragen (US 30001). (FH)
"""

import psycopg
from flask import Blueprint, current_app, jsonify, request

from .arbeitsweg import fahrzeit_berechnen
from .datenbank import fahrzeit_speichern, stellenanzeige_speichern, wohnadresse_lesen
from .stellenanzeige_erfassen import stellenanzeige_auslesen

# Sammelt unsere Stellenanzeigen-Routen.
# In __init__.py wird diese Sammlung bei der Flask-App registriert.
stellenanzeigen = Blueprint("stellenanzeigen", __name__)


# POST bedeutet: Der Browser übermittelt Daten, hier den Stellenlink.
@stellenanzeigen.post("/api/stellenanzeigen/vorschau")
def stellenanzeige_vorschauen():
    """Nimmt einen Link entgegen und liefert die erkannten Anzeigenangaben."""
    # Wandelt die JSON-Anfrage in ein Python-Dictionary um.
    # Bei ungültigem JSON liefert silent=True den Wert None.
    daten = request.get_json(silent=True)

    if not isinstance(daten, dict):
        return jsonify({"fehler": "Bitte einen Link übermitteln."}), 400

    url = daten.get("url")

    # Nur ein nicht leerer Text darf an die Auslesefunktion weitergehen.
    if not isinstance(url, str) or not url.strip():
        return jsonify({"fehler": "Bitte einen Link eingeben."}), 400

    try:
        # Lädt die Anzeige und liest alle vorgesehenen Vorschaufelder.
        # Es wird noch nichts in der Datenbank gespeichert.
        vorschau = stellenanzeige_auslesen(url)
    except ValueError as fehler:
        # HTTP 400 meldet dem Frontend eine fehlgeschlagene Vorschau.
        return jsonify({"fehler": str(fehler)}), 400

    # Wandelt das Dictionary mit allen Feldern in JSON für den Browser um.
    return jsonify(vorschau)


# ==================================================
# Fahrzeit für eine neu gespeicherte Stelle berechnen und eintragen (FH)
# ==================================================
# Wozu: Die Route unten soll kurz bleiben. Diese Hilfsfunktion erledigt
# den ganzen Arbeitsweg-Teil, nachdem die Stelle gespeichert ist:
#
#   wohnadresse_lesen() → fahrzeit_berechnen() → fahrzeit_speichern()
#
def arbeitsweg_eintragen(stellen_id, daten):
    """Berechnet die Fahrzeit einer neuen Stelle und trägt sie bei ihr ein.

    daten sind die Formularangaben. Gibt die Minuten zurück, z. B. 95,
    oder None, wenn der Arbeitsweg nicht berechnet werden konnte.
    """
    datenbank_url = current_app.config["DATABASE"]

    # 1. Arbeitsadresse aus dem Formular zusammenstellen, in derselben Form
    #    wie die Wohnadresse aus wohnadresse_lesen(). So kann
    #    fahrzeit_berechnen() beide Adressen gleich behandeln.
    arbeitsadresse = {
        "strasse": daten.get("inseratadresse_strasse"),
        "postleitzahl": daten.get("inseratadresse_postleitzahl"),
        "ort": daten.get("inseratadresse_ort"),
    }

    # 2. Wohnadresse des Demo-Benutzers aus der Datenbank holen.
    wohnadresse = wohnadresse_lesen(datenbank_url)

    # 3. Fahrzeit berechnen lassen. Scheitert das, kommt None zurück.
    fahrzeit_in_minuten = fahrzeit_berechnen(
        wohnadresse,
        arbeitsadresse,
        current_app.config["OPENROUTESERVICE_API_KEY"],
    )

    # 4. Ergebnis bei der Stelle eintragen. Bei None bleibt das Feld leer.
    fahrzeit_speichern(datenbank_url, stellen_id, fahrzeit_in_minuten)

    return fahrzeit_in_minuten


# ==================================================
# Geprüfte Stellenanzeige speichern
# ==================================================
@stellenanzeigen.post("/api/stellenanzeigen")
def stellenanzeige_anlegen():
    """Speichert die bestätigten Formularangaben in PostgreSQL."""
    daten = request.get_json(silent=True)

    try:
        # current_app greift auf die Konfiguration der laufenden Flask-App zu.
        neue_id = stellenanzeige_speichern(
            current_app.config["DATABASE"],
            daten,
        )
    except ValueError as fehler:
        # Ungültige Eingaben oder doppelte Links verständlich zurückmelden.
        return jsonify({"fehler": str(fehler)}), 400
    except psycopg.Error:
        # Technische Datenbankdetails werden nicht an den Browser geschickt.
        return (
            jsonify(
                {
                    "fehler": "Speichern derzeit nicht möglich. "
                    "Bitte später erneut versuchen."
                }
            ),
            503,
        )

    # Erst jetzt, mit gespeicherter Stelle, den Arbeitsweg berechnen. (FH)
    # Ein doppelter Link oder ein Eingabefehler bricht schon oben ab;
    # dann wird der Kartendienst gar nicht erst gefragt.
    fahrzeit_in_minuten = arbeitsweg_eintragen(neue_id, daten)

    # HTTP 201 bedeutet: Ein neuer Datensatz wurde erstellt.
    # Das gilt auch, wenn die Fahrzeit fehlt (None wird in JSON zu null):
    # Die Stelle ist gespeichert, nur der Arbeitsweg nicht. Welcher Text
    # dann erscheint, entscheidet das Frontend.
    return (
        jsonify({"id": neue_id, "fahrzeit_auto_in_minuten": fahrzeit_in_minuten}),
        201,
    )
