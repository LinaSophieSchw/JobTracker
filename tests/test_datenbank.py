"""Prüft die PostgreSQL-Anbindung ohne echte Datenbankzugriffe."""

from unittest.mock import MagicMock, Mock

import pytest

from app import app
from app.datenbank import (
    tabellen_erstellen,
    verbindung_oeffnen,
    wohnadresse_lesen,
)


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


# ==================================================
# US 30004: Demo-Benutzer mit Wohnadresse fest hinterlegen (FH)
# ==================================================
def demo_benutzer_befehl_finden(verbindung):
    """Sucht unter allen SQL-Befehlen den INSERT für den Demo-Benutzer."""
    # tabellen_erstellen() führt mehrere Befehle aus. call_args_list
    # enthält alle Aufrufe von execute() in der Reihenfolge.
    for aufruf in verbindung.execute.call_args_list:
        if "INSERT INTO benutzer" in aufruf.args[0]:
            return aufruf
    return None


# Requirement 1: Der Demo-Benutzer hat die Wohnadresse in drei Feldern.
def test_demo_benutzer_wird_mit_wohnadresse_in_drei_teilen_angelegt(monkeypatch):
    """Strasse, Postleitzahl und Ort werden getrennt eingefügt.

    Wofür: Die Arbeitswegberechnung liest die Wohnadresse später in drei
    Teilen. Der Test wird rot, wenn jemand den Demo-Benutzer ändert, z. B.
    die Adresse wieder in ein Feld schreibt, Postleitzahl und Ort vertauscht
    oder eine andere id als 1 verwendet. Ob das SQL selbst stimmt, prüft er
    nicht; das zeigt erst ein Versuch mit der echten Datenbank.
    """
    # Statt Neon verwenden wir eine nachgebaute Verbindung. Sie nimmt alle
    # Befehle entgegen und merkt sich, womit execute() aufgerufen wurde.
    # MagicMock kann auch einen with-Block simulieren.
    verbindung = MagicMock()
    verbindung.__enter__.return_value = verbindung
    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen",
        Mock(return_value=verbindung),
    )

    tabellen_erstellen("testdatenbank")

    # args[0] ist der SQL-Text, args[1] sind die Werte für die %s-Platzhalter.
    aufruf = demo_benutzer_befehl_finden(verbindung)
    assert aufruf is not None
    assert aufruf.args[1] == (1, "Demo-Benutzer", "Bundesplatz 3", "3005", "Bern")


# Requirement 2: Die Wohnadresse kann für die Arbeitswegberechnung gelesen werden.
def test_wohnadresse_wird_in_drei_teilen_gelesen(monkeypatch):
    """Die Datenbankzeile wird zu einem Dictionary mit drei Namen.

    Wofür: Die Arbeitswegberechnung greift später über die Namen
    «strasse», «postleitzahl» und «ort» auf die Adresse zu. Der Test prüft
    auch, dass nach dem Demo-Benutzer mit id 1 gefragt wird.
    """
    # Die nachgebaute Datenbank antwortet mit einer Zeile wie PostgreSQL.
    verbindung = MagicMock()
    verbindung.__enter__.return_value = verbindung
    verbindung.execute.return_value.fetchone.return_value = (
        "Bundesplatz 3",
        "3005",
        "Bern",
    )
    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen",
        Mock(return_value=verbindung),
    )

    wohnadresse = wohnadresse_lesen("testdatenbank")

    assert wohnadresse == {
        "strasse": "Bundesplatz 3",
        "postleitzahl": "3005",
        "ort": "Bern",
    }
    assert verbindung.execute.call_args.args[1] == (1,)


def test_fehlender_benutzer_liefert_keine_wohnadresse(monkeypatch):
    """Ohne Benutzer gibt die Funktion None zurück, statt abzustürzen.

    Wofür: Fehlt der Demo-Benutzer, z. B. weil die Tabellen noch nicht
    angelegt wurden, soll die Arbeitswegberechnung das erkennen können.
    Sie zeigt dann «Arbeitsweg konnte nicht berechnet werden.» an.
    """
    # fetchone() liefert None, wenn keine Zeile gefunden wird.
    verbindung = MagicMock()
    verbindung.__enter__.return_value = verbindung
    verbindung.execute.return_value.fetchone.return_value = None
    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen",
        Mock(return_value=verbindung),
    )

    assert wohnadresse_lesen("testdatenbank") is None
