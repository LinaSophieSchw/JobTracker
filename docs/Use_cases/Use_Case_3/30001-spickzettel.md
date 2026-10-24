# Spickzettel US 30001 – Fahrzeit beim ersten Speichern

Stand: 2026-10-24 · Umgesetzt von Fabio · Story: [US 30001](30001-fahrzeit-beim-ersten-speichern.md)

Vorbereitung für die Präsentation. Hier steht **der ganze Code dieser Story**
mit Erklärung, in der Reihenfolge, in der er beim Klick auf «Speichern»
abläuft. Man muss also nicht durch die Dateien klicken.

In den Codeblöcken fehlen die Kommentare und Docstrings; im Code stehen sie.
Wo nur ein Teil einer Funktion neu ist, markiert `# ← neu` die neuen Zeilen.

## Wozu gibt es diese Story?

Beim Speichern einer Stelle sieht der Nutzer sofort, wie lange er mit dem Auto
von seiner Wohnung zur Arbeit fährt:

```
Stellenanzeige gespeichert (ID: 4). Fahrzeit mit dem Auto: 95 Minuten
```

Die Fahrzeit rechnet ein Kartendienst im Internet aus: OpenRouteService
([ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md)). Er
rechnet nicht mit Adressen, sondern mit Punkten auf der Karte. Deshalb gibt es
zwei Teile: Adresse → Punkt, dann Punkt A → Punkt B → Fahrzeit.

## Der Ablauf auf einen Blick

```
Browser   Klick «Speichern» → fetch POST /api/stellenanzeigen      (Linas Code)
   │
Backend   stellenanzeige_anlegen()                   Abschnitt 1
   │        ├─ stellenanzeige_speichern()  → id 42    (Linas Code)
   │        └─ arbeitsweg_eintragen(42, daten)       Abschnitt 3
   │             ├─ wohnadresse_lesen()               Abschnitt 5
   │             ├─ fahrzeit_berechnen()              Abschnitt 6
   │             │    ├─ koordinaten_suchen() ×2      Abschnitt 7  → OpenRouteService
   │             │    └─ fahrzeit_in_sekunden_abfragen()  Abschnitt 8  → OpenRouteService
   │             └─ fahrzeit_speichern(42, 95)        Abschnitt 9  → Datenbank
   │
Browser   {"id": 42, "fahrzeit_auto_in_minuten": 95} → Meldung    Abschnitt 10
```

| Datei | Was von dieser Story drin ist |
|---|---|
| `src/app/stellenanzeigen_routes.py` | 2 Imports, `arbeitsweg_eintragen()`, 2 neue Stellen in Linas Route |
| `src/app/__init__.py` | 1 Zeile: Schlüssel laden |
| `src/app/arbeitsweg.py` | ganze Datei, neu |
| `src/app/datenbank.py` | `fahrzeit_speichern()`, dazu `wohnadresse_lesen()` aus US 30004 |
| `public/index.html` | 1 `if`/`else` in Linas Speichermethode |
| `tests/test_arbeitsweg.py` | ganze Datei, neu |
| `tests/test_stellenanzeige_speichern.py` | 1 angepasster Test von Lina |

---

## 1. Die Speicherroute: zuerst speichern, dann Arbeitsweg

[`src/app/stellenanzeigen_routes.py`, Zeilen 101–139](../../../src/app/stellenanzeigen_routes.py#L101-L139)

**Wozu:** Hier kommt der Klick auf «Speichern» an. Linas Route speichert die
Stelle; neu ist, dass danach der Arbeitsweg berechnet und mitgeschickt wird.

```python
@stellenanzeigen.post("/api/stellenanzeigen")
def stellenanzeige_anlegen():
    daten = request.get_json(silent=True)

    try:
        neue_id = stellenanzeige_speichern(
            current_app.config["DATABASE"],
            daten,
        )
    except ValueError as fehler:
        return jsonify({"fehler": str(fehler)}), 400
    except psycopg.Error:
        return (
            jsonify(
                {
                    "fehler": "Speichern derzeit nicht möglich. "
                    "Bitte später erneut versuchen."
                }
            ),
            503,
        )

    fahrzeit_in_minuten = arbeitsweg_eintragen(neue_id, daten)  # ← neu

    return (
        jsonify({"id": neue_id, "fahrzeit_auto_in_minuten": fahrzeit_in_minuten}),  # ← neu
        201,
    )
```

**Der Reihe nach:**
1. `daten = request.get_json(...)` → nimmt die Formularangaben aus dem Browser
   entgegen (Linas Teil).
2. `neue_id = stellenanzeige_speichern(...)` → **speichert die Stelle** und
   liefert ihre `id`, z. B. 42 (Linas Teil). Bei einem Eingabefehler (400) oder
   einem Datenbankfehler (503) bricht die Route hier ab, und der Kartendienst
   wird gar nicht erst gefragt.
3. `fahrzeit_in_minuten = arbeitsweg_eintragen(neue_id, daten)` → **neu:**
   erledigt den ganzen Arbeitsweg-Teil (Abschnitt 3). Ergebnis: z. B. `95`
   oder `None`.
4. `return jsonify({...}), 201` → **neu:** antwortet dem Browser mit `id`
   **und** Fahrzeit. Immer 201 («erstellt»), weil die Stelle gespeichert ist.
   `None` wird in JSON zu `null`.

*Warum zuerst speichern, dann rechnen:* Die Stelle ist so sicher gespeichert,
auch wenn die Berechnung scheitert. Linas Speicherfunktion musste nicht
geändert werden.

## 2. Imports in der Routen-Datei

[`src/app/stellenanzeigen_routes.py`, Zeilen 19–20](../../../src/app/stellenanzeigen_routes.py#L19-L20)

```python
from .arbeitsweg import fahrzeit_berechnen
from .datenbank import fahrzeit_speichern, stellenanzeige_speichern, wohnadresse_lesen
```

1. `from .arbeitsweg import fahrzeit_berechnen` → **neu:** holt die
   Hauptfunktion aus `arbeitsweg.py`. Der Punkt heisst «aus demselben Ordner».
2. `from .datenbank import ...` → `fahrzeit_speichern` und `wohnadresse_lesen`
   sind **neu** dazugekommen, `stellenanzeige_speichern` war schon da.

## 3. Arbeitsweg-Teil: lesen, berechnen, eintragen

[`src/app/stellenanzeigen_routes.py`, Zeilen 65–95](../../../src/app/stellenanzeigen_routes.py#L65-L95) · ganz neu

**Wozu:** Bündelt alles, was nach dem Speichern für den Arbeitsweg passiert.
So bleibt Linas Route kurz.

```python
def arbeitsweg_eintragen(stellen_id, daten):
    datenbank_url = current_app.config["DATABASE"]

    arbeitsadresse = {
        "strasse": daten.get("inseratadresse_strasse"),
        "postleitzahl": daten.get("inseratadresse_postleitzahl"),
        "ort": daten.get("inseratadresse_ort"),
    }

    wohnadresse = wohnadresse_lesen(datenbank_url)

    fahrzeit_in_minuten = fahrzeit_berechnen(
        wohnadresse,
        arbeitsadresse,
        current_app.config["OPENROUTESERVICE_API_KEY"],
    )

    fahrzeit_speichern(datenbank_url, stellen_id, fahrzeit_in_minuten)

    return fahrzeit_in_minuten
```

**Der Reihe nach:**
1. `datenbank_url = current_app.config["DATABASE"]` → holt die Adresse der
   Datenbank aus den Einstellungen der App.
2. `arbeitsadresse = {...}` → **stellt die Arbeitsadresse aus dem Formular
   zusammen**, in derselben Form wie die Wohnadresse (`strasse`,
   `postleitzahl`, `ort`). `daten.get(...)` liefert `None`, falls ein Feld
   fehlt. *Warum:* `fahrzeit_berechnen()` kann so beide Adressen gleich
   behandeln.
3. `wohnadresse = wohnadresse_lesen(datenbank_url)` → **holt die Wohnadresse**
   des Demo-Benutzers aus der Datenbank (Abschnitt 5).
4. `fahrzeit_in_minuten = fahrzeit_berechnen(...)` → **berechnet die
   Fahrzeit** (Abschnitt 6). Den Schlüssel holt sie aus den Einstellungen
   (Abschnitt 4).
5. `fahrzeit_speichern(datenbank_url, stellen_id, fahrzeit_in_minuten)` →
   **trägt das Ergebnis bei der Stelle ein** (Abschnitt 9). Bei `None` bleibt
   das Feld leer.
6. `return fahrzeit_in_minuten` → gibt die Minuten an die Route zurück.

## 4. Den Schlüssel beim Start laden

[`src/app/__init__.py`, Zeile 55](../../../src/app/__init__.py#L55) · neu

```python
app.config["OPENROUTESERVICE_API_KEY"] = os.getenv("OPENROUTESERVICE_API_KEY")
```

1. `os.getenv("OPENROUTESERVICE_API_KEY")` → **liest den Schlüssel** aus den
   Umgebungsvariablen: lokal aus der `.env`, online aus den
   Vercel-Einstellungen. Fehlt er, kommt `None`.
2. `app.config[...] = ...` → **legt ihn in die Einstellungen der App**, wo
   `arbeitsweg_eintragen()` ihn abholt. Gleich wie Lina es mit `DATABASE_URL`
   macht.

*Warum:* Der Schlüssel ist geheim. Er steht nie im Code und nie in Git
(`.env` ist in `.gitignore`).

## 5. Wohnadresse lesen (aus US 30004)

[`src/app/datenbank.py`, Zeilen 137–163](../../../src/app/datenbank.py#L137-L163) · schon mit US 30004 gebaut

```python
def wohnadresse_lesen(datenbank_url):
    with verbindung_oeffnen(datenbank_url) as verbindung:
        ergebnis = verbindung.execute(
            """
            SELECT wohnadresse_strasse, wohnadresse_postleitzahl, wohnadresse_ort
            FROM benutzer
            WHERE id = %s
            """,
            (aktuelle_benutzer_id(),),
        ).fetchone()

    if ergebnis is None:
        return None

    return {
        "strasse": ergebnis[0],
        "postleitzahl": ergebnis[1],
        "ort": ergebnis[2],
    }
```

1. `SELECT ... FROM benutzer WHERE id = %s` → holt die drei Adressteile des
   Demo-Benutzers (id 1).
2. `if ergebnis is None: return None` → gibt es keinen Benutzer, kommt `None`.
3. `return {...}` → packt die Zeile in ein Dictionary:
   `{"strasse": "Bundesplatz 3", "postleitzahl": "3005", "ort": "Bern"}`.

Details im [Spickzettel 30004](30004-spickzettel.md).

## 6. Fahrzeit berechnen: die Hauptfunktion

[`src/app/arbeitsweg.py`, Zeilen 140–169](../../../src/app/arbeitsweg.py#L140-L169) · neu

**Wozu:** Setzt die Teile zusammen: zwei Adressen rein, Minuten oder `None`
raus. Die Route ruft nur diese eine Funktion auf.

```python
def fahrzeit_berechnen(wohnadresse, arbeitsadresse, api_schluessel):
    try:
        start = koordinaten_suchen(wohnadresse, api_schluessel)
        ziel = koordinaten_suchen(arbeitsadresse, api_schluessel)
        sekunden = fahrzeit_in_sekunden_abfragen(start, ziel, api_schluessel)

    except Exception:
        return None

    return round(sekunden / 60)
```

**Der Reihe nach:**
1. `try:` → «Versuch Folgendes»:
   - `start = koordinaten_suchen(wohnadresse, ...)` → Wohnadresse → Punkt A
     (Abschnitt 7).
   - `ziel = koordinaten_suchen(arbeitsadresse, ...)` → Arbeitsadresse →
     Punkt B.
   - `sekunden = fahrzeit_in_sekunden_abfragen(start, ziel, ...)` → Fahrzeit
     von A nach B in Sekunden (Abschnitt 8).
2. `except Exception: return None` → **fängt jeden Fehler auf**: kein
   Internet, Zeitlimit, falscher oder fehlender Schlüssel, keine echte
   Adresse, keine Wohnadresse. Statt abzustürzen, kommt `None` («keine
   Fahrzeit») zurück. *Warum alle gleich:* Die Story verlangt in jedem Fall
   dieselbe Meldung ohne technische Details.
3. `return round(sekunden / 60)` → **Sekunden in ganze Minuten**: 5682 / 60 =
   94,7 → 95. *Warum ganze Minuten:* Die Datenbankspalte speichert nur ganze
   Zahlen.

**Was heisst `None`?** Pythons Wort für «nichts, leer». In der Datenbank wird
daraus ein leeres Feld, in JSON `null`.

## 7. Adresse → Punkt auf der Karte

[`src/app/arbeitsweg.py`, Zeilen 31–49 und 56–103](../../../src/app/arbeitsweg.py#L56-L103) · neu

**Wozu:** Der Kartendienst rechnet nur mit Punkten. Diese Funktion übersetzt
`Bundesplatz 3, 3005 Bern` in `[7.44, 46.95]`.

```python
import requests

ADRESSSUCHE_URL = "https://api.openrouteservice.org/geocode/search/structured"

ROUTE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

ZEITLIMIT_IN_SEKUNDEN = 5


def koordinaten_suchen(adresse, api_schluessel):
    antwort = requests.get(
        ADRESSSUCHE_URL,
        params={
            "address": adresse["strasse"],
            "postalcode": adresse["postleitzahl"],
            "locality": adresse["ort"],
            "country": "CH",
        },
        headers={"Authorization": api_schluessel},
        timeout=ZEITLIMIT_IN_SEKUNDEN,
    )

    antwort.raise_for_status()

    treffer = antwort.json()["features"][0]

    if treffer["properties"]["layer"] != "address":
        raise ValueError("Keine konkrete Adresse gefunden.")

    return treffer["geometry"]["coordinates"]
```

**Vorbereitung oben in der Datei:**
- `import requests` → Werkzeug, mit dem Python Fragen ins Internet schicken
  kann.
- `ADRESSSUCHE_URL` → Internetadresse der **strukturierten** Adresssuche
  (siehe Knackpunkt).
- `ROUTE_URL` → Internetadresse der Routenberechnung fürs Auto
  (Abschnitt 8).
- `ZEITLIMIT_IN_SEKUNDEN = 5` → höchstens 5 Sekunden auf eine Antwort warten,
  sonst hängt das Speichern.

**Der Reihe nach in `koordinaten_suchen()`:**
1. `antwort = requests.get(...)` → **fragt den Kartendienst:** «Wo liegt
   Bundesplatz 3, 3005 Bern, in der Schweiz?»
   - `params` → die Adresse, Strasse, PLZ und Ort getrennt, dazu fest
     `"country": "CH"`.
   - `headers` → unser Schlüssel als Ausweis. *Warum im Header:* URLs landen
     oft in Protokollen, Header nicht.
   - `timeout` → nach 5 Sekunden ohne Antwort abbrechen.
   - Die ganze Antwort des Dienstes wird in `antwort` gespeichert.
2. `antwort.raise_for_status()` → **prüft die Antwort:** Hat der Dienst normal
   geantwortet? Wenn nicht, z. B. 403 bei falschem Schlüssel, bricht die
   Funktion ab.
3. `treffer = antwort.json()["features"][0]` → **nimmt den besten Treffer:**
   `.json()` macht aus dem Antworttext ein Dictionary, `["features"]` ist die
   Trefferliste, `[0]` der erste Treffer. Gibt es keinen, bricht `[0]` ab.
4. `if treffer["properties"]["layer"] != "address": raise ValueError(...)` →
   **nur eine echte Adresse zählt.** Im Feld `layer` steht, was gefunden
   wurde: `address` (mit Hausnummer), `locality` (nur Ort), `country` (nur
   Land) usw. Ist es keine Adresse, bricht die Funktion ab. *Warum:* Wer nur
   «Luzern» eingibt, bekäme sonst eine Fahrzeit bis in die Stadtmitte.
5. `return treffer["geometry"]["coordinates"]` → **gibt den Punkt zurück**,
   z. B. `[7.444185, 46.946805]`. Stolperfalle: zuerst Längengrad, dann
   Breitengrad.

**Was heisst «bricht ab»?** `raise` löst einen Fehler aus: Die Funktion hört
sofort auf. Aufgefangen wird er in `fahrzeit_berechnen()` beim `except`.

## 8. Punkt A → Punkt B → Sekunden

[`src/app/arbeitsweg.py`, Zeilen 110–133](../../../src/app/arbeitsweg.py#L110-L133) · neu

```python
def fahrzeit_in_sekunden_abfragen(start, ziel, api_schluessel):
    antwort = requests.post(
        ROUTE_URL,
        json={"coordinates": [start, ziel]},
        headers={"Authorization": api_schluessel},
        timeout=ZEITLIMIT_IN_SEKUNDEN,
    )

    antwort.raise_for_status()

    return antwort.json()["routes"][0]["summary"]["duration"]
```

**Der Reihe nach:**
1. `antwort = requests.post(ROUTE_URL, json={"coordinates": [start, ziel]}, ...)`
   → **schickt die zwei Punkte** an die Routenberechnung fürs Auto. Zwei
   Punkte heisst: einfacher Hinweg. `post` statt `get`, weil die Punkte im
   Inhalt der Anfrage mitgehen; so verlangt es der Dienst.
2. `antwort.raise_for_status()` → **prüft die Antwort**, z. B. 404, wenn ein
   Punkt mitten im See liegt und keine Strasse in der Nähe ist.
3. `return antwort.json()["routes"][0]["summary"]["duration"]` → **holt die
   Fahrzeit** aus der Antwort, in Sekunden, z. B. `5682.0`.

So sieht der Teil der echten Antwort aus, den wir lesen:

```
{"routes": [{"summary": {"distance": 138267.6, "duration": 5682.0}, ...}]}
```

## 9. Fahrzeit in die Datenbank eintragen

[`src/app/datenbank.py`, Zeilen 297–321](../../../src/app/datenbank.py#L297-L321) · neu

**Wozu:** Die Stelle ist schon gespeichert; diese Funktion trägt die Minuten
bei ihr nach. So steht die Fahrzeit dauerhaft in der Datenbank.

```python
def fahrzeit_speichern(datenbank_url, stellen_id, fahrzeit_in_minuten):
    with verbindung_oeffnen(datenbank_url) as verbindung:
        verbindung.execute(
            """
            UPDATE stellenanzeigen
            SET fahrzeit_auto_in_minuten = %s,
                geaendert_am = CURRENT_TIMESTAMP
            WHERE id = %s AND benutzer_id = %s
            """,
            (fahrzeit_in_minuten, stellen_id, aktuelle_benutzer_id()),
        )
```

**Der Reihe nach:**
1. `with verbindung_oeffnen(datenbank_url) as verbindung:` → **öffnet die
   Verbindung** zu Neon. Am Ende des `with`-Blocks wird die Änderung bestätigt
   und die Verbindung geschlossen.
2. `UPDATE stellenanzeigen` → **ändert eine bestehende Zeile**, statt eine neue
   anzulegen (das wäre `INSERT`).
3. `SET fahrzeit_auto_in_minuten = %s, geaendert_am = CURRENT_TIMESTAMP` →
   trägt die Minuten ein und setzt den Änderungszeitpunkt auf jetzt (Regel Z1
   im Datenmodell).
4. `WHERE id = %s AND benutzer_id = %s` → **nur diese eine Stelle** des
   aktuellen Benutzers (Regel B1). Ohne `WHERE` würden alle Stellen geändert.
5. `(fahrzeit_in_minuten, stellen_id, aktuelle_benutzer_id())` → die Werte für
   die drei `%s`, in derselben Reihenfolge.

**Was heisst `%s`?** Ein Platzhalter. Die Werte gehen getrennt mit und werden
nie direkt in den SQL-Text geklebt. Das schützt vor SQL-Injection.

## 10. Browser zeigt die Meldung

[`public/index.html`, Zeilen 326–338](../../../public/index.html#L326-L338) · in Linas Methode `stellenanzeige_speichern()`

```javascript
this.erfolgsmeldung =
    `Stellenanzeige gespeichert (ID: ${daten.id}).`;

if (daten.fahrzeit_auto_in_minuten === null) {                          // ← neu
    this.erfolgsmeldung += " Arbeitsweg konnte nicht berechnet werden.";  // ← neu
} else {                                                                // ← neu
    this.erfolgsmeldung +=                                              // ← neu
        ` Fahrzeit mit dem Auto: ${daten.fahrzeit_auto_in_minuten} Minuten`;  // ← neu
}                                                                       // ← neu
```

**Der Reihe nach:**
1. `this.erfolgsmeldung = ...` → Linas Bestätigung «Stellenanzeige gespeichert
   (ID: 4).»
2. `if (daten.fahrzeit_auto_in_minuten === null)` → **prüft die Antwort des
   Backends**: Ist die Fahrzeit leer?
   - ja → `+= " Arbeitsweg konnte nicht berechnet werden."` hängt den Hinweis
     an.
   - nein → `` += ` Fahrzeit mit dem Auto: ${...} Minuten` `` hängt die
     Minuten an.

`+=` heisst «hinten anhängen». `${...}` setzt einen Wert in den Text ein.
*Warum der Text im Frontend steht:* Laut Datenmodell gehören Anzeigetexte ins
Frontend; das Backend liefert nur die Zahl oder `null`.

---

## 11. Tests

[`tests/test_arbeitsweg.py`](../../../tests/test_arbeitsweg.py) · ganz neu

**Wozu:** Prüft automatisch, dass die Fahrzeit berechnet wird und dass ein
Fehler das Speichern nicht verhindert. Die Tests fragen **nie den echten
Kartendienst** und nie die echte Datenbank.

```bash
uv run pytest tests/test_arbeitsweg.py -v
```

**Was heisst `Mock` und `monkeypatch`?**
- `Mock` ist eine **Attrappe**: Sie gibt eine vorbereitete Antwort zurück und
  merkt sich, ob und womit sie aufgerufen wurde.
- `monkeypatch` **tauscht** für die Dauer eines Tests eine echte Funktion,
  z. B. `requests.get`, gegen eine Attrappe aus. Danach ist alles wie vorher.

*Warum so:* ohne Internet, ohne Schlüssel, ohne Gratis-Kontingent zu
verbrauchen, und jedes Mal dasselbe Ergebnis.

### 11a. Vorbereitung und simulierte Antworten

[Zeilen 21–62](../../../tests/test_arbeitsweg.py#L21-L62)

```python
from unittest.mock import Mock

import requests

from app import app
from app.arbeitsweg import fahrzeit_berechnen

WOHNADRESSE = {"strasse": "Bundesplatz 3", "postleitzahl": "3005", "ort": "Bern"}


def antwort_simulieren(json_daten):
    antwort = Mock()
    antwort.json.return_value = json_daten
    return antwort


def adresstreffer(layer, koordinaten):
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


def routenantwort(dauer_in_sekunden):
    return antwort_simulieren(
        {"routes": [{"summary": {"distance": 138267.6, "duration": dauer_in_sekunden}}]}
    )
```

1. `WOHNADRESSE = {...}` → die Wohnadresse, die in mehreren Tests gebraucht
   wird.
2. `antwort_simulieren(json_daten)` → baut eine **Attrappe einer Antwort**.
   Unser Code ruft darauf nur `raise_for_status()` (macht bei der Attrappe
   nichts) und `json()` (liefert `json_daten`) auf.
3. `adresstreffer("address", [7.44, 46.95])` → simuliert die **Antwort der
   Adresssuche**, gleich aufgebaut wie die echte.
4. `routenantwort(5682.0)` → simuliert die **Antwort der Routenberechnung**.

### 11b. Test: Nur ein Ort ergibt keine Fahrzeit

[Zeilen 67–87](../../../tests/test_arbeitsweg.py#L67-L87)

```python
def test_treffer_mit_nur_einem_ort_ergibt_keine_fahrzeit(monkeypatch):
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
    minuten = fahrzeit_berechnen(WOHNADRESSE, nur_ort, "testschluessel")

    assert minuten is None
    routenberechnung.assert_not_called()
```

**Wofür:** Der Kartendienst findet bei «Luzern» nur den Ort. Damit darf nicht
gerechnet werden.

1. `adresssuche = Mock(side_effect=[...])` → die Attrappe der Adresssuche
   antwortet beim **1. Aufruf** (Wohnadresse) mit `address`, beim **2. Aufruf**
   (Luzern) mit `locality`.
2. `monkeypatch.setattr(...)` → ersetzt `requests.get` und `requests.post`
   durch die Attrappen.
3. `fahrzeit_berechnen(WOHNADRESSE, nur_ort, ...)` → ruft unseren echten Code
   auf.
4. `assert minuten is None` → **prüft:** keine Fahrzeit.
5. `routenberechnung.assert_not_called()` → **prüft:** Ohne echtes Ziel wurde
   gar keine Route abgefragt.

### 11c. Vorbereitung für die Routen-Tests

[Zeilen 93–125](../../../tests/test_arbeitsweg.py#L93-L125)

```python
def speicherroute_vorbereiten(monkeypatch):
    monkeypatch.setitem(app.config, "DATABASE", "testdatenbank")
    monkeypatch.setitem(app.config, "OPENROUTESERVICE_API_KEY", "testschluessel")
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        Mock(return_value=42),
    )
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.wohnadresse_lesen",
        Mock(return_value=WOHNADRESSE),
    )
    fahrzeit_speichern_mock = Mock()
    monkeypatch.setattr(
        "app.stellenanzeigen_routes.fahrzeit_speichern",
        fahrzeit_speichern_mock,
    )
    return fahrzeit_speichern_mock


FORMULAR_ZUG = {
    "url": "testlink",
    "titel": "Pilot",
    "firma": "Rega",
    "inseratadresse_strasse": "Bahnhofstrasse 12",
    "inseratadresse_postleitzahl": "6300",
    "inseratadresse_ort": "Zug",
}
```

1. `monkeypatch.setitem(app.config, ...)` → setzt eine Test-Datenbankadresse
   und einen Test-Schlüssel.
2. `stellenanzeige_speichern` → Attrappe, liefert immer die `id` 42.
3. `wohnadresse_lesen` → Attrappe, liefert immer den Bundesplatz.
4. `fahrzeit_speichern_mock` → Attrappe, die sich merkt, was gespeichert
   **würde**. Sie wird zurückgegeben, damit der Test das prüfen kann.
5. `FORMULAR_ZUG` → die Formularangaben, wie sie der Browser schicken würde.

So wird in Neon nichts gespeichert.

### 11d. Test: Ganzer Ablauf liefert und speichert die Fahrzeit

[Zeilen 128–152](../../../tests/test_arbeitsweg.py#L128-L152)

```python
def test_speicherroute_liefert_und_speichert_die_fahrzeit(monkeypatch):
    fahrzeit_speichern_mock = speicherroute_vorbereiten(monkeypatch)
    monkeypatch.setattr(
        "app.arbeitsweg.requests.get",
        Mock(
            side_effect=[
                adresstreffer("address", [7.444185, 46.946805]),
                adresstreffer("address", [8.515899, 47.168894]),
            ]
        ),
    )
    monkeypatch.setattr(
        "app.arbeitsweg.requests.post",
        Mock(return_value=routenantwort(5682.0)),
    )

    antwort = app.test_client().post("/api/stellenanzeigen", json=FORMULAR_ZUG)

    assert antwort.status_code == 201
    assert antwort.get_json() == {"id": 42, "fahrzeit_auto_in_minuten": 95}
    fahrzeit_speichern_mock.assert_called_once_with("testdatenbank", 42, 95)
```

**Wofür:** Das ist der ganze Ablauf der Story in einem Test.

1. `speicherroute_vorbereiten(...)` → Datenbank durch Attrappen ersetzen
   (11c).
2. `requests.get` → Attrappe findet beide Adressen (Bern und Zug).
3. `requests.post` → Attrappe liefert 5682 Sekunden.
4. `app.test_client().post("/api/stellenanzeigen", ...)` → **spielt den
   Browser:** schickt das Formular an die echte Route, ohne dass ein Server
   laufen muss.
5. `assert antwort.status_code == 201` → **prüft:** gespeichert.
6. `assert antwort.get_json() == {"id": 42, "fahrzeit_auto_in_minuten": 95}` →
   **prüft:** 5682 Sekunden wurden zu 95 Minuten und mitgeschickt.
7. `fahrzeit_speichern_mock.assert_called_once_with("testdatenbank", 42, 95)`
   → **prüft:** 95 wäre bei Stelle 42 eingetragen worden.

### 11e. Test: Gescheiterte Berechnung verhindert das Speichern nicht

[Zeilen 155–171](../../../tests/test_arbeitsweg.py#L155-L171)

```python
def test_gescheiterte_berechnung_verhindert_das_speichern_nicht(monkeypatch):
    fahrzeit_speichern_mock = speicherroute_vorbereiten(monkeypatch)
    monkeypatch.setattr(
        "app.arbeitsweg.requests.get",
        Mock(side_effect=requests.Timeout("Zeitlimit überschritten")),
    )

    antwort = app.test_client().post("/api/stellenanzeigen", json=FORMULAR_ZUG)

    assert antwort.status_code == 201
    assert antwort.get_json() == {"id": 42, "fahrzeit_auto_in_minuten": None}
    fahrzeit_speichern_mock.assert_called_once_with("testdatenbank", 42, None)
```

**Wofür:** Die Story verlangt, dass die Stelle gespeichert bleibt, auch wenn
der Arbeitsweg nicht berechnet werden kann.

1. `Mock(side_effect=requests.Timeout(...))` → die Attrappe **löst einen
   Fehler aus**, als hätte der Kartendienst nicht rechtzeitig geantwortet.
2. `app.test_client().post(...)` → schickt das Formular an die Route.
3. `assert antwort.status_code == 201` → **prüft:** trotzdem gespeichert.
4. `assert ... == {"id": 42, "fahrzeit_auto_in_minuten": None}` → **prüft:**
   `null` geht an den Browser, er zeigt den Hinweis.
5. `assert_called_once_with(..., 42, None)` → **prüft:** Das Feld bleibt leer.

### 11f. Angepasster Test von Lina

[`tests/test_stellenanzeige_speichern.py`, Zeilen 81–103](../../../tests/test_stellenanzeige_speichern.py#L81-L103) · mit Lina abgesprochen

```python
def test_speicherroute_bestaetigt_neuen_eintrag(monkeypatch):
    daten = {"url": "testlink", "titel": "Pilot", "firma": "Rega"}
    speichern_mock = Mock(return_value=42)

    monkeypatch.setattr(
        "app.stellenanzeigen_routes.stellenanzeige_speichern",
        speichern_mock,
    )
    monkeypatch.setitem(app.config, "DATABASE", "testdatenbank")
    monkeypatch.setattr(                                            # ← neu
        "app.stellenanzeigen_routes.arbeitsweg_eintragen",          # ← neu
        Mock(return_value=95),                                      # ← neu
    )                                                               # ← neu

    antwort = app.test_client().post("/api/stellenanzeigen", json=daten)

    assert antwort.status_code == 201
    assert antwort.get_json() == {"id": 42, "fahrzeit_auto_in_minuten": 95}  # ← geändert
    speichern_mock.assert_called_once_with("testdatenbank", daten)
```

1. **Neu:** `monkeypatch.setattr(..., "arbeitsweg_eintragen", Mock(return_value=95))`
   → ersetzt unseren Arbeitsweg-Teil durch eine Attrappe. *Warum:* Linas Test
   prüft nur ihr Speichern; der Arbeitsweg hat eigene Tests.
2. **Geändert:** Die erwartete Antwort enthält jetzt zusätzlich
   `"fahrzeit_auto_in_minuten": 95`, weil die Route das neue Feld mitschickt.

### Gegenprobe und Prüfung von Hand

- Mit absichtlich eingebauten Fehlern (Prüfung auf `address` entfernt,
  Sekunden nicht durch 60 geteilt) wurden die Tests rot.
- Von Hand im Browser mit echtem Kartendienst und Neon: Zug → «95 Minuten»,
  nur «Luzern» → Hinweis. Die Teststellen wurden danach gelöscht.

---

## Knackpunkt

**Der Kartendienst findet fast immer irgendetwas, auch bei einer erfundenen
Adresse.** In der technischen Prüfung vom 22.10.2026 fand die Freitext-Suche
für «Gibtsnichtweg 999, 9999 Nirgendwo» die «Böschenstrasse 999, Chur», und
zwar als Adresse. Das hätte eine falsche Fahrzeit ergeben.

Gelöst mit zwei Dingen
([ADR 0011](../../decisions/0011-strukturierte-adresssuche.md)):

1. **Strukturierte Suche** (Abschnitt 7, `params`): Strasse, PLZ und Ort gehen
   getrennt an den Dienst. Für die erfundene Adresse findet er dann nur noch
   «Schweiz».
2. **Nur `layer` `address` zählt** (Abschnitt 7, Schritt 4). Bei «Luzern»
   allein kommt `locality`, also gibt es keine Fahrzeit statt einer falschen.

| Eingabe | Freitext | Strukturiert |
|---|---|---|
| Bundesplatz 3, 3005 Bern | Adresse ✅ | Adresse ✅ |
| Gibtsnichtweg 999, 9999 Nirgendwo | Adresse in Chur ❌ | nur «Schweiz» ✅ |
| Luzern | nur Ort ✅ | nur Ort ✅ |

## Mögliche Fragen der Dozierenden

**«Warum fängst du mit `except Exception` alle Fehler ab? Ist das nicht zu
breit?»** (Abschnitt 6)

Die Story verlangt bei jedem Grund dieselbe Meldung ohne technische Details:
kein Internet, falscher Schlüssel, unbrauchbare Adresse. Deshalb muss der Code
die Fehler nicht unterscheiden, und er bleibt kurz. Der Nachteil ist bewusst
in Kauf genommen: Auch ein eigener Programmierfehler würde still zu «nicht
berechenbar». Die Tests decken die wichtigen Fälle ab, damit das auffällt.

**«Was prüfen deine Tests, wenn sie gar nicht den echten Kartendienst
fragen?»** (Abschnitt 11)

Die Attrappe gibt eine Antwort zurück, die gleich aufgebaut ist wie die echte
aus der technischen Prüfung. So prüft der Test unsere Logik: die richtige
Stelle in der Antwort lesen, in Minuten umrechnen, speichern, 201 melden. Und
das ohne Internet, ohne Schlüssel und ohne Kontingent. Dass der echte Dienst
so antwortet, wurde einmal von Hand geprüft.

**Zusatzfrage: «Warum steht der API-Schlüssel nicht im Code und nicht im
Browser?»** (Abschnitte 4 und 7)

Der Schlüssel steht in der `.env` (in `.gitignore`), online in den
Vercel-Einstellungen. Nur das Backend fragt den Kartendienst, der Browser
sieht den Schlüssel nie. In der Anfrage steht er im Header, nicht in der URL,
weil URLs oft in Protokollen landen.

**Zusatzfrage: «Warum zuerst speichern und dann rechnen?»** (Abschnitt 1)

So ist die Stelle sicher gespeichert, auch wenn die Berechnung scheitert. Ein
doppelter Link fällt vorher auf, und Linas Speicherfunktion musste nicht
geändert werden.

**Zusatzfrage: «Was passiert, wenn der Kartendienst nicht antwortet?»**
(Abschnitt 7, `timeout`)

Nach 5 Sekunden ohne Antwort bricht `requests` ab. Der Fehler landet im
`except`, die Stelle ist gespeichert, und es erscheint «Arbeitsweg konnte
nicht berechnet werden.». Genau das prüft Test 11e.

## Offen

- **Anzeige beim erneuten Öffnen:** Die Fahrzeit steht dauerhaft in der
  Datenbank. Eine Ansicht zum Öffnen einer Stelle gehört zur Detailansicht von
  Use Case 2; sie muss die Spalte `fahrzeit_auto_in_minuten` nur mitlesen.
- **Online (Vercel):** `OPENROUTESERVICE_API_KEY` muss in den
  Vercel-Einstellungen eingetragen werden, sonst erscheint dort immer der
  Hinweis.
- **Selten:** Fällt die Datenbank genau zwischen Speichern und Eintragen der
  Fahrzeit aus, meldet der Browser einen Fehler, obwohl die Stelle gespeichert
  ist. Bewusst in Kauf genommen, um den Code schlank zu halten.
