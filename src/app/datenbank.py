"""Öffnet die Verbindung zur lokalen SQLite-Datenbank."""

import sqlite3

# Schliesst die Datenbankverbindung nach dem with-Block.
from contextlib import closing
from pathlib import Path


def verbindung_oeffnen(datenbank_pfad):
    """Erstellt bei Bedarf die Datenbank und öffnet eine Verbindung."""
    datenbank_pfad = Path(datenbank_pfad)

    # SQLite erstellt die Datei, aber nicht den übergeordneten Ordner.
    datenbank_pfad.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(datenbank_pfad)


# Legt die Tabelle für Stellenanzeigen an, sofern sie noch nicht existiert.
# Vorhandene Einträge bleiben dabei erhalten.
def tabellen_erstellen(datenbank_pfad):
    """Erstellt die Tabelle für Link und Stellentitel."""
    with closing(verbindung_oeffnen(datenbank_pfad)) as verbindung:
        verbindung.execute("""
            CREATE TABLE IF NOT EXISTS stellenanzeigen (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                titel TEXT NOT NULL
            )
        """)
        verbindung.commit()

        # Speichert Link und Titel als neuen Eintrag.


# Platzhalter halten die Eingaben vom SQL-Befehl getrennt.
def stellenanzeige_speichern(datenbank_pfad, url, titel):
    """Speichert eine Stellenanzeige und gibt ihre ID zurück."""
    with closing(verbindung_oeffnen(datenbank_pfad)) as verbindung:
        cursor = verbindung.execute(
            "INSERT INTO stellenanzeigen (url, titel) VALUES (?, ?)",
            (url, titel),
        )
        verbindung.commit()

        return cursor.lastrowid
