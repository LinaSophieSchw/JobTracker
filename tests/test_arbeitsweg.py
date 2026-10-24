"""Prüft die Berechnung des Arbeitswegs (US 30001 und US 30002).

Wozu gibt es diese Datei?
Die Tests prüfen, dass beim Speichern einer Stelle Fahrzeit und Strecke
berechnet werden und dass ein Fehler das Speichern nicht verhindert.

Die Tests fragen nie den echten Kartendienst. Stattdessen ersetzen sie
requests.get und requests.post durch Attrappen (Mocks), die eine vorbereitete
Antwort zurückgeben. Die Antworten sind so aufgebaut wie die echten aus der
technischen Prüfung. Warum: Die Tests laufen so ohne Internet, ohne Schlüssel
und ohne das Gratis-Kontingent zu verbrauchen, und sie liefern jedes Mal
dasselbe Ergebnis.

Version 01  24.10.2026:
Tests für Adressprüfung, fehlenden Schlüssel und Speicherroute. (FH)

Version 02  24.10.2026:
Test für fehlenden Schlüssel entfernt; die Prüfung gibt es nicht mehr. (FH)

Version 03  24.10.2026:
Streckenlänge ergänzt: Test für die Umrechnung, bestehende Tests prüfen
zusätzlich die Strecke (US 30002). (FH)

Version 04  24.10.2026:
Vereinfacht: eigener Umrechnungstest entfernt; der Test der Speicherroute
prüft Umrechnung und einzige Routenabfrage mit. (FH)
"""

from unittest.mock import Mock

import requests

from app import app
from app.arbeitsweg import arbeitsweg_berechnen

WOHNADRESSE = {"strasse": "Bundesplatz 3", "postleitzahl": "3005", "ort": "Bern"}


# ==================================================
# Hilfsfunktionen: simulierte Antworten des Kartendienstes
# ==================================================
def antwort_simulieren(json_daten):
    """Baut eine Attrappe einer erfolgreichen Antwort (Statuscode 200)."""
    # Unser Code verwendet von der Antwort nur json().
    antwort = Mock()
    antwort.json.return_value = json_daten
    return antwort


def adresstreffer(layer, koordinaten):
    """Antwort der Adresssuche mit einem Treffer, aufgebaut wie die echte."""
    return antwort_simulieren(
        {
            "features": [
                {
                    "geometry": {"type": "Point", "coordinates": koordinaten},
                    "properties": {"layer": layer},
                }
            ]
        }
    )


def routenantwort(dauer_in_sekunden, strecke_in_metern):
    """Antwort der Routenberechnung, aufgebaut wie die echte."""
    return antwort_simulieren(
        {
            "routes": [
                {
                    "summary": {
                        "distance": strecke_in_metern,
                        "duration": dauer_in_sekunden,
                    }
                }
            ]
        }
    )


# ==================================================
# Requirement: Nur eine konkrete Adresse taugt für die Berechnung
# ==================================================
def test_treffer_mit_nur_einem_ort_ergibt_keine_fahrzeit(monkeypatch):
    # Wofür: Der Kartendienst findet fast immer irgendetwas. Bei «Luzern»
    # ohne Strasse liefert er nur den Ort («locality»). Damit darf nicht
    # gerechnet werden, sonst entstünde eine falsche Fahrzeit bis irgendwo
    # in die Stadtmitte.
    adresssuche = Mock(
        side_effect=[
            adresstreffer("address", [7.444185, 46.946805]),
            adresstreffer("locality", [8.303928, 47.04791]),
        ]
    )
    routenberechnung = Mock()
    monkeypatch.setattr("app.arbeitsweg.requests.get", adresssuche)
    monkeypatch.setattr("app.arbeitsweg.requests.post", routenberechnung)

    nur_ort = {"strasse": None, "postleitzahl": None, "ort": "Luzern"}
    arbeitsweg = arbeitsweg_berechnen(WOHNADRESSE, nur_ort, "testschluessel")

    assert arbeitsweg == {
        "fahrzeit_auto_in_minuten": None,
        "strecke_auto_in_metern": None,
    }
    # Ohne konkretes Ziel wird gar keine Route abgefragt.
    routenberechnung.assert_not_called()


# ==================================================
# Requirement: Der Klick auf «Speichern» liefert den Arbeitsweg mit
# ==================================================
def speicherroute_vorbereiten(monkeypatch):
    """Ersetzt die Datenbankfunktionen der Speicherroute durch Attrappen.

    Gibt die Attrappe von arbeitsweg_speichern() zurück, damit der Test
    prüfen kann, was in die Datenbank geschrieben würde.
    """
    monkeypatch.setitem(app.config, "DATABASE", "testdatenbank")
    monkeypatch.setitem(app.config, "OPENROUTESERVICE_API_KEY", "testschluessel")
    # Die Stelle bekommt die id 42, der Demo-Benutzer wohnt am Bundesplatz.
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        Mock(return_value=42),
    )
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.wohnadresse_lesen",
        Mock(return_value=WOHNADRESSE),
    )
    arbeitsweg_speichern_mock = Mock()
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.arbeitsweg_speichern",
        arbeitsweg_speichern_mock,
    )
    return arbeitsweg_speichern_mock


FORMULAR_ZUG = {
    "url": "testlink",
    "titel": "Pilot",
    "firma": "Rega",
    "inseratadresse_strasse": "Bahnhofstrasse 12",
    "inseratadresse_postleitzahl": "6300",
    "inseratadresse_ort": "Zug",
}


def test_speicherroute_liefert_und_speichert_den_arbeitsweg(monkeypatch):
    # Wofür: Das ist der ganze Ablauf der Stories in einem Test. Ein Klick auf
    # «Speichern» schickt die Formularangaben an die Route. Sie sucht beide
    # Adressen, fragt die Route ab, rechnet Fahrzeit und Strecke um, trägt
    # beide bei Stelle 42 ein und schickt sie dem Browser zurück.
    # Die Werte sind die echten Bern–Zug aus der technischen Prüfung:
    # 5682 s → 95 Minuten, 138267.6 m → 138268 Meter.
    arbeitsweg_speichern_mock = speicherroute_vorbereiten(monkeypatch)
    # side_effect gibt bei jedem Aufruf die nächste Antwort aus der Liste:
    # zuerst Bern (Wohnadresse), dann Zug (Arbeitsadresse).
    monkeypatch.setattr(
        "app.arbeitsweg.requests.get",
        Mock(
            side_effect=[
                adresstreffer("address", [7.444185, 46.946805]),
                adresstreffer("address", [8.515899, 47.168894]),
            ]
        ),
    )
    routenberechnung = Mock(return_value=routenantwort(5682.0, 138267.6))
    monkeypatch.setattr("app.arbeitsweg.requests.post", routenberechnung)

    antwort = app.test_client().post("/api/stellenanzeigen", json=FORMULAR_ZUG)

    assert antwort.status_code == 201
    assert antwort.get_json() == {
        "id": 42,
        "fahrzeit_auto_in_minuten": 95,
        "strecke_auto_in_metern": 138268,
    }
    arbeitsweg_speichern_mock.assert_called_once_with(
        "testdatenbank",
        42,
        {"fahrzeit_auto_in_minuten": 95, "strecke_auto_in_metern": 138268},
    )
    # Fahrzeit und Strecke kommen aus einer einzigen Routenabfrage (US 30002:
    # keine zusätzliche Anfrage nur für die Strecke).
    routenberechnung.assert_called_once()


def test_gescheiterte_berechnung_verhindert_das_speichern_nicht(monkeypatch):
    # Wofür: Die Story verlangt, dass eine Stelle auch dann gespeichert
    # bleibt, wenn der Arbeitsweg nicht berechnet werden kann. Hier antwortet
    # der Kartendienst nicht rechtzeitig (Zeitlimit). Die Route muss trotzdem
    # 201 melden, Fahrzeit und Strecke leer lassen und das Frontend mit null
    # informieren, damit es «Arbeitsweg konnte nicht berechnet werden.» zeigt.
    arbeitsweg_speichern_mock = speicherroute_vorbereiten(monkeypatch)
    monkeypatch.setattr(
        "app.arbeitsweg.requests.get",
        Mock(side_effect=requests.Timeout("Zeitlimit überschritten")),
    )

    antwort = app.test_client().post("/api/stellenanzeigen", json=FORMULAR_ZUG)

    assert antwort.status_code == 201
    assert antwort.get_json() == {
        "id": 42,
        "fahrzeit_auto_in_minuten": None,
        "strecke_auto_in_metern": None,
    }
    arbeitsweg_speichern_mock.assert_called_once_with(
        "testdatenbank",
        42,
        {"fahrzeit_auto_in_minuten": None, "strecke_auto_in_metern": None},
    )
