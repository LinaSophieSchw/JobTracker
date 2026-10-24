"""Berechnet den Arbeitsweg mit OpenRouteService (Use Case 3).

Wozu gibt es diese Datei?
Wir wollen wissen, wie lange man mit dem Auto von der Wohnung zur Arbeit
fährt. Das rechnet ein Kartendienst im Internet für uns aus: OpenRouteService.
Der Kartendienst rechnet aber nicht mit Adressen, sondern mit Punkten auf der
Karte (Koordinaten). Deshalb arbeitet diese Datei in zwei Teilen:

    Wohnadresse     → koordinaten_suchen() → Punkt A ┐
                                                      ├→ Fahrzeit → 95 Minuten
    Arbeitsadresse  → koordinaten_suchen() → Punkt B ┘

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

    # 2. Antwort prüfen: Hat der Dienst normal geantwortet?
    #    Wenn nicht, z. B. weil der Schlüssel falsch ist (Statuscode 403),
    #    bricht die Funktion hier ab.
    antwort.raise_for_status()

    # 3. Den besten Treffer nehmen: den ersten in der Liste «features».
    #    Gibt es keinen, bricht [0] mit einem Fehler ab.
    treffer = antwort.json()["features"][0]

    # 4. Prüfen, ob der Treffer eine echte Adresse ist.
    #    Der Kartendienst findet fast immer irgendetwas und schreibt im Feld
    #    «layer» dazu, was es ist: «address» ist eine Adresse mit Hausnummer,
    #    «locality» z. B. nur ein Ort, «country» nur das Land.
    #    Warum es das braucht: Wer nur «Luzern» eingibt, bekäme sonst eine
    #    Fahrzeit bis irgendwo in die Stadtmitte. Diese Zahl wäre falsch.
    if treffer["properties"]["layer"] != "address":
        raise ValueError("Keine konkrete Adresse gefunden.")

    # 5. Den Punkt auf der Karte zurückgeben, also die zwei Zahlen.
    #    Stolperfalle: zuerst der Längengrad (Ost-West), dann der Breitengrad
    #    (Nord-Süd). Bei Google Maps ist es umgekehrt.
    return treffer["geometry"]["coordinates"]


# ==================================================
# Teil 2: Fahrzeit von Punkt A nach Punkt B abfragen
# Beispiel: Bern → Zug = 5682 Sekunden
# ==================================================
def fahrzeit_in_sekunden_abfragen(start, ziel, api_schluessel):
    """Fragt die Autofahrzeit vom Start zum Ziel in Sekunden ab.

    start und ziel sind Punkte auf der Karte [Längengrad, Breitengrad].
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

    # 2. Antwort prüfen, wie bei der Adresssuche.
    #    Liegt ein Punkt z. B. mitten im See, findet der Dienst keine Strasse
    #    (Statuscode 404), und die Funktion bricht ab.
    antwort.raise_for_status()

    # 3. Die Fahrzeit aus der Antwort holen, z. B. 5682.0.
    #    Sie ist in Sekunden; das hat die technische Prüfung bestätigt.
    return antwort.json()["routes"][0]["summary"]["duration"]


# ==================================================
# Hauptfunktion: setzt Teil 1 und Teil 2 zusammen
# Die Speicherroute ruft nur diese eine Funktion auf.
# ==================================================
def fahrzeit_berechnen(wohnadresse, arbeitsadresse, api_schluessel):
    """Berechnet die Autofahrzeit von der Wohn- zur Arbeitsadresse in Minuten.

    Beide Adressen sind Dictionaries mit «strasse», «postleitzahl» und «ort».
    Gibt None («keine Fahrzeit») zurück, wenn die Berechnung scheitert.
    """
    # 1. try heisst: «Versuch Folgendes.» Darin die drei Arbeitsschritte:
    try:
        # Wohnadresse → Punkt A (Teil 1)
        start = koordinaten_suchen(wohnadresse, api_schluessel)
        # Arbeitsadresse → Punkt B (Teil 1)
        ziel = koordinaten_suchen(arbeitsadresse, api_schluessel)
        # Fahrzeit von A nach B in Sekunden (Teil 2)
        sekunden = fahrzeit_in_sekunden_abfragen(start, ziel, api_schluessel)

    # 2. except fängt jeden Fehler auf, statt dass die App abstürzt: kein
    #    Internet, Zeitlimit, falscher oder fehlender Schlüssel, keine echte
    #    Adresse, keine Wohnadresse, unerwartete Antwort.
    #    Warum alle gleich: Die Story verlangt in jedem Fall dieselbe Meldung
    #    ohne technische Details. Deshalb geben wir einfach None zurück.
    #    None ist Pythons Wort für «nichts, leer». In der Datenbank wird daraus
    #    ein leeres Feld, und das Frontend zeigt «Arbeitsweg konnte nicht
    #    berechnet werden.».
    except Exception:
        return None

    # 3. Hat alles geklappt: Sekunden in ganze Minuten umrechnen und
    #    zurückgeben. 5682 Sekunden sind 94,7 Minuten → 95.
    #    Ganze Minuten, weil die Datenbankspalte nur ganze Zahlen speichert.
    return round(sekunden / 60)
