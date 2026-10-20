"""Prüft die PostgreSQL-Anbindung ohne echte Datenbankzugriffe."""

from unittest.mock import Mock

import pytest

from app import app
from app.datenbank import verbindung_oeffnen


def test_verbindung_ohne_adresse():
    """Eine fehlende Datenbankadresse wird verständlich gemeldet."""
    with pytest.raises(ValueError, match="DATABASE_URL fehlt"):
        verbindung_oeffnen(None)


def test_verbindung_uebergibt_adresse(monkeypatch):
    """Die Adresse und das Zeitlimit werden an psycopg übergeben."""
    # Mock simuliert die Verbindungsfunktion ohne Netzwerkzugriff.
    testverbindung = Mock()
    connect_mock = Mock(return_value=testverbindung)
    monkeypatch.setattr("app.datenbank.psycopg.connect", connect_mock)

    testadresse = "postgresql://benutzer:passwort@localhost/test"
    ergebnis = verbindung_oeffnen(testadresse)

    connect_mock.assert_called_once_with(testadresse, connect_timeout=15)
    assert ergebnis is testverbindung


def test_datenbank_status_antwortet_mit_ok(monkeypatch):
    """Die Route fragt die Datenbank ab und schliesst die Verbindung."""
    # Die simulierte Datenbank liefert für SELECT 1 das Ergebnis (1,).
    testverbindung = Mock()
    testverbindung.execute.return_value.fetchone.return_value = (1,)

    verbindung_mock = Mock(return_value=testverbindung)

    # Ersetzt die Funktion dort, wo die Flask-Route sie verwendet.
    monkeypatch.setattr("app.verbindung_oeffnen", verbindung_mock)
    monkeypatch.setitem(app.config, "DATABASE", "testadresse")

    # Ruft die Route ohne laufenden Webserver auf.
    antwort = app.test_client().get("/api/datenbank/status")

    assert antwort.status_code == 200
    assert antwort.get_json() == {"datenbank": "ok"}
    verbindung_mock.assert_called_once_with("testadresse")
    testverbindung.execute.assert_called_once_with("SELECT 1")
    testverbindung.execute.return_value.fetchone.assert_called_once_with()
    testverbindung.close.assert_called_once_with()
