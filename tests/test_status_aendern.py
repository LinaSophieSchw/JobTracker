"""Prüft das Ändern des Status (US 20003) ohne echte Datenbank. (MG)"""

from unittest.mock import MagicMock, Mock

import psycopg
import pytest

from app import app
from app.datenbank import status_speichern


def datenbank_mit_rowcount_ersetzen(monkeypatch, rowcount):
    """Ersetzt die Datenbank durch einen Mock, der so viele Zeilen ändert."""
    # Wie in test_stellenanzeige_oeffnen.py. Statt fetchone() geben wir hier
    # rowcount vor: 1 heisst «Stelle gefunden», 0 heisst «nicht gefunden».
    testverbindung = MagicMock()
    testverbindung.__enter__.return_value = testverbindung
    testverbindung.execute.return_value.rowcount = rowcount

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen", Mock(return_value=testverbindung)
    )
    return testverbindung


# Requirement 1: Wird die Stelle gefunden, meldet die Funktion True.
def test_gefundene_stelle_liefert_true(monkeypatch):
    datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    assert status_speichern("testadresse", 7, "beworben") is True


# Requirement 2: Gibt es die Stelle nicht, meldet die Funktion False.
def test_unbekannte_stelle_liefert_false(monkeypatch):
    datenbank_mit_rowcount_ersetzen(monkeypatch, 0)

    assert status_speichern("testadresse", 999, "beworben") is False


# Requirement 3: Das UPDATE setzt geaendert_am und filtert nach Benutzer.
def test_update_setzt_zeitstempel_und_prueft_benutzer(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    status_speichern("testadresse", 7, "interview")

    sql, werte = testverbindung.execute.call_args.args
    assert "geaendert_am = CURRENT_TIMESTAMP" in sql
    assert "WHERE id = %s AND benutzer_id = %s" in sql
    assert werte == ("interview", 7, 1)


# Requirement 4: Ein unbekannter Status wird abgelehnt, bevor die Datenbank
# gefragt wird.
def test_unbekannter_status_wird_abgelehnt(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    # pytest.raises prüft, dass genau dieser Fehler entsteht.
    with pytest.raises(ValueError):
        status_speichern("testadresse", 7, "verliebt")

    testverbindung.execute.assert_not_called()


# ==================================================
# Route PUT /api/stellenanzeigen/<id>
# ==================================================
def route_vorbereiten(monkeypatch, status_ersatz):
    """Ersetzt Datenbank und Arbeitsweg dort, wo die Route sie aufruft."""
    monkeypatch.setattr("app.stellenanzeigen_routes.status_speichern", status_ersatz)
    stelle = {
        "inseratadresse_strasse": "Limmatstrasse 152",
        "inseratadresse_postleitzahl": "8005",
        "inseratadresse_ort": "Zürich",
    }
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_mit_id_lesen",
        Mock(return_value=stelle),
    )
    # Fabios Funktion ersetzen wir ganz, damit kein Kartendienst gefragt wird.
    eintragen_mock = Mock(
        return_value={"fahrzeit_auto_in_minuten": 18, "strecke_auto_in_metern": 12500}
    )
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.arbeitsweg_eintragen", eintragen_mock
    )
    monkeypatch.setitem(app.config, "DATABASE", "testadresse")
    return eintragen_mock


# Requirement 5: Erfolg liefert 200 mit Status und neuem Arbeitsweg.
def test_route_speichert_status_und_liefert_arbeitsweg(monkeypatch):
    route_vorbereiten(monkeypatch, Mock(return_value=True))

    antwort = app.test_client().put(
        "/api/stellenanzeigen/7", json={"status": "beworben"}
    )

    assert antwort.status_code == 200
    assert antwort.get_json() == {
        "id": 7,
        "status": "beworben",
        "fahrzeit_auto_in_minuten": 18,
        "strecke_auto_in_metern": 12500,
    }


# Requirement 6: Jedes Speichern berechnet den Arbeitsweg mit den
# gespeicherten Adressen der Stelle neu.
def test_route_berechnet_arbeitsweg_mit_gespeicherter_adresse(monkeypatch):
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(return_value=True))

    app.test_client().put("/api/stellenanzeigen/7", json={"status": "beworben"})

    stellen_id, daten = eintragen_mock.call_args.args
    assert stellen_id == 7
    assert daten["inseratadresse_ort"] == "Zürich"


# Requirement 7: Eine unbekannte Stelle gibt 404, ohne Berechnung.
def test_route_meldet_unbekannte_stelle_mit_404(monkeypatch):
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(return_value=False))

    antwort = app.test_client().put(
        "/api/stellenanzeigen/999", json={"status": "beworben"}
    )

    assert antwort.status_code == 404
    assert antwort.get_json() == {"fehler": "Diese Stelle wurde nicht gefunden."}
    eintragen_mock.assert_not_called()


# Requirement 8: Ein ungültiger Status gibt 400, ohne Berechnung.
def test_route_meldet_ungueltigen_status_mit_400(monkeypatch):
    fehler = ValueError("Bitte einen gültigen Status wählen.")
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().put(
        "/api/stellenanzeigen/7", json={"status": "verliebt"}
    )

    assert antwort.status_code == 400
    assert antwort.get_json() == {"fehler": "Bitte einen gültigen Status wählen."}
    eintragen_mock.assert_not_called()


# Requirement 9: Ist die Datenbank nicht erreichbar, kommt eine kurze Meldung.
def test_route_meldet_datenbankfehler_ohne_technische_details(monkeypatch):
    fehler = psycopg.OperationalError("Verbindung zu geheimer-server.neon.tech")
    route_vorbereiten(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().put(
        "/api/stellenanzeigen/7", json={"status": "beworben"}
    )

    assert antwort.status_code == 503
    assert "neon.tech" not in antwort.get_data(as_text=True)
