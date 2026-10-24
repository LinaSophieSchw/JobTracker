"""Backend des JobTrackers.

Diese Datei erstellt die Flask-App. Sie gehört zur Schicht «Backend»:
Der Browser schickt Anfragen hierher, und Flask antwortet mit JSON.

18.10 Zusätzlich wurde in dieser Datei die SQLite-Datenbankanbindung implementiert.
Die Datenbank wird lokal im Ordner instance/ gespeichert. In der Datei datenbank.py
ist die Funktion verbindung_oeffnen() implementiert,
die die Verbindung zur SQLite-Datenbank öffnet.
Die Datenbank wir lokal gespeichert. (LS)

20.10.2026: Die oben beschriebene SQLite-Anbindung wurde durch PostgreSQL
bei Neon ersetzt. datenbank.py öffnet jetzt die PostgreSQL-Verbindung.
Die Verbindungsadresse wird über DATABASE_URL geladen:
lokal aus der .env-Datei, online aus den Vercel-Umgebungsvariablen.
Die Verbindung zu Neon muss noch getestet werden. (LS)
"""

# closing schliesst die Datenbankverbindung automatisch; gehört zu Python. (LS)
import os
from contextlib import closing
from pathlib import Path

# Liest lokale Einstellungen aus der .env-Datei.
from dotenv import load_dotenv
from flask import Flask, jsonify

# Importiert die Module aus demselben Paket wie diese Datei.
from .datenbank import verbindung_oeffnen
from .stellenanzeigen_routes import stellenanzeigen

# Das Frontend liegt im Ordner public/ im Hauptordner des Projekts.
# Online liefert Vercel diesen Ordner selbst aus. Damit es auf deinem
# Laptop gleich funktioniert, zeigen wir Flask denselben Ordner.
# parents[0] ist src/app, parents[1] ist src, parents[2] der Projektordner.
PUBLIC_ORDNER = Path(__file__).resolve().parents[2] / "public"

# Lädt die .env aus dem Projektordner.
# Zur Einrichtung der Verbindung zur Datenbank
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

app = Flask(__name__, static_folder=PUBLIC_ORDNER, static_url_path="")

# Macht die Stellenanzeigen-Routen in dieser Flask-App erreichbar.
app.register_blueprint(stellenanzeigen)

# Liest die PostgreSQL-Adresse aus den Umgebungsvariablen.
# Lokal kommt sie aus der .env, online aus den Vercel-Einstellungen.
app.config["DATABASE"] = os.getenv("DATABASE_URL")

# Liest den Schlüssel für OpenRouteService aus den Umgebungsvariablen. (FH)
# Wie bei der Datenbank: lokal aus der .env, online aus den
# Vercel-Einstellungen. So steht der Schlüssel nie im Code und nie in Git.
# Die Speicherroute holt ihn hier ab und gibt ihn an fahrzeit_berechnen().
app.config["OPENROUTESERVICE_API_KEY"] = os.getenv("OPENROUTESERVICE_API_KEY")

# ALT Ersatzt durch die andere Datenbankverbindung zu PostgreSQL am 20.10 (LS)
#  Die lokale Datenbank liegt im Hauptordner unter instance/. [LS]
# datenbank_ordner = Path(__file__).resolve().parents[2] / "instance"
# app.config["DATABASE"] = datenbank_ordner / "jobtracker.db"


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
