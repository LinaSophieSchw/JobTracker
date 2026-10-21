"""Liest Stelleninformationen für das Backend aus einer Webseite.
18.10 Version 1.0: Die Funktion stellentitel_auslesen() wurde implementiert.
Sie prüft einen jobs.ch-Link, lädt die Anzeige herunter und gibt den Stellentitel zurück
20.10 Version 2.0: Die Funktion wir eergänzt dirhc die anderen felder"""

# Zerlegt den Link und liest Parameter wie jobid aus.
# Wandelt strukturierte Daten aus der Webseite in Python-Werte um.
import json
from urllib.parse import parse_qs, urlsplit

# Prüft, ob die Stellen-ID ein gültiges UUID-Format hat.
from uuid import UUID

# Lädt die Stellenanzeige über eine Internetanfrage.
import requests
from bs4 import BeautifulSoup


# Die Seite kann mehrere Datenblöcke enthalten.
# Wir wählen nur die Stellenanzeige mit der gesuchten ID aus,
# damit keine Angaben einer anderen Stelle übernommen werden.
# Bevorzugt einen Datenblock mit passender Stellen-ID.
# Fehlt die Kennung, muss die Seitenadresse die Zuordnung bestätigen.
def stellenanzeige_daten_finden(html, job_id):
    """Findet die strukturierten Daten zur gesuchten Stellenanzeige."""
    seite = BeautifulSoup(html, "html.parser")
    kandidaten_ohne_kennung = []
    anzahl_stellenanzeigen = 0

    for block in seite.find_all("script", type="application/ld+json"):
        try:
            daten = json.loads(block.get_text())
        except json.JSONDecodeError:
            continue

        eintraege = daten if isinstance(daten, list) else [daten]

        for eintrag in eintraege:
            if not isinstance(eintrag, dict):
                continue

            if eintrag.get("@type") != "JobPosting":
                continue

            anzahl_stellenanzeigen += 1
            kennung = eintrag.get("identifier")

            # Eine ausdrücklich passende Kennung hat Vorrang.
            if isinstance(kennung, dict) and kennung.get("value") == job_id:
                return eintrag

            # Nur fehlende Kennungen erlauben später den Ersatzweg.
            # Eine vorhandene, fremde Kennung wird nicht ignoriert.
            if kennung is None and not eintrag.get("url"):
                kandidaten_ohne_kennung.append(eintrag)

    canonical = seite.find("link", rel="canonical")
    erwarteter_link = f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"

    # Ohne Kennung nur bei genau einer Anzeige und passender Seitenadresse.
    if (
        anzahl_stellenanzeigen == 1
        and len(kandidaten_ohne_kennung) == 1
        and canonical is not None
        and canonical.get("href") == erwarteter_link
    ):
        return kandidaten_ohne_kennung[0]

    raise ValueError(
        "Für diese Stellen-ID wurden keine eindeutig zugeordneten "
        "Anzeigendaten gefunden."
    )


# HIlfunktionen
# ---------------------------------------------------------


# FIRMA
# Die Firma steht im verschachtelten Bereich hiringOrganization.
# Fehlt sie, bleibt das Feld leer und kann später ergänzt werden.
def firma_aus_daten_lesen(daten):
    """Liest den Firmennamen aus den strukturierten Anzeigendaten."""
    organisation = daten.get("hiringOrganization")

    if not isinstance(organisation, dict):
        return ""

    name = organisation.get("name")

    if not isinstance(name, str):
        return ""

    return name.strip()


# ARBEITSORT UND ADRESSE
# jobLocation kann einen Ort oder eine Liste mehrerer Orte enthalten.
# Arbeitsort ist für die Anzeige; die vollständige Adresse wird getrennt
# zurückgegeben und später beispielsweise für die Fahrzeit verwendet.
def ort_und_adresse_aus_daten_lesen(daten):
    """Liest Arbeitsorte und die erste Adresse mit einer Strassenangabe."""
    standorte = daten.get("jobLocation", [])
    if isinstance(standorte, dict):
        standorte = [standorte]

    if not isinstance(standorte, list):
        return "", "", "", ""

    arbeitsorte = []
    adresse_strasse = ""
    adresse_postleitzahl = ""
    adresse_ort = ""

    for standort in standorte:
        if not isinstance(standort, dict):
            continue

        anschrift = standort.get("address")
        if not isinstance(anschrift, dict):
            continue

        # Arbeitsort bleibt eine separate Angabe für die Anzeige.
        ort = anschrift.get("addressLocality") or anschrift.get("addressRegion")
        ort = ort.strip() if isinstance(ort, str) else ""

        if ort and ort not in arbeitsorte:
            arbeitsorte.append(ort)

        strasse = anschrift.get("streetAddress")
        strasse = strasse.strip() if isinstance(strasse, str) else ""

        # Alle Adressbestandteile stammen vom selben Standort.
        # Fehlende Angaben bleiben leer; das Format wird nicht geprüft.
        if not adresse_strasse and strasse:
            plz = anschrift.get("postalCode")
            adresse_strasse = strasse
            adresse_postleitzahl = str(plz).strip() if plz is not None else ""
            adresse_ort = ort

    return (
        ", ".join(arbeitsorte),
        adresse_strasse,
        adresse_postleitzahl,
        adresse_ort,
    )


# Stellenbeschreibung
# Die Beschreibung enthält HTML für Überschriften, Absätze und Listen.
# Wir übernehmen nur den Text und erhalten die Absatzstruktur.
def beschreibung_aus_daten_lesen(daten):
    """Wandelt die Stellenbeschreibung in reinen Text um."""
    beschreibung = daten.get("description")

    if not isinstance(beschreibung, str):
        return ""

    inhalt = BeautifulSoup(beschreibung, "html.parser")

    # Skripte und Formatierungsregeln gehören nicht zur Beschreibung.
    for element in inhalt(["script", "style"]):
        element.decompose()

    # Absatzgrenzen markieren, bevor die HTML-Tags entfernt werden.
    for element in inhalt.find_all(
        ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "br"]
    ):
        element.insert_before("\n")
        element.insert_after("\n")

    text = inhalt.get_text()

    # Entfernt leere Zeilen und überflüssige Abstände innerhalb einer Zeile.
    zeilen = [" ".join(zeile.split()) for zeile in text.splitlines()]
    return "\n".join(zeile for zeile in zeilen if zeile)


# ARBEITSsPENSUM
# Liest das ausdrücklich gekennzeichnete Pensum der Anzeige.
# Prozentangaben im Titel oder in Stellenempfehlungen bleiben unberücksichtigt.
def pensum_aus_html_lesen(html):
    """Liest das Pensum aus dem Informationsbereich der Anzeige."""
    seite = BeautifulSoup(html, "html.parser")
    pensum_element = seite.select_one('li[data-cy="info-workload"]')

    if pensum_element is None:
        return ""

    return pensum_element.get_text(" ", strip=True)


# ---------------------------------------------------------


def stellentitel_aus_html_lesen(html):
    """Gibt die erste Hauptüberschrift als Stellentitel zurück."""
    seite = BeautifulSoup(html, "html.parser")
    ueberschrift = seite.find("h1")

    if ueberschrift is None:
        raise ValueError("In der Stellenanzeige wurde kein Titel gefunden.")

    titel = ueberschrift.get_text(strip=True)

    if not titel:
        raise ValueError("Der Stellentitel ist leer.")

    return titel


# Prüft den jobs.ch-Link und liest die Stellen-ID aus dem Pfad oder
# dem Parameter jobid. Daraus entsteht ein direkter Link zur Anzeige.
def anzeigenlink_bestimmen(url):
    """Wandelt einen jobs.ch-Link in einen direkten Anzeigenlink um."""
    teile = urlsplit(url.strip())

    if teile.scheme != "https" or teile.netloc != "www.jobs.ch":
        raise ValueError("Bitte einen HTTPS-Link von www.jobs.ch eingeben.")

    if teile.path.startswith("/de/stellenangebote/detail/"):
        job_id = teile.path.removeprefix("/de/stellenangebote/detail/").strip("/")
    elif teile.path == "/de/stellenangebote/":
        parameter = parse_qs(teile.query)
        job_id = parameter.get("jobid", [""])[0]
    else:
        raise ValueError("Dieser jobs.ch-Link wird noch nicht unterstützt.")

    try:
        job_id = str(UUID(job_id))
    except ValueError:
        raise ValueError("Der Link enthält keine gültige Stellen-ID.") from None

    return f"https://www.jobs.ch/de/stellenangebote/detail/{job_id}/"


# Verbindet die bisherigen Schritte: jobs.ch-Link prüfen, Anzeige
# herunterladen und den Stellentitel aus dem HTML lesen.
# Bei einem fehlgeschlagenen Abruf wird eine verständliche Fehlermeldung
# ausgelöst. Die Funktion speichert noch nichts in der Datenbank.
def stellentitel_auslesen(url):
    """Lädt eine geprüfte jobs.ch-Anzeige und gibt ihren Titel zurück."""
    anzeigenlink = anzeigenlink_bestimmen(url)

    try:
        # Begrenzt die Wartezeit und folgt keinen Weiterleitungen.
        antwort = requests.get(
            anzeigenlink,
            timeout=15,
            allow_redirects=False,
        )
        # Löst bei HTTP-Fehlern wie 403 oder 404 eine Ausnahme aus.
        antwort.raise_for_status()
    except requests.RequestException as fehler:
        raise ValueError("Die Stellenanzeige konnte nicht geladen werden.") from fehler

    if antwort.status_code != 200:
        raise ValueError("Die Stellenanzeige ist nicht direkt erreichbar.")

    return stellentitel_aus_html_lesen(antwort.text)


# Hauptfunktion
# -------------------------------------------------------------------------


# Verbindet Linkprüfung, Abruf und die einzelnen Auslesefunktionen.
# Die Anzeige wird nur einmal heruntergeladen.
def stellenanzeige_auslesen(url):
    """Lädt eine jobs.ch-Anzeige und liefert ihre Vorschauangaben."""
    anzeigenlink = anzeigenlink_bestimmen(url)

    # Der geprüfte Anzeigenlink endet mit der Stellen-ID.
    job_id = urlsplit(anzeigenlink).path.strip("/").split("/")[-1]

    try:
        antwort = requests.get(
            anzeigenlink,
            timeout=15,
            allow_redirects=False,
        )
        antwort.raise_for_status()
    except requests.RequestException as fehler:
        raise ValueError("Die Stellenanzeige konnte nicht geladen werden.") from fehler

    if antwort.status_code != 200:
        raise ValueError("Die Stellenanzeige ist nicht direkt erreichbar.")

    daten = stellenanzeige_daten_finden(antwort.text, job_id)

    # Die Auslesefunktion liefert Arbeitsort und drei Adressbestandteile.
    (
        arbeitsort,
        inseratadresse_strasse,
        inseratadresse_postleitzahl,
        inseratadresse_ort,
    ) = ort_und_adresse_aus_daten_lesen(daten)

    # Diese Feldnamen werden auch im Frontend und in der Datenbank verwendet.
    return {
        "url": anzeigenlink,
        "titel": stellentitel_aus_html_lesen(antwort.text),
        "firma": firma_aus_daten_lesen(daten),
        "arbeitsort": arbeitsort,
        "inseratadresse_strasse": inseratadresse_strasse,
        "inseratadresse_postleitzahl": inseratadresse_postleitzahl,
        "inseratadresse_ort": inseratadresse_ort,
        "pensum": pensum_aus_html_lesen(antwort.text),
        "stellenbeschreibung": beschreibung_aus_daten_lesen(daten),
    }
