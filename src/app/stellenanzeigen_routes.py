"""Empfängt Browseranfragen zur Vorschau und Speicherung von Stellenanzeigen.

Version 01 – 18.10.2026:
Route für die Titelvorschau ergänzt; noch keine Speicherung. (LS)

Version 02 – 20.10.2026:
Vorschau um Firma, Arbeitsort, Adresse, Pensum und Beschreibung erweitert. (LS)

Version 03 – 20.10.2026:
Route zum Speichern bestätigter Formularangaben in PostgreSQL ergänzt. (LS)
"""

import psycopg
from flask import Blueprint, current_app, jsonify, request

from .datenbank import stellenanzeige_speichern
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

    # HTTP 201 bedeutet: Ein neuer Datensatz wurde erstellt.
    return jsonify({"id": neue_id}), 201
