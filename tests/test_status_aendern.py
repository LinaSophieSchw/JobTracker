"""Prüft das Ändern einer Stelle ohne echte Datenbank. (MG)

US 20003 hat nur den Status geändert. Seit US 20004 schickt der PUT alle
Felder ausser der url; die Tests verwenden darum vollständige Formularwerte.
"""

from unittest.mock import MagicMock, Mock

import psycopg
import pytest

from app import app
from app.datenbank import stellenanzeige_aktualisieren


def formularwerte(**aenderungen):
    """Liefert vollständige Formularwerte; einzelne Felder lassen sich ändern."""
    # So muss nicht jeder Test alle Felder aufzählen. Ein Test, der nur
    # einen leeren Titel prüfen will, schreibt formularwerte(titel="").
    werte = {
        "titel": "Software Engineer",
        "firma": "Beispiel AG",
        "arbeitsort": "Zürich",
        "inseratadresse_strasse": "Limmatstrasse 152",
        "inseratadresse_postleitzahl": "8005",
        "inseratadresse_ort": "Zürich",
        "pensum": "80-100%",
        "stellenbeschreibung": "Entwickeln von Webapplikationen.",
        "status": "beworben",
    }
    werte.update(aenderungen)
    return werte


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

    assert stellenanzeige_aktualisieren("testadresse", 7, formularwerte()) is True


# Requirement 2: Gibt es die Stelle nicht, meldet die Funktion False.
def test_unbekannte_stelle_liefert_false(monkeypatch):
    datenbank_mit_rowcount_ersetzen(monkeypatch, 0)

    assert stellenanzeige_aktualisieren("testadresse", 999, formularwerte()) is False


# Requirement 3: Das UPDATE setzt geaendert_am und filtert nach Benutzer.
def test_update_setzt_zeitstempel_und_prueft_benutzer(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    stellenanzeige_aktualisieren("testadresse", 7, formularwerte())

    sql, werte = testverbindung.execute.call_args.args
    assert "geaendert_am = CURRENT_TIMESTAMP" in sql
    assert "WHERE id = %s AND benutzer_id = %s" in sql
    # Die letzten zwei Werte gehören zum WHERE: id 7 und Demo-Benutzer 1.
    assert werte[-2:] == (7, 1)


# Requirement 4: Alle Felder werden gespeichert, bereinigt wie beim Erfassen.
def test_update_speichert_alle_felder(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    stellenanzeige_aktualisieren(
        "testadresse", 7, formularwerte(titel="  Data Engineer  ", pensum="")
    )

    sql, werte = testverbindung.execute.call_args.args
    assert werte == (
        "Data Engineer",  # Leerzeichen am Rand entfernt
        "Beispiel AG",
        "Zürich",
        "Limmatstrasse 152",
        "8005",
        "Zürich",
        None,  # leeres Pensum wird zu None
        "Entwickeln von Webapplikationen.",
        "beworben",
        7,
        1,
    )


# Requirement 5: Die url wird nie geändert, auch wenn sie mitgeschickt wird.
def test_update_aendert_die_url_nicht(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    stellenanzeige_aktualisieren(
        "testadresse", 7, formularwerte(url="https://www.jobs.ch/andere")
    )

    sql, werte = testverbindung.execute.call_args.args
    assert "url" not in sql
    assert "https://www.jobs.ch/andere" not in werte


# Requirement 6: Fehlt ein Pflichtfeld, wird die Datenbank nicht gefragt.
@pytest.mark.parametrize("feld", ["titel", "firma"])
def test_leeres_pflichtfeld_wird_abgelehnt(monkeypatch, feld):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    # pytest.raises prüft, dass genau dieser Fehler entsteht.
    with pytest.raises(ValueError):
        stellenanzeige_aktualisieren("testadresse", 7, formularwerte(**{feld: " "}))

    testverbindung.execute.assert_not_called()


# Requirement 7: Ein unbekannter Status wird abgelehnt, bevor die Datenbank
# gefragt wird.
def test_unbekannter_status_wird_abgelehnt(monkeypatch):
    testverbindung = datenbank_mit_rowcount_ersetzen(monkeypatch, 1)

    with pytest.raises(ValueError):
        stellenanzeige_aktualisieren("testadresse", 7, formularwerte(status="verliebt"))

    testverbindung.execute.assert_not_called()


# ==================================================
# Route PUT /api/stellenanzeigen/<id>
# ==================================================
def route_vorbereiten(monkeypatch, aktualisieren_ersatz):
    """Ersetzt Datenbank und Arbeitsweg dort, wo die Route sie aufruft."""
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_aktualisieren",
        aktualisieren_ersatz,
    )
    # So liefert stellenanzeige_mit_id_lesen() die Stelle nach dem Speichern.
    stelle = {
        "status": "beworben",
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


# Requirement 8: Erfolg liefert 200 mit Status und neuem Arbeitsweg.
def test_route_speichert_angaben_und_liefert_arbeitsweg(monkeypatch):
    route_vorbereiten(monkeypatch, Mock(return_value=True))

    antwort = app.test_client().put("/api/stellenanzeigen/7", json=formularwerte())

    assert antwort.status_code == 200
    assert antwort.get_json() == {
        "id": 7,
        "status": "beworben",
        "fahrzeit_auto_in_minuten": 18,
        "strecke_auto_in_metern": 12500,
    }


# Requirement 9: Die Route reicht alle Formularwerte an die Datenbank weiter.
def test_route_uebergibt_alle_formularwerte(monkeypatch):
    aktualisieren_mock = Mock(return_value=True)
    route_vorbereiten(monkeypatch, aktualisieren_mock)

    app.test_client().put("/api/stellenanzeigen/7", json=formularwerte())

    datenbank_url, stellen_id, daten = aktualisieren_mock.call_args.args
    assert stellen_id == 7
    assert daten == formularwerte()


# Requirement 10: Jedes Speichern berechnet den Arbeitsweg mit den
# gespeicherten Adressen der Stelle neu.
def test_route_berechnet_arbeitsweg_mit_gespeicherter_adresse(monkeypatch):
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(return_value=True))

    app.test_client().put("/api/stellenanzeigen/7", json=formularwerte())

    stellen_id, daten = eintragen_mock.call_args.args
    assert stellen_id == 7
    assert daten["inseratadresse_ort"] == "Zürich"


# Requirement 11: Eine unbekannte Stelle gibt 404, ohne Berechnung.
def test_route_meldet_unbekannte_stelle_mit_404(monkeypatch):
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(return_value=False))

    antwort = app.test_client().put("/api/stellenanzeigen/999", json=formularwerte())

    assert antwort.status_code == 404
    assert antwort.get_json() == {"fehler": "Diese Stelle wurde nicht gefunden."}
    eintragen_mock.assert_not_called()


# Requirement 12: Ungültige Angaben geben 400, ohne Berechnung.
def test_route_meldet_ungueltige_angaben_mit_400(monkeypatch):
    fehler = ValueError("Bitte Titel eingeben.")
    eintragen_mock = route_vorbereiten(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().put(
        "/api/stellenanzeigen/7", json=formularwerte(titel="")
    )

    assert antwort.status_code == 400
    assert antwort.get_json() == {"fehler": "Bitte Titel eingeben."}
    eintragen_mock.assert_not_called()


# Requirement 13: Ist die Datenbank nicht erreichbar, kommt eine kurze Meldung.
def test_route_meldet_datenbankfehler_ohne_technische_details(monkeypatch):
    fehler = psycopg.OperationalError("Verbindung zu geheimer-server.neon.tech")
    route_vorbereiten(monkeypatch, Mock(side_effect=fehler))

    antwort = app.test_client().put("/api/stellenanzeigen/7", json=formularwerte())

    assert antwort.status_code == 503
    assert "neon.tech" not in antwort.get_data(as_text=True)
