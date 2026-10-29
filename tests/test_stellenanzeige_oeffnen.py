"""Prüft das Öffnen einer einzelnen Stelle (US 20002) ohne echte Datenbank. (MG)"""

from unittest.mock import MagicMock, Mock

import psycopg

from app import app
from app.datenbank import stellenanzeige_mit_id_lesen

# Eine gespeicherte Stelle als Tupel, so wie fetchone() sie liefert.
# Die Reihenfolge entspricht den Spalten im SELECT.
GESPEICHERTE_ZEILE = (
    7,
    "https://www.jobs.ch/de/stellenangebote/detail/123",
    "Data Analyst",
    "Migros",
    "Zürich",
    "Limmatstrasse 152",
    "8005",
    "Zürich",
    "80-100%",
    "Wir suchen ...",
    "beworben",
    12500,
    18,
)


def datenbank_mit_zeile_ersetzen(monkeypatch, zeile):
    """Ersetzt die Datenbank durch einen Mock, der die gegebene Zeile liefert."""
    # Wie in test_stellenanzeigen_uebersicht.py, nur mit fetchone() statt
    # fetchall(), weil wir genau eine Zeile erwarten.
    testverbindung = MagicMock()
    testverbindung.__enter__.return_value = testverbindung
    testverbindung.execute.return_value.fetchone.return_value = zeile

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen", Mock(return_value=testverbindung)
    )
    return testverbindung


# Requirement 1: Die gefundene Stelle kommt als Dictionary mit Namen zurück.
def test_stelle_wird_als_dictionary_mit_namen_geliefert(monkeypatch):
    datenbank_mit_zeile_ersetzen(monkeypatch, GESPEICHERTE_ZEILE)

    stelle = stellenanzeige_mit_id_lesen("testadresse", 7)

    assert stelle == {
        "id": 7,
        "url": "https://www.jobs.ch/de/stellenangebote/detail/123",
        "titel": "Data Analyst",
        "firma": "Migros",
        "arbeitsort": "Zürich",
        "inseratadresse_strasse": "Limmatstrasse 152",
        "inseratadresse_postleitzahl": "8005",
        "inseratadresse_ort": "Zürich",
        "pensum": "80-100%",
        "stellenbeschreibung": "Wir suchen ...",
        "status": "beworben",
        "strecke_auto_in_metern": 12500,
        "fahrzeit_auto_in_minuten": 18,
    }


# Requirement 2: Findet die Abfrage nichts, kommt None zurück.
def test_ohne_treffer_wird_none_geliefert(monkeypatch):
    datenbank_mit_zeile_ersetzen(monkeypatch, None)

    assert stellenanzeige_mit_id_lesen("testadresse", 999) is None


# Requirement 3: Gesucht wird nach der id und nur beim Demo-Benutzer.
def test_abfrage_sucht_id_nur_beim_demo_benutzer(monkeypatch):
    testverbindung = datenbank_mit_zeile_ersetzen(monkeypatch, None)

    stellenanzeige_mit_id_lesen("testadresse", 7)

    sql, werte = testverbindung.execute.call_args.args
    assert "WHERE id = %s AND benutzer_id = %s" in sql
    assert werte == (7, 1)


# ==================================================
# Route GET /api/stellenanzeigen/<id>
# ==================================================
def stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, ersatz):
    """Ersetzt stellenanzeige_mit_id_lesen() dort, wo die Route sie aufruft."""
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_mit_id_lesen", ersatz
    )
    monkeypatch.setitem(app.config, "DATABASE", "testadresse")


# Requirement 4: Die Route liefert die gefundene Stelle als JSON.
def test_route_liefert_gefundene_stelle_als_json(monkeypatch):
    stelle = {"id": 7, "titel": "Data Analyst", "firma": "Migros"}
    lesen_mock = Mock(return_value=stelle)
    stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, lesen_mock)

    antwort = app.test_client().get("/api/stellenanzeigen/7")

    assert antwort.status_code == 200
    assert antwort.get_json() == stelle
    # Die 7 aus der Adresse kommt als Zahl bei der Datenbankfunktion an.
    lesen_mock.assert_called_once_with("testadresse", 7)


# Requirement 5: Gibt es die Stelle nicht, antwortet die Route mit 404.
def test_route_meldet_unbekannte_stelle_mit_404(monkeypatch):
    stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, Mock(return_value=None))

    antwort = app.test_client().get("/api/stellenanzeigen/999")

    assert antwort.status_code == 404
    assert antwort.get_json() == {"fehler": "Diese Stelle wurde nicht gefunden."}


# Requirement 6: Eine id, die keine Zahl ist, erreicht die Datenbank gar nicht.
def test_route_lehnt_id_ohne_zahl_ab(monkeypatch):
    lesen_mock = Mock()
    stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, lesen_mock)

    antwort = app.test_client().get("/api/stellenanzeigen/abc")

    assert antwort.status_code == 404
    lesen_mock.assert_not_called()


# Requirement 7: Ist die Datenbank nicht erreichbar, kommt eine kurze Meldung.
def test_route_meldet_datenbankfehler_ohne_technische_details(monkeypatch):
    fehler = psycopg.OperationalError("Verbindung zu geheimer-server.neon.tech")
    stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().get("/api/stellenanzeigen/7")

    assert antwort.status_code == 503
    assert antwort.get_json() == {"fehler": "Stelle derzeit nicht verfügbar."}


# Requirement 8: Das Öffnen löst keine Arbeitswegberechnung aus.
def test_route_berechnet_keinen_arbeitsweg(monkeypatch):
    stellenanzeige_mit_id_lesen_ersetzen(monkeypatch, Mock(return_value=None))
    berechnen_mock = Mock()
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.arbeitsweg_berechnen", berechnen_mock
    )

    app.test_client().get("/api/stellenanzeigen/7")

    berechnen_mock.assert_not_called()
