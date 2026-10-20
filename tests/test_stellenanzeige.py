"""Prüft die Titelvorschau ohne Internetzugriff."""

import json

import pytest

from app import app
from app.stellenanzeige_erfassen import (
    anzeigenlink_bestimmen,
    beschreibung_aus_daten_lesen,
    firma_aus_daten_lesen,
    ort_und_adresse_aus_daten_lesen,
    pensum_aus_html_lesen,
    stellenanzeige_daten_finden,
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
def test_route_liefert_alle_vorschaufelder(monkeypatch):
    """Prüft die vollständige JSON-Antwort ohne Internetzugriff."""
    testvorschau = {
        "url": (
            "https://www.jobs.ch/de/stellenangebote/detail/"
            "ac2fdcb3-f807-41b3-8914-d973ec426dd4/"
        ),
        "titel": "Helikopterpilot",
        "firma": "Testfirma",
        "arbeitsort": "Samedan",
        "adresse": "Plazza Aviatica 6, 7503 Samedan",
        "pensum": "100%",
        "stellenbeschreibung": "Beschreibung der Teststelle.",
    }

    # Ersetzt die neue Auslesefunktion durch vorbereitete Testdaten.
    # Damit prüft dieser Test die Route unabhängig von jobs.ch.
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_auslesen",
        lambda url: testvorschau,
    )

    antwort = app.test_client().post(
        "/api/stellenanzeigen/vorschau",
        json={"url": testvorschau["url"]},
    )

    assert antwort.status_code == 200
    assert antwort.get_json() == testvorschau


def test_route_lehnt_leeren_link_ab():
    """Ohne Link wird kein Internetabruf ausgelöst."""
    antwort = app.test_client().post("/api/stellenanzeigen/vorschau", json={"url": ""})
    assert antwort.status_code == 400
    assert antwort.get_json() == {"fehler": "Bitte einen Link eingeben."}


# Requirement 4: Es werden nur eindeutig zugeordnete Anzeigendaten gelesen.
def test_passende_stellen_id_wird_ausgewaehlt():
    """Ignoriert eine fremde Anzeige vor der gesuchten Anzeige."""
    daten = [
        {
            "@type": "JobPosting",
            "identifier": {"value": "fremde-id"},
            "title": "Andere Stelle",
        },
        {
            "@type": "JobPosting",
            "identifier": {"value": "gesuchte-id"},
            "title": "Gesuchte Stelle",
        },
    ]
    html = '<script type="application/ld+json">' + json.dumps(daten) + "</script>"

    ergebnis = stellenanzeige_daten_finden(html, "gesuchte-id")

    assert ergebnis["title"] == "Gesuchte Stelle"


def test_anzeige_ohne_kennung_mit_passender_seitenadresse():
    """Erlaubt einen einzelnen Datenblock bei bestätigter Seitenadresse."""
    job_id = "02ae4db9-d71e-4ed3-99e8-f4c4cf71413b"
    url = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"
    daten = {"@type": "JobPosting", "title": "Helikoptermechaniker"}
    html = (
        f'<link rel="canonical" href="{url}">'
        '<script type="application/ld+json">' + json.dumps(daten) + "</script>"
    )

    ergebnis = stellenanzeige_daten_finden(html, job_id)

    assert ergebnis["title"] == "Helikoptermechaniker"


def test_fremde_stellen_id_wird_abgelehnt():
    """Eine fremde Kennung darf nicht durch die Seitenadresse übergangen werden."""
    job_id = "02ae4db9-d71e-4ed3-99e8-f4c4cf71413b"
    url = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"
    daten = {
        "@type": "JobPosting",
        "identifier": {"value": "fremde-id"},
        "title": "Andere Stelle",
    }
    html = (
        f'<link rel="canonical" href="{url}">'
        '<script type="application/ld+json">' + json.dumps(daten) + "</script>"
    )

    with pytest.raises(ValueError):
        stellenanzeige_daten_finden(html, job_id)


def test_mehrere_anzeigen_ohne_kennung_werden_abgelehnt():
    """Ohne Kennung darf bei mehreren Anzeigen keine geraten werden."""
    job_id = "02ae4db9-d71e-4ed3-99e8-f4c4cf71413b"
    url = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"
    daten = [
        {"@type": "JobPosting", "title": "Erste Stelle"},
        {"@type": "JobPosting", "title": "Zweite Stelle"},
    ]
    html = (
        f'<link rel="canonical" href="{url}">'
        '<script type="application/ld+json">' + json.dumps(daten) + "</script>"
    )

    with pytest.raises(ValueError):
        stellenanzeige_daten_finden(html, job_id)


# Requirement 5: Importfelder werden korrekt gelesen.
def test_firma_wird_gelesen():
    """Entfernt äussere Leerzeichen beim Firmennamen."""
    daten = {"hiringOrganization": {"name": " Rega "}}

    assert firma_aus_daten_lesen(daten) == "Rega"


def test_fehlende_firma_bleibt_leer():
    """Erfindet keinen Firmennamen."""
    assert firma_aus_daten_lesen({}) == ""


def test_arbeitsort_und_adresse_werden_getrennt():
    """Liest den Ort und setzt eine vollständige Adresse zusammen."""
    daten = {
        "jobLocation": {
            "address": {
                "streetAddress": "Plazza Aviatica 6",
                "postalCode": "7503",
                "addressRegion": "Samedan",
                "addressCountry": "CH",
            }
        }
    }

    assert ort_und_adresse_aus_daten_lesen(daten) == (
        "Samedan",
        "Plazza Aviatica 6, 7503 Samedan",
    )


def test_adresse_ohne_strasse_bleibt_leer():
    """Ein bekannter Ort reicht nicht für eine vollständige Adresse."""
    daten = {
        "jobLocation": {
            "address": {
                "addressLocality": "Bern",
                "postalCode": "3000",
                "addressCountry": "CH",
            }
        }
    }

    assert ort_und_adresse_aus_daten_lesen(daten) == ("Bern", "")


def test_beschreibung_enthaelt_text_und_absatzumbrueche():
    """Entfernt HTML und behält die Trennung zwischen Absätzen."""
    daten = {"description": "<p>Wir suchen <strong>dich</strong>.</p><p>In Bern.</p>"}

    assert beschreibung_aus_daten_lesen(daten) == "Wir suchen dich.\nIn Bern."


def test_pensum_ignoriert_prozentangaben_anderer_stellen():
    """Verwendet das gekennzeichnete Feld statt beliebiger Prozentwerte."""
    html = """
        <p>Andere Stelle: 50%</p>
        <li data-cy="info-workload"><span>80 – 100%</span></li>
    """

    assert pensum_aus_html_lesen(html) == "80 – 100%"


def test_fehlendes_pensum_bleibt_leer():
    """Übernimmt keine Prozentangabe aus einer Stellenempfehlung."""
    assert pensum_aus_html_lesen("<p>Andere Stelle: 50%</p>") == ""
