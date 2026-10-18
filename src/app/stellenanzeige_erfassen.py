"""Liest Stelleninformationen für das Backend aus einer Webseite."""

# Zerlegt den Link und liest Parameter wie jobid aus.
from urllib.parse import parse_qs, urlsplit

# Prüft, ob die Stellen-ID ein gültiges UUID-Format hat.
from uuid import UUID

# Lädt die Stellenanzeige über eine Internetanfrage.
import requests
from bs4 import BeautifulSoup


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
