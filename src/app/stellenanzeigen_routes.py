"""Empfängt Browseranfragen zur Vorschau und Speicherung von Stellenanzeigen.

Version 01 – 18.10.2026:
Route für die Titelvorschau ergänzt; noch keine Speicherung. (LS)

Version 02 – 20.10.2026:
Vorschau um Firma, Arbeitsort, Adresse, Pensum und Beschreibung erweitert. (LS)

Version 03 – 20.10.2026:
Route zum Speichern bestätigter Formularangaben in PostgreSQL ergänzt. (LS)

Version 04 – 24.10.2026:
Beim Speichern wird die Fahrzeit berechnet und eingetragen (US 30001). (FH)

Version 05 – 24.10.2026:
Zusätzlich wird die Streckenlänge eingetragen und mitgeschickt (US 30002). (FH)

Version 06 – 24.10.2026:
Route für die Übersicht aller Stellen ergänzt (US 20001). (MG)

Version 07 – 25.10.2026:
Route zum Öffnen einer einzelnen Stelle ergänzt (US 20002). (MG)
"""

import psycopg
from flask import Blueprint, current_app, jsonify, request

from .arbeitsweg import arbeitsweg_berechnen
from .datenbank import (
    arbeitsweg_speichern,
    stellenanzeige_mit_id_lesen,
    stellenanzeige_speichern,
    stellenanzeigen_lesen,
    wohnadresse_lesen,
)
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
# Arbeitsweg für eine neu gespeicherte Stelle berechnen und eintragen (FH)
# ==================================================
# Wozu: Die Route unten soll kurz bleiben. Diese Hilfsfunktion erledigt
# den ganzen Arbeitsweg-Teil, nachdem die Stelle gespeichert ist:
#
#   wohnadresse_lesen() → arbeitsweg_berechnen() → arbeitsweg_speichern()
#
def arbeitsweg_eintragen(stellen_id, daten):
    """Berechnet Fahrzeit und Strecke einer neuen Stelle und trägt sie ein.

    daten sind die Formularangaben. Gibt ein Dictionary zurück, z. B.
    {"fahrzeit_auto_in_minuten": 95, "strecke_auto_in_metern": 138268}.
    Konnte der Arbeitsweg nicht berechnet werden, sind beide Werte None.
    """
    datenbank_url = current_app.config["DATABASE"]

    # 1. Arbeitsadresse aus dem Formular zusammenstellen, in derselben Form
    #    wie die Wohnadresse aus wohnadresse_lesen(). So kann
    #    arbeitsweg_berechnen() beide Adressen gleich behandeln.
    arbeitsadresse = {
        "strasse": daten.get("inseratadresse_strasse"),
        "postleitzahl": daten.get("inseratadresse_postleitzahl"),
        "ort": daten.get("inseratadresse_ort"),
    }

    # 2. Wohnadresse des Demo-Benutzers aus der Datenbank holen.
    wohnadresse = wohnadresse_lesen(datenbank_url)

    # 3. Fahrzeit und Strecke berechnen lassen. Scheitert das, sind beide
    #    Werte None.
    arbeitsweg = arbeitsweg_berechnen(
        wohnadresse,
        arbeitsadresse,
        current_app.config["OPENROUTESERVICE_API_KEY"],
    )

    # 4. Ergebnis bei der Stelle eintragen. Bei None bleiben die Felder leer.
    arbeitsweg_speichern(datenbank_url, stellen_id, arbeitsweg)

    return arbeitsweg


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
    arbeitsweg = arbeitsweg_eintragen(neue_id, daten)

    # HTTP 201 bedeutet: Ein neuer Datensatz wurde erstellt.
    # Das gilt auch, wenn der Arbeitsweg fehlt (None wird in JSON zu null):
    # Die Stelle ist gespeichert, nur der Arbeitsweg nicht. Welcher Text
    # dann erscheint, entscheidet das Frontend.
    # Die Strecke geht in Metern an den Browser, so wie sie gespeichert ist.
    return (
        jsonify(
            {
                "id": neue_id,
                "fahrzeit_auto_in_minuten": arbeitsweg["fahrzeit_auto_in_minuten"],
                "strecke_auto_in_metern": arbeitsweg["strecke_auto_in_metern"],
            }
        ),
        201,
    )


# ==================================================
# Alle Stellen für die Übersicht liefern (MG)
# ==================================================
# GET bedeutet: Der Browser will nur Daten abholen und schickt keine mit.
# Es ist dieselbe Adresse wie beim Speichern oben; Flask unterscheidet die
# beiden Routen an der Methode: GET liest, POST legt neu an.
@stellenanzeigen.get("/api/stellenanzeigen")
def stellenanzeigen_auflisten():
    """Liefert alle Stellen des Demo-Benutzers als JSON-Liste."""
    try:
        stellen = stellenanzeigen_lesen(current_app.config["DATABASE"])
    except psycopg.Error:
        # Wie beim Speichern: keine technischen Details an den Browser.
        # 503 heisst «Dienst gerade nicht verfügbar».
        return (
            jsonify({"fehler": "Übersicht derzeit nicht verfügbar."}),
            503,
        )

    # jsonify macht aus der Python-Liste JSON. Ohne Angabe ist der
    # Statuscode 200, also «OK».
    return jsonify(stellen)


# ==================================================
# Eine einzelne Stelle zum Öffnen liefern (MG)
# ==================================================
# <int:stellen_id> ist ein Platzhalter in der Adresse. Bei
# /api/stellenanzeigen/7 übergibt Flask die 7 als Zahl an stellen_id.
# int: sorgt dafür, dass nur Zahlen passen; /api/stellenanzeigen/abc
# beantwortet Flask selbst mit 404.
@stellenanzeigen.get("/api/stellenanzeigen/<int:stellen_id>")
def stellenanzeige_oeffnen(stellen_id):
    """Liefert eine Stelle des Demo-Benutzers als JSON-Objekt."""
    try:
        stelle = stellenanzeige_mit_id_lesen(
            current_app.config["DATABASE"],
            stellen_id,
        )
    except psycopg.Error:
        # Wie bei der Übersicht: keine technischen Details an den Browser.
        return jsonify({"fehler": "Stelle derzeit nicht verfügbar."}), 503

    # None heisst: keine Stelle mit dieser id, oder sie gehört einem anderen
    # Benutzer. Für den Browser ist beides gleich: 404, «nicht gefunden».
    # So verrät die Antwort nicht, ob es die id bei jemand anderem gibt.
    if stelle is None:
        return jsonify({"fehler": "Diese Stelle wurde nicht gefunden."}), 404

    return jsonify(stelle)
