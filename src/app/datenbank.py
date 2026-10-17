"""Öffnet die Verbindung zur lokalen SQLite-Datenbank."""

import sqlite3
from pathlib import Path


def verbindung_oeffnen(datenbank_pfad):
    """Erstellt bei Bedarf die Datenbank und öffnet eine Verbindung."""
    datenbank_pfad = Path(datenbank_pfad)

    # SQLite erstellt die Datei, aber nicht den übergeordneten Ordner.
    datenbank_pfad.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(datenbank_pfad)
