# Code-Stil wie in den Codebeispielen

Die Codebeispiele aus dem Unterricht (Anagramm-Generator, Weihnachtsbaum,
Bankkonto, Greeter, Passwort-Prüfung) haben einen gemeinsamen Stil. Das Team
kennt ihn und kann Code in diesem Stil lesen. Deshalb schreibt der Agent
Projektcode genauso.

## Namen

- **Deutsch und sprechend**, so dass man ohne Kommentar versteht, was drin
  ist: `name_ohne_abstand`, `kontostand_in_chf`, `maximale_baum_breite`.
  Lieber lang und klar als kurz und rätselhaft (`neue_bewerbung` statt `nb`).
- **Funktionen heissen nach dem, was sie tun:** `bewerbung_speichern()`,
  `bewerbungen_nach_status_filtern()`.
- **Umlaute in Namen vermeiden** (`anzahl_bewerbungen`, `aendern`), weil sie in
  URLs, Datenbankspalten und Dateinamen Probleme machen können. In Kommentaren
  und Texten sind Umlaute natürlich in Ordnung.

## Docstrings

- **Oben in jeder Datei** ein Docstring: wofür die Datei da ist und zu welcher
  Schicht sie gehört.
- **Jede Funktion** bekommt einen Docstring mit einem Satz, was sie tut. Bei
  Parametern, die nicht offensichtlich sind, kurz, was erwartet wird.

## Kommentare erklären das Warum und den Denkweg

Die Codebeispiele kommentieren nicht jede Zeile, sondern die Stellen, an denen
man sonst stolpern würde:

- **Warum etwas so gelöst ist** – z. B. im Bankkonto, warum `überweisen()`
  die Methoden `abheben()` und `einzahlen()` wiederverwendet, statt den
  Kontostand direkt zu ändern: So gilt die Prüfung gegen Überziehen
  automatisch auch für Überweisungen.
- **Wie man auf eine Lösung kommt** – z. B. beim Weihnachtsbaum, wo die
  Formel für die Einrückung hergeleitet wird, indem man Werte für einige
  Fälle aufschreibt und das Muster sucht.
- **Stolperfallen** – z. B. dass `random.shuffle()` die Liste direkt
  verändert, `"".join()` aber einen neuen Wert zurückgibt, den man speichern
  muss.

Keine Kommentare, die nur wiederholen, was ohnehin dasteht
(`# i um 1 erhöhen`).

## Kleine Funktionen mit einer Aufgabe

Wie in der Passwort-Prüfung (`count_digits`, `count_capital_letters`, …):
Jede Funktion macht eine Sache, die Hauptfunktion setzt sie zusammen. Das
macht den Code leichter erklärbar und leichter testbar.

Logik, die man testen will (Berechnungen, Prüfungen, Filter), gehört in eigene
Funktionen und nicht direkt in die Flask-Route. Die Route nimmt nur die Daten
entgegen, ruft die Funktion auf und gibt das Ergebnis zurück.

## Beispiel: Flask-Route im Stil der Codebeispiele

```python
"""Backend für die Bewerbungen.

Gehört zum Slice «Neue Bewerbung erfassen»: Das Formular im Frontend
schickt die Daten hierher, und dieses Modul speichert sie.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Fürs Erste speichern wir die Bewerbungen nur in einer Python-Liste.
# Das reicht, um den ganzen Slice einmal vom Formular bis zurück in den
# Browser durchzuspielen. Achtung: Beim Neustart des Servers ist die
# Liste wieder leer. Im nächsten Schritt kommt die Datenbank.
bewerbungen = []


def bewerbung_erstellen(firma, stelle):
    """Erstellt eine neue Bewerbung als Dictionary mit Status «offen»."""
    # Jede neue Bewerbung startet als «offen». Den Status setzen wir
    # hier im Backend und nicht im Formular, damit niemand eine
    # Bewerbung direkt als «Zusage» erfassen kann.
    return {"firma": firma, "stelle": stelle, "status": "offen"}


@app.post("/api/bewerbungen")
def bewerbung_speichern():
    """Nimmt eine neue Bewerbung aus dem Formular entgegen und speichert sie."""
    # Das Frontend schickt die Daten als JSON. request.get_json() macht
    # daraus ein Python-Dictionary.
    daten = request.get_json()
    neue_bewerbung = bewerbung_erstellen(daten["firma"], daten["stelle"])
    bewerbungen.append(neue_bewerbung)
    # Statuscode 201 heisst «Created». So weiss das Frontend, dass
    # tatsächlich etwas gespeichert wurde.
    return jsonify(neue_bewerbung), 201
```

Das Beispiel zeigt den Stil, nicht die fertige Lösung. Der Agent passt Namen,
Felder und Ablauf an das an, was das Team gerade baut.

## Tests wie im Greeter-Beispiel

- Datei `tests/test_<modul>.py`, ausgeführt mit `uv run pytest`.
- **Testnamen sind Sätze** auf Deutsch, die das erwartete Verhalten
  beschreiben: `test_neue_bewerbung_startet_mit_status_offen`. Schlägt der
  Test fehl, sagt der Name schon, was kaputt ist.
- **Gruppiert nach Anforderungen** mit einem Kommentar
  `# Requirement 1: …`, `# Requirement 2: …`. Die Anforderungen kommen aus
  der User Story bzw. ihren Akzeptanzkriterien.
- Ein Test prüft ein Verhalten. Lieber mehrere kurze Tests als einen langen.
- Zuerst die einfachen Funktionen testen (ohne Flask), dann die Routen mit dem
  Flask-Test-Client.

```python
from app import app, bewerbung_erstellen


# Requirement 1: Eine neue Bewerbung startet mit Status «offen»
def test_neue_bewerbung_startet_mit_status_offen():
    bewerbung = bewerbung_erstellen("Migros", "Praktikum Informatik")
    assert bewerbung["status"] == "offen"


# Requirement 2: Das Formular kann eine Bewerbung speichern
def test_gespeicherte_bewerbung_wird_mit_status_201_bestaetigt():
    # Der Test-Client spielt den Browser: Er schickt einen Request an
    # unsere App, ohne dass ein echter Server laufen muss.
    client = app.test_client()
    antwort = client.post(
        "/api/bewerbungen",
        json={"firma": "Migros", "stelle": "Praktikum Informatik"},
    )
    assert antwort.status_code == 201
```

## Programm direkt ausprobieren

Wie in den Codebeispielen (`if __name__ == "__main__":` im Greeter, der
Testaufruf am Ende des Weihnachtsbaums) darf ein Modul unten einen kleinen
Aufruf haben, mit dem man eine Funktion schnell von Hand ausprobieren kann.
Für das Starten der Webapplikation selbst verwendet der Agent aber den Weg,
der im Projekt festgelegt ist (z. B. `uv run flask --app app run`), und
erklärt den Befehl.
