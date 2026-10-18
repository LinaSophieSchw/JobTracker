"""Prüft die Titelvorschau ohne Internetzugriff."""

import pytest

from app import app
from app.stellenanzeige_erfassen import (
    anzeigenlink_bestimmen,
    stellentitel_aus_html_lesen,
)


# Requirement 1: Der Titel wird aus dem HTML gelesen.
def test_titel_wird_aus_hauptueberschrift_gelesen():
    """Entfernt HTML-Tags aus dem gefundenen Titel."""
    assert stellentitel_aus_html_lesen("<h1> Pilot 100% </h1>") == "Pilot 100%"


def test_fehlender_titel_wird_gemeldet():
    """Ein Dokument ohne Hauptüberschrift liefert keinen erfundenen Titel."""
    with pytest.raises(ValueError, match="kein Titel"):
        stellentitel_aus_html_lesen("<p>Keine Stellenanzeige</p>")


# Requirement 2: Suchlinks werden in direkte Anzeigenlinks umgewandelt.
def test_suchlink_wird_in_anzeigenlink_umgewandelt():
    """Übernimmt die Stellen-ID aus dem Suchparameter."""
    job_id = "ac2fdcb3-f807-41b3-8914-d973ec426dd4"
    url = f"https://www.jobs.ch/de/stellenangebote/?term=pilot&jobid={job_id}"
    assert anzeigenlink_bestimmen(url) == (
        f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"
    )


def test_fremder_anbieter_wird_abgelehnt():
    """Nicht unterstützte Anbieter werden vor einem Abruf abgelehnt."""
    with pytest.raises(ValueError, match="www.jobs.ch"):
        anzeigenlink_bestimmen("https://example.com/anzeige")


# Requirement 3: Die Route liefert eine Vorschau oder verständliche Fehler.
def test_route_liefert_titelvorschau(monkeypatch):
    """Ersetzt den Internetabruf durch eine feste Testantwort."""
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellentitel_auslesen",
        lambda url: "Helikopterpilot",
    )
    url = "https://www.jobs.ch/de/stellenangebote/?jobid=test"
    antwort = app.test_client().post("/api/stellenanzeigen/vorschau", json={"url": url})
    assert antwort.status_code == 200
    assert antwort.get_json() == {"url": url, "titel": "Helikopterpilot"}


def test_route_lehnt_leeren_link_ab():
    """Ohne Link wird kein Internetabruf ausgelöst."""
    antwort = app.test_client().post("/api/stellenanzeigen/vorschau", json={"url": ""})
    assert antwort.status_code == 400
    assert antwort.get_json() == {"fehler": "Bitte einen Link eingeben."}
