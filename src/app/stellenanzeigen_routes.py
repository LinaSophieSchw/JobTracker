"""Verarbeitet Browseranfragen zur Vorschau von Stellenanzeigen."""

from flask import Blueprint, jsonify, request

from app.stellenanzeige_erfassen import stellentitel_auslesen

# Sammelt die zusammengehörigen Stellenanzeigen-Routen.
stellenanzeigen = Blueprint("stellenanzeigen", __name__)


# Liest einen Titel zur Vorschau aus; speichert noch keine Bewerbung.
@stellenanzeigen.post("/api/stellenanzeigen/vorschau")
def stellenanzeige_vorschauen():
    """Nimmt einen Link entgegen und liefert den erkannten Titel."""
    daten = request.get_json(silent=True)

    if not isinstance(daten, dict):
        return jsonify({"fehler": "Bitte einen Link übermitteln."}), 400

    url = daten.get("url")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"fehler": "Bitte einen Link eingeben."}), 400

    try:
        titel = stellentitel_auslesen(url)
    except ValueError as fehler:
        return jsonify({"fehler": str(fehler)}), 400

    return jsonify({"url": url.strip(), "titel": titel})
