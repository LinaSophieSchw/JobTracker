"""Verarbeitet Anfragen zur Vorschau und Speicherung von Stellenanzeigen."""

from flask import Blueprint, current_app, jsonify, request

from app.datenbank import stellenanzeige_speichern, tabellen_erstellen
from app.stellenanzeige_erfassen import (
    anzeigenlink_bestimmen,
    stellentitel_auslesen,
)

# Sammelt die Stellenanzeigen-Routen.
# In __init__.py wird dieser Blueprint bei der Flask-App angemeldet.
stellenanzeigen = Blueprint("stellenanzeigen", __name__)


# Erstellt eine Vorschau: Link empfangen, Anzeige laden, Titel zurückgeben.
# Hier wird noch nichts in der Datenbank gespeichert.
@stellenanzeigen.post("/api/stellenanzeigen/vorschau")
def stellenanzeige_vorschauen():
    """Nimmt einen Link entgegen und liefert den erkannten Titel."""
    # Wandelt die JSON-Anfrage des Browsers in ein Python-Dictionary um.
    # Bei ungültigem oder fehlendem JSON erhalten wir None.
    daten = request.get_json(silent=True)

    if not isinstance(daten, dict):
        return jsonify({"fehler": "Bitte einen Link übermitteln."}), 400

    url = daten.get("url")

    # Prüft auch im Backend, da Browserprüfungen umgangen werden können.
    if not isinstance(url, str) or not url.strip():
        return jsonify({"fehler": "Bitte einen Link eingeben."}), 400

    try:
        titel = stellentitel_auslesen(url)
    except ValueError as fehler:
        # Gibt die verständliche Meldung unserer Auslesefunktion zurück.
        return jsonify({"fehler": str(fehler)}), 400

    # Vue übernimmt den Titel in ein bearbeitbares Eingabefeld.
    return jsonify({"url": url.strip(), "titel": titel})


# Speichert den Link und den vom Nutzer bestätigten Titel.
# Die Webseite wird dabei nicht erneut heruntergeladen.
@stellenanzeigen.post("/api/stellenanzeigen")
def stellenanzeige_anlegen():
    """Prüft die Eingaben und speichert eine Stellenanzeige."""
    daten = request.get_json(silent=True)

    if not isinstance(daten, dict):
        return jsonify({"fehler": "Bitte Link und Titel übermitteln."}), 400

    url = daten.get("url")
    titel = daten.get("titel")

    # Erst den Datentyp prüfen, bevor wir Textmethoden wie strip() aufrufen.
    if not isinstance(url, str) or not isinstance(titel, str):
        return jsonify({"fehler": "Link und Titel müssen Texte sein."}), 400

    # Entfernt Leerzeichen am Anfang und Ende.
    titel = titel.strip()

    if not titel:
        return jsonify({"fehler": "Bitte einen Stellentitel eingeben."}), 400

    try:
        # Prüft den Anbieter und bildet einen direkten jobs.ch-Anzeigenlink.
        url = anzeigenlink_bestimmen(url)
    except ValueError as fehler:
        return jsonify({"fehler": str(fehler)}), 400

    # current_app verweist auf die aktuell laufende Flask-App.
    # So verwenden wir ihren konfigurierten Datenbankpfad.
    datenbank_pfad = current_app.config["DATABASE"]

    # Erstellt die Tabelle nur, falls sie noch fehlt.
    # Bestehende Tabellen und Einträge werden nicht gelöscht.
    tabellen_erstellen(datenbank_pfad)

    # Die Speicherfunktion bestätigt die Änderung und liefert die neue ID.
    eintrag_id = stellenanzeige_speichern(datenbank_pfad, url, titel)

    # Status 201 bedeutet: Ein neuer Eintrag wurde erstellt.
    return jsonify({"id": eintrag_id, "url": url, "titel": titel}), 201
