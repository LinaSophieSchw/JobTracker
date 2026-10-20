"""Prüft Eingabeprüfung und Speicherung von Stellenanzeigen."""

from unittest.mock import MagicMock, Mock

import psycopg
import pytest

from app import app
from app.datenbank import (
    stellenanzeige_eingaben_pruefen,
    stellenanzeige_speichern,
    textfeld_pruefen,
)


# Requirement: Eingaben vor dem Speichern bereinigen und prüfen.
def test_textfeld_entfernt_aeussere_leerzeichen():
    """Behält den Inhalt ohne überflüssige Randabstände."""
    assert textfeld_pruefen(" Rega ", "Firma") == "Rega"


def test_optionales_leeres_textfeld_wird_none():
    """Leere optionale Angaben werden später als NULL gespeichert."""
    assert textfeld_pruefen("   ", "Arbeitsort") is None


def test_leeres_pflichtfeld_wird_abgelehnt():
    """Ein Pflichtfeld darf nicht nur Leerzeichen enthalten."""
    with pytest.raises(ValueError, match="Firma"):
        textfeld_pruefen(" ", "Firma", pflicht=True)


def test_zu_langes_textfeld_wird_abgelehnt():
    """Verhindert Werte oberhalb der vereinbarten Maximallänge."""
    with pytest.raises(ValueError, match="höchstens"):
        textfeld_pruefen("A" * 201, "Titel", maximale_laenge=200)


def test_formularwerte_werden_bereinigt():
    """Normalisiert den Link und ignoriert eine gesendete Benutzer-ID."""
    job_id = "ac2fdcb3-f807-41b3-8914-d973ec426dd4"
    daten = {
        "url": f"https://www.jobs.ch/de/stellenangebote/?jobid={job_id}",
        "titel": " Pilot ",
        "firma": " Rega ",
        "arbeitsort": " ",
        "benutzer_id": 999,
    }

    ergebnis = stellenanzeige_eingaben_pruefen(daten)

    assert ergebnis["url"] == (
        f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"
    )
    assert ergebnis["titel"] == "Pilot"
    assert ergebnis["firma"] == "Rega"
    assert ergebnis["arbeitsort"] is None
    assert "benutzer_id" not in ergebnis


def test_unvollstaendige_adresse_wird_abgelehnt():
    """Eine angegebene Adresse muss das vereinbarte Format erfüllen."""
    daten = {
        "url": (
            "https://www.jobs.ch/de/stellenangebote/detail/"
            "ac2fdcb3-f807-41b3-8914-d973ec426dd4/"
        ),
        "titel": "Pilot",
        "firma": "Rega",
        "adresse": "Samedan",
    }

    with pytest.raises(ValueError, match="Adresse"):
        stellenanzeige_eingaben_pruefen(daten)


# Requirement: Die Speicherroute bestätigt Erfolg und meldet Eingabefehler.
def test_speicherroute_bestaetigt_neuen_eintrag(monkeypatch):
    """Übermittelt Formularwerte an die Speicherfunktion und liefert HTTP 201."""
    daten = {"url": "testlink", "titel": "Pilot", "firma": "Rega"}
    speichern_mock = Mock(return_value=42)

    # Ersetzt die Speicherfunktion: Es erfolgt kein echter Datenbankzugriff.
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        speichern_mock,
    )
    monkeypatch.setitem(app.config, "DATABASE", "testdatenbank")

    antwort = app.test_client().post("/api/stellenanzeigen", json=daten)

    assert antwort.status_code == 201
    assert antwort.get_json() == {"id": 42}
    speichern_mock.assert_called_once_with("testdatenbank", daten)


def test_speicherroute_meldet_eingabefehler(monkeypatch):
    """Eine abgelehnte Eingabe darf nicht als Erfolg erscheinen."""
    speichern_mock = Mock(side_effect=ValueError("Bitte Firma eingeben."))

    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        speichern_mock,
    )

    antwort = app.test_client().post("/api/stellenanzeigen", json={})

    assert antwort.status_code == 400
    assert antwort.get_json() == {"fehler": "Bitte Firma eingeben."}


# Requirement: Speichern liefert die ID und verhindert doppelte Einträge.
def test_speichern_liefert_id_und_verwendet_demo_benutzer(monkeypatch):
    """Übergibt bereinigte Werte und übernimmt keine fremde Benutzer-ID."""
    daten = {
        "url": (
            "https://www.jobs.ch/de/stellenangebote/detail/"
            "ac2fdcb3-f807-41b3-8914-d973ec426dd4/"
        ),
        "titel": " Pilot ",
        "firma": " Rega ",
        "benutzer_id": 999,
    }

    # MagicMock kann auch einen with-Block simulieren.
    verbindung = MagicMock()
    verbindung.__enter__.return_value = verbindung
    verbindung.execute.return_value.fetchone.return_value = (42,)

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen",
        Mock(return_value=verbindung),
    )

    neue_id = stellenanzeige_speichern("testdatenbank", daten)

    assert neue_id == 42

    # Prüft die übergebenen Werte statt der SQL-Formatierung.
    parameter = verbindung.execute.call_args.args[1]
    assert parameter == (1, daten["url"], "Pilot", "Rega", None, None, None, None)


def test_speichern_meldet_bestehenden_eintrag(monkeypatch):
    """Ein Duplikat liefert eine Meldung mit der vorhandenen ID."""
    daten = {
        "url": (
            "https://www.jobs.ch/de/stellenangebote/detail/"
            "ac2fdcb3-f807-41b3-8914-d973ec426dd4/"
        ),
        "titel": "Pilot",
        "firma": "Rega",
    }

    verbindung = MagicMock()
    verbindung.__enter__.return_value = verbindung

    # INSERT liefert keine neue ID; SELECT findet den vorhandenen Eintrag.
    verbindung.execute.return_value.fetchone.side_effect = [None, (7,)]

    monkeypatch.setattr(
        "app.datenbank.verbindung_oeffnen",
        Mock(return_value=verbindung),
    )

    with pytest.raises(ValueError, match=r"bereits gespeichert \(ID: 7\)"):
        stellenanzeige_speichern("testdatenbank", daten)

    # Auch die Suche nach dem Duplikat muss auf den Benutzer begrenzt sein.
    parameter = verbindung.execute.call_args.args[1]
    assert parameter == (1, daten["url"])


def test_speicherroute_meldet_datenbankausfall(monkeypatch):
    """Liefert HTTP 503 ohne interne Fehlerdetails."""
    # Simuliert einen Verbindungsfehler statt eines echten Datenbankzugriffs.
    speichern_mock = Mock(
        side_effect=psycopg.OperationalError("Interne Test-Fehlerdetails")
    )

    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        speichern_mock,
    )

    antwort = app.test_client().post(
        "/api/stellenanzeigen",
        json={"titel": "Pilot", "firma": "Rega"},
    )

    assert antwort.status_code == 503
    assert antwort.get_json() == {
        "fehler": ("Speichern derzeit nicht möglich. " "Bitte später erneut versuchen.")
    }
    assert b"Interne Test-Fehlerdetails" not in antwort.data
