"""Öffnet eine Verbindung zur PostgreSQL-Datenbank.
20.10.2026: Die bisherige SQLite-Anbindung wurde ersetzt."""

import psycopg


# Die Verbindungsadresse enthält Server, Datenbankname und Zugangsdaten.
# Sie wird aus der Konfiguration übergeben und nicht im Code gespeichert.
def verbindung_oeffnen(datenbank_url):
    """Öffnet eine Verbindung zu PostgreSQL."""
    if not datenbank_url:
        raise ValueError("Die Umgebungsvariable DATABASE_URL fehlt.")

    # Bricht den Verbindungsversuch nach spätestens 15 Sekunden ab.
    return psycopg.connect(datenbank_url, connect_timeout=15)

    # ALT Ersetzt durch die andere Datenbankverbindung zu PostgreSQL am 20.10 (LS)
    # """Öffnet die Verbindung zur lokalen SQLite-Datenbank."""

    # import sqlite3
    # from pathlib import Path

    # def verbindung_oeffnen(datenbank_pfad):
    # """Erstellt bei Bedarf die Datenbank und öffnet eine Verbindung."""
    # datenbank_pfad = Path(datenbank_pfad)

    # SQLite erstellt die Datei, aber nicht den übergeordneten Ordner.
    # datenbank_pfad.parent.mkdir(parents=True, exist_ok=True)

    # return sqlite3.connect(datenbank_pfad)
