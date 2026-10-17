"""Backend des JobTrackers.

Diese Datei erstellt die Flask-App. Sie gehört zur Schicht «Backend»:
Der Browser schickt Anfragen hierher, und Flask antwortet mit JSON.

18.10 Zusätzlich wurde in dieser Datei die SQLite-Datenbankanbindung implementiert.
Die Datenbank wird lokal im Ordner instance/ gespeichert. In der Datei datenbank.py
ist die Funktion verbindung_oeffnen() implementiert,
die die Verbindung zur SQLite-Datenbank öffnet.
Die Datenbank wir lokal gespeichert.
"""

# closing schliesst die Datenbankverbindung automatisch; gehört zu Python. (LS)
from contextlib import closing
from pathlib import Path

from flask import Flask, jsonify

# Lädt unsere eigene Funktion aus datenbank.py; keine Installation nötig. (LS)
from app.datenbank import verbindung_oeffnen

# Das Frontend liegt im Ordner public/ im Hauptordner des Projekts.
# Online liefert Vercel diesen Ordner selbst aus. Damit es auf deinem
# Laptop gleich funktioniert, zeigen wir Flask denselben Ordner.
# parents[0] ist src/app, parents[1] ist src, parents[2] der Projektordner.
PUBLIC_ORDNER = Path(__file__).resolve().parents[2] / "public"

app = Flask(__name__, static_folder=PUBLIC_ORDNER, static_url_path="")

# Die lokale Datenbank liegt im Hauptordner unter instance/. [LS]
datenbank_ordner = Path(__file__).resolve().parents[2] / "instance"
app.config["DATABASE"] = datenbank_ordner / "jobtracker.db"


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


@app.get("/api/datenbank/status")
def datenbank_status_abfragen():
    """Prüft, ob eine Verbindung zur Datenbank möglich ist."""
    # Öffnet die Datenbank und schliesst die Verbindung nach der Prüfung.
    with closing(verbindung_oeffnen(app.config["DATABASE"])) as verbindung:
        # Eine einfache SQL-Abfrage prüft, ob die Datenbank antwortet.
        verbindung.execute("SELECT 1").fetchone()

    return jsonify({"datenbank": "ok"})
