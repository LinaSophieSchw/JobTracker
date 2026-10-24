"""Prüft die Übersicht aller Stellen (US 20001) ohne echte Datenbank. (MG)"""

from unittest.mock import MagicMock, Mock

import psycopg

from app import app
from app.datenbank import stellenanzeigen_lesen


def datenbank_mit_zeilen_ersetzen(monkeypatch, zeilen):
    """Ersetzt die Datenbank durch einen Mock, der die gegebenen Zeilen liefert."""
    # MagicMock kann im with-Block stehen. __enter__ bestimmt, was nach
    # «as verbindung» ankommt: wieder dieselbe Testverbindung.
    testverbindung = MagicMock()
    testverbindung.__enter__.return_value = testverbindung
    testverbindung.execute.return_value.fetchall.return_value = zeilen

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen", Mock(return_value=testverbindung)
    )
    return testverbindung


# Requirement 1: Jede Stelle kommt mit den Spalten der Übersicht zurück.
def test_stellen_werden_als_dictionaries_mit_namen_geliefert(monkeypatch):
    datenbank_mit_zeilen_ersetzen(
        monkeypatch,
        [(7, "Data Analyst", "Migros", "Zürich", "beworben", 12500, 18)],
    )

    stellen = stellenanzeigen_lesen("testadresse")

    assert stellen == [
        {
            "id": 7,
            "titel": "Data Analyst",
            "firma": "Migros",
            "arbeitsort": "Zürich",
            "status": "beworben",
            "strecke_auto_in_metern": 12500,
            "fahrzeit_auto_in_minuten": 18,
        }
    ]


# Requirement 2: Ohne gespeicherte Stellen ist die Liste leer.
def test_ohne_stellen_wird_eine_leere_liste_geliefert(monkeypatch):
    datenbank_mit_zeilen_ersetzen(monkeypatch, [])

    assert stellenanzeigen_lesen("testadresse") == []


# Requirement 3: Nur Stellen des Demo-Benutzers, die neueste zuerst.
def test_abfrage_liest_nur_eigene_stellen_neueste_zuerst(monkeypatch):
    testverbindung = datenbank_mit_zeilen_ersetzen(monkeypatch, [])

    stellenanzeigen_lesen("testadresse")

    # call_args enthält, womit execute() aufgerufen wurde:
    # args[0] ist der SQL-Text, args[1] die Werte für die Platzhalter.
    sql, werte = testverbindung.execute.call_args.args
    assert "ORDER BY erstellt_am DESC" in sql
    assert werte == (1,)


# ==================================================
# Route GET /api/stellenanzeigen
# ==================================================
def stellenanzeigen_lesen_ersetzen(monkeypatch, ersatz):
    """Ersetzt stellenanzeigen_lesen() dort, wo die Route sie aufruft."""
    # Die Route hat die Funktion mit «from .datenbank import ...» geholt.
    # Darum ersetzen wir sie in stellenanzeigen_routes und nicht in datenbank.
    monkeypatch.setattr("app.stellenanzeigen_routes.stellenanzeigen_lesen", ersatz)
    monkeypatch.setitem(app.config, "DATABASE", "testadresse")


# Requirement 4: Die Route liefert die Stellen als JSON-Liste.
def test_route_liefert_stellen_als_json_liste(monkeypatch):
    stelle = {"id": 7, "titel": "Data Analyst", "firma": "Migros"}
    stellenanzeigen_lesen_ersetzen(monkeypatch, Mock(return_value=[stelle]))

    # Der Test-Client spielt den Browser, ohne dass ein Server laufen muss.
    antwort = app.test_client().get("/api/stellenanzeigen")

    assert antwort.status_code == 200
    assert antwort.get_json() == [stelle]


# Requirement 5: Ohne Stellen liefert die Route eine leere Liste.
def test_route_liefert_ohne_stellen_eine_leere_liste(monkeypatch):
    stellenanzeigen_lesen_ersetzen(monkeypatch, Mock(return_value=[]))

    antwort = app.test_client().get("/api/stellenanzeigen")

    assert antwort.status_code == 200
    assert antwort.get_json() == []


# Requirement 6: Ist die Datenbank nicht erreichbar, kommt eine kurze Meldung.
def test_route_meldet_datenbankfehler_ohne_technische_details(monkeypatch):
    # side_effect: Statt etwas zurückzugeben, löst der Mock diesen Fehler aus.
    fehler = psycopg.OperationalError("Verbindung zu geheimer-server.neon.tech")
    stellenanzeigen_lesen_ersetzen(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().get("/api/stellenanzeigen")

    assert antwort.status_code == 503
    assert antwort.get_json() == {"fehler": "Übersicht derzeit nicht verfügbar."}


# Requirement 7: Das Laden der Übersicht löst keine Arbeitswegberechnung aus.
def test_route_berechnet_keinen_arbeitsweg(monkeypatch):
    stellenanzeigen_lesen_ersetzen(monkeypatch, Mock(return_value=[]))
    berechnen_mock = Mock()
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.arbeitsweg_berechnen", berechnen_mock
    )

    app.test_client().get("/api/stellenanzeigen")

    berechnen_mock.assert_not_called()
