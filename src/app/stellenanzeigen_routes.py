"""Empfängt Browseranfragen zur Vorschau von Stellenanzeigen."""

from flask import Blueprint, jsonify, request

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
