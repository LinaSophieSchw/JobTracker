"""Prüft die SQLite-Verbindung und die Flask-Statusroute."""

from contextlib import closing

from app import app
from app.datenbank import verbindung_oeffnen


# Requirement 1: Eine neue Datenbank kann erstellt und abgefragt werden.
def test_verbindung_erstellt_datenbank(tmp_path):
    """Prüft die Verbindungsfunktion unabhängig von Flask."""
    # pytest stellt einen temporären Ordner für die Testdatenbank bereit.
    datenbank_pfad = tmp_path / "instance" / "test.db"

    with closing(verbindung_oeffnen(datenbank_pfad)) as verbindung:
        ergebnis = verbindung.execute("SELECT 1").fetchone()

    assert ergebnis == (1,)
    assert datenbank_pfad.is_file()


# Requirement 2: Die Statusroute meldet eine erfolgreiche Verbindung.
def test_datenbank_status_antwortet_mit_ok(tmp_path, monkeypatch):
    """Prüft die Statusroute mit einer separaten Testdatenbank."""
    testdatenbank = tmp_path / "instance" / "test.db"

    # Ersetzt den Pfad nur für diesen Test und stellt ihn danach wieder her.
    monkeypatch.setitem(app.config, "DATABASE", testdatenbank)

    # Der Test-Client ruft Flask ohne laufenden Webserver auf.
    antwort = app.test_client().get("/api/datenbank/status")

    assert antwort.status_code == 200
    assert antwort.get_json() == {"datenbank": "ok"}
    assert testdatenbank.is_file()
