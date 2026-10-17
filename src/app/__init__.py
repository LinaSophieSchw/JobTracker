"""Backend des JobTrackers.

Diese Datei erstellt die Flask-App. Sie gehört zur Schicht «Backend»:
Der Browser schickt Anfragen hierher, und Flask antwortet mit JSON.
"""

from pathlib import Path

from flask import Flask, jsonify

# Das Frontend liegt im Ordner public/ im Hauptordner des Projekts.
# Online liefert Vercel diesen Ordner selbst aus. Damit es auf deinem
# Laptop gleich funktioniert, zeigen wir Flask denselben Ordner.
# parents[0] ist src/app, parents[1] ist src, parents[2] der Projektordner.
PUBLIC_ORDNER = Path(__file__).resolve().parents[2] / "public"

app = Flask(__name__, static_folder=PUBLIC_ORDNER, static_url_path="")


@app.get("/")
def startseite_anzeigen():
    """Liefert die Startseite des Frontends aus."""
    return app.send_static_file("index.html")


@app.get("/api/status")
def status_abfragen():
    """Meldet, ob das Backend läuft."""
    # Diese Route hat noch keine Fachlogik. Sie ist ein Lebenszeichen:
    # Antwortet sie, wissen wir, dass Flask läuft und erreichbar ist.
    # Später prüfen wir hier zusätzlich die Verbindung zur Datenbank.
    return jsonify({"status": "ok"})
