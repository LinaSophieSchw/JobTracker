"""Berechnet den Arbeitsweg mit OpenRouteService (Use Case 3).

Wozu gibt es diese Datei?
Wir wollen wissen, wie lange und wie weit man mit dem Auto von der Wohnung
zur Arbeit fährt. Das rechnet ein Kartendienst im Internet für uns aus:
OpenRouteService.
Der Kartendienst rechnet aber nicht mit Adressen, sondern mit Punkten auf der
Karte (Koordinaten). Deshalb arbeitet diese Datei in zwei Teilen:

    Wohnadresse     → koordinaten_suchen() → Punkt A ┐
                                                      ├→ route_abfragen()
    Arbeitsadresse  → koordinaten_suchen() → Punkt B ┘      → 95 Minuten
                                                              138268 Meter

Gehört zur Schicht «Backend». Der Browser spricht nie direkt mit
OpenRouteService, damit der API-Schlüssel auf dem Server bleibt.

Version 01  22.10.2026:
Adresssuche mit Koordinaten ergänzt (US 30001). (FH)

Version 02  24.10.2026:
Routenabfrage und Hauptfunktion fahrzeit_berechnen() ergänzt (US 30001). (FH)

Version 03  24.10.2026:
Erklärende Kommentare ergänzt. (FH)

Version 04  24.10.2026:
Vereinfacht: kleine Hilfsfunktionen und Testteil entfernt, ein einziges
Auffangen aller Fehler in fahrzeit_berechnen(). (FH)

Version 05  24.10.2026:
Zusätzlich die Streckenlänge aus derselben Routenantwort übernehmen
(US 30002). fahrzeit_in_sekunden_abfragen() heisst jetzt route_abfragen(),
fahrzeit_berechnen() heisst jetzt arbeitsweg_berechnen(). (FH)

Version 06  24.10.2026:
Vereinfacht: raise_for_status() entfernt. Fehlerantworten des Dienstes
enthalten weder «features» noch «routes» und landen so ohnehin im except
von arbeitsweg_berechnen(). (FH)
"""

# Werkzeug, mit dem Python Fragen ins Internet schicken kann.
import requests

# ==================================================
# Vorbereitung: Adressen und Zeitlimit
# ==================================================
# Internetadresse der Adresssuche des Kartendienstes.
# Strukturierte Suche: Strasse, Postleitzahl und Ort gehen getrennt an den
# Dienst. Die Freitext-Suche hat in der technischen Prüfung die erfundene
# Adresse «Gibtsnichtweg 999, 9999 Nirgendwo» als «Böschenstrasse 999, Chur»
# erkannt. Die strukturierte Suche findet dafür nur «Schweiz» (ADR 0011).
ADRESSSUCHE_URL = "https://api.openrouteservice.org/geocode/search/structured"

# Internetadresse der Routenberechnung fürs Auto («driving-car»).
# Ohne Live-Verkehr, so wie es die Story will.
ROUTE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

# Wir warten höchstens 5 Sekunden auf eine Antwort.
# Sonst würde der Klick auf «Speichern» im schlimmsten Fall ewig hängen.
ZEITLIMIT_IN_SEKUNDEN = 5


# ==================================================
# Teil 1: Adresse in einen Punkt auf der Karte übersetzen
# Beispiel: Bundesplatz 3, 3005 Bern → [7.44, 46.95]
# ==================================================
def koordinaten_suchen(adresse, api_schluessel):
    """Übersetzt eine Schweizer Adresse in einen Punkt auf der Karte.

    adresse ist ein Dictionary mit «strasse», «postleitzahl» und «ort»,
    so wie es wohnadresse_lesen() liefert.
    Gibt [Längengrad, Breitengrad] zurück, z. B. [7.44, 46.95].
    Klappt es nicht, bricht die Funktion mit einem Fehler ab.
    """
    # 1. Fragen: «Wo liegt Bundesplatz 3, 3005 Bern, in der Schweiz?»
    #    In params steht die Adresse, in headers unser Schlüssel als Ausweis.
    #    Die Antwort des Dienstes wird in «antwort» gespeichert.
    antwort = requests.get(
        ADRESSSUCHE_URL,
        params={
            "address": adresse["strasse"],
            "postalcode": adresse["postleitzahl"],
            "locality": adresse["ort"],
            # Die Schweiz ist fest vorgegeben, es gibt keine Länderauswahl.
            "country": "CH",
        },
        # Der Schlüssel steht im Header und nicht in der URL. URLs landen
        # oft in Protokollen und Fehlermeldungen, Header nicht.
        headers={"Authorization": api_schluessel},
        timeout=ZEITLIMIT_IN_SEKUNDEN,
    )

    # 2. Den besten Treffer nehmen: den ersten in der Liste «features».
    #    Gibt es keinen, bricht [0] mit einem Fehler ab. Meldet der Dienst
    #    einen Fehler, z. B. bei falschem Schlüssel, fehlt «features» ganz,
    #    und die Funktion bricht ebenfalls ab.
    treffer = antwort.json()["features"][0]

    # 3. Prüfen, ob der Treffer eine echte Adresse ist.
    #    Der Kartendienst findet fast immer irgendetwas und schreibt im Feld
    #    «layer» dazu, was es ist: «address» ist eine Adresse mit Hausnummer,
    #    «locality» z. B. nur ein Ort, «country» nur das Land.
    #    Warum es das braucht: Wer nur «Luzern» eingibt, bekäme sonst eine
    #    Fahrzeit bis irgendwo in die Stadtmitte. Diese Zahl wäre falsch.
    if treffer["properties"]["layer"] != "address":
        raise ValueError("Keine konkrete Adresse gefunden.")

    # 4. Den Punkt auf der Karte zurückgeben, also die zwei Zahlen.
    #    Stolperfalle: zuerst der Längengrad (Ost-West), dann der Breitengrad
    #    (Nord-Süd). Bei Google Maps ist es umgekehrt.
    return treffer["geometry"]["coordinates"]


# ==================================================
# Teil 2: Route von Punkt A nach Punkt B abfragen
# Beispiel: Bern → Zug = 5682 Sekunden und 138267.6 Meter
# ==================================================
def route_abfragen(start, ziel, api_schluessel):
    """Fragt Fahrzeit und Strecke der Autoroute vom Start zum Ziel ab.

    start und ziel sind Punkte auf der Karte [Längengrad, Breitengrad].
    Gibt die Zusammenfassung der Route zurück, z. B.
    {"duration": 5682.0, "distance": 138267.6}: Sekunden und Meter.
    """
    # 1. Die zwei Punkte an den Kartendienst schicken.
    #    Nur zwei Punkte heisst: einfacher Hinweg, kein Rückweg.
    #    post statt get, weil wir die Punkte im Inhalt der Anfrage
    #    mitschicken müssen. So verlangt es der Dienst.
    antwort = requests.post(
        ROUTE_URL,
        json={"coordinates": [start, ziel]},
        headers={"Authorization": api_schluessel},
        timeout=ZEITLIMIT_IN_SEKUNDEN,
    )

    # 2. Die Zusammenfassung der Route zurückgeben. Darin stehen beide Werte,
    #    die wir brauchen: «duration» in Sekunden und «distance» in Metern.
    #    Das hat die technische Prüfung bestätigt. Weil beide in derselben
    #    Antwort stehen, braucht die Strecke keine zusätzliche Anfrage.
    #    Findet der Dienst keine Route, z. B. weil ein Punkt mitten im See
    #    liegt, fehlt «routes», und die Funktion bricht ab.
    return antwort.json()["routes"][0]["summary"]


# ==================================================
# Hauptfunktion: setzt Teil 1 und Teil 2 zusammen
# Die Speicherroute ruft nur diese eine Funktion auf.
# ==================================================
def arbeitsweg_berechnen(wohnadresse, arbeitsadresse, api_schluessel):
    """Berechnet Fahrzeit und Strecke von der Wohn- zur Arbeitsadresse.

    Beide Adressen sind Dictionaries mit «strasse», «postleitzahl» und «ort».
    Gibt ein Dictionary zurück, z. B.
    {"fahrzeit_auto_in_minuten": 95, "strecke_auto_in_metern": 138268}.
    Scheitert die Berechnung, sind beide Werte None («leer»).
    """
    # 1. try heisst: «Versuch Folgendes.» Darin die drei Arbeitsschritte:
    try:
        # Wohnadresse → Punkt A (Teil 1)
        start = koordinaten_suchen(wohnadresse, api_schluessel)
        # Arbeitsadresse → Punkt B (Teil 1)
        ziel = koordinaten_suchen(arbeitsadresse, api_schluessel)
        # Fahrzeit und Strecke von A nach B (Teil 2)
        route = route_abfragen(start, ziel, api_schluessel)

    # 2. except fängt jeden Fehler auf, statt dass die App abstürzt: kein
    #    Internet, Zeitlimit, falscher oder fehlender Schlüssel, keine echte
    #    Adresse, keine Wohnadresse, unerwartete Antwort.
    #    Warum alle gleich: Die Story verlangt in jedem Fall dieselbe Meldung
    #    ohne technische Details. Deshalb bleiben einfach beide Werte leer.
    #    None ist Pythons Wort für «nichts, leer». In der Datenbank wird daraus
    #    ein leeres Feld, und das Frontend zeigt «Arbeitsweg konnte nicht
    #    berechnet werden.».
    except Exception:
        return {"fahrzeit_auto_in_minuten": None, "strecke_auto_in_metern": None}

    # 3. Hat alles geklappt: beide Werte auf ganze Zahlen runden, weil die
    #    Datenbankspalten nur ganze Zahlen speichern.
    #    - Fahrzeit: Sekunden in Minuten. 5682 Sekunden sind 94,7 Minuten → 95.
    #    - Strecke: bleibt in Metern. 138267.6 Meter → 138268.
    #      In Kilometer rechnet erst das Frontend um, für die Anzeige.
    #    Die Schlüssel heissen gleich wie die Datenbankspalten. So sieht man
    #    sofort, welcher Wert wohin gehört.
    return {
        "fahrzeit_auto_in_minuten": round(route["duration"] / 60),
        "strecke_auto_in_metern": round(route["distance"]),
    }
