"""Prüft das Löschen einer Stelle (US 20005) ohne echte Datenbank. (MG)"""

from unittest.mock import MagicMock, Mock

import psycopg

from app import app
from app.datenbank import stellenanzeige_loeschen


def datenbank_mit_rowcount_ersetzen(monkeypatch, rowcount):
    """Ersetzt die Datenbank durch einen Mock, der so viele Zeilen löscht."""
    # Wie in test_status_aendern.py: 1 heisst «Stelle gefunden und gelöscht»,
    # 0 heisst «nicht gefunden».
    testverbindung = MagicMock()
    testverbindung.__enter__.return_value = testverbindung
    testverbindung.execute.return_value.rowcount = rowcount

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen", Mock(return_value=testverbindung)
    )
    return testverbindung


# Requirement 1: Wird die Stelle gefunden und gelöscht, meldet die Funktion
# True.
def test_geloeschte_stelle_liefert_true(monkeypatch):
    datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    assert stellenanzeige_loeschen("testadresse", 7) is True


# Requirement 2: Gibt es die Stelle nicht, meldet die Funktion False.
def test_unbekannte_stelle_liefert_false(monkeypatch):
    datenbank_mit_rowcount_ersetzen(monkeypatch, 0)

    assert stellenanzeige_loeschen("testadresse", 999) is False


# Requirement 3: Das DELETE löscht nur diese id beim aktuellen Benutzer.
def test_delete_prueft_id_und_benutzer(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    stellenanzeige_loeschen("testadresse", 7)

    sql, werte = testverbindung.execute.call_args.args
    assert "DELETE FROM stellenanzeigen" in sql
    assert "WHERE id = %s AND benutzer_id = %s" in sql
    assert werte == (7, 1)


# ==================================================
# Route DELETE /api/stellenanzeigen/<id>
# ==================================================
def route_vorbereiten(monkeypatch, loeschen_ersatz):
    """Ersetzt die Datenbankfunktion dort, wo die Route sie aufruft."""
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_loeschen", loeschen_ersatz
    )
    monkeypatch.setitem(app.config, "DATABASE", "testadresse")


# Requirement 4: Erfolg liefert 204 ohne Inhalt. KOMPONENTENTEST
def test_route_loescht_stelle_mit_204_ohne_inhalt(monkeypatch):
    loeschen_mock = Mock(return_value=True)
    route_vorbereiten(monkeypatch, loeschen_mock)

    antwort = app.test_client().delete("/api/stellenanzeigen/7")

    assert antwort.status_code == 204
    assert antwort.get_data(as_text=True) == ""
    loeschen_mock.assert_called_once_with("testadresse", 7)


# Requirement 5: Eine unbekannte Stelle gibt 404 mit Meldung.
def test_route_meldet_unbekannte_stelle_mit_404(monkeypatch):
    route_vorbereiten(monkeypatch, Mock(return_value=False))

    antwort = app.test_client().delete("/api/stellenanzeigen/999")

    assert antwort.status_code == 404
    assert antwort.get_json() == {"fehler": "Diese Stelle wurde nicht gefunden."}


# Requirement 6: Ist die Datenbank nicht erreichbar, kommt eine kurze Meldung.
def test_route_meldet_datenbankfehler_ohne_technische_details(monkeypatch):
    fehler = psycopg.OperationalError("Verbindung zu geheimer-server.neon.tech")
    route_vorbereiten(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().delete("/api/stellenanzeigen/7")

    assert antwort.status_code == 503
    assert "neon.tech" not in antwort.get_data(as_text=True)
