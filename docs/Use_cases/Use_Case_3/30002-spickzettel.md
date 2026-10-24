# Spickzettel US 30002 – Streckenlänge ergänzen

Stand: 2026-10-24 · Umgesetzt von Fabio · Story: [US 30002](30002-streckenlaenge-ergaenzen.md)

Vorbereitung für die Präsentation. US 30002 baut direkt auf
[US 30001](30001-spickzettel.md) auf. Hier steht **nur, was sich geändert
hat**. Den Ablauf, die Adresssuche und die Wohnadresse erklärt der
Spickzettel von US 30001.

In den Codeblöcken fehlen die Kommentare und Docstrings; im Code stehen sie.
`# ← neu` markiert neue oder geänderte Zeilen.

## Wozu gibt es diese Story?

Beim Speichern einer Stelle sieht der Nutzer jetzt auch, wie weit der
Arbeitsweg ist:

```
Stellenanzeige gespeichert (ID: 4). Fahrzeit mit dem Auto: 95 Minuten, Strecke: 138.3 km
```

**Die wichtigste Idee:** Die Strecke kostet keine zusätzliche Anfrage beim
Kartendienst. Sie stand schon in der Antwort, die wir für die Fahrzeit
bekommen haben:

```json
{"routes": [{"summary": {"distance": 138267.6, "duration": 5682.0}}]}
```

Bisher haben wir nur `duration` (Sekunden) gelesen. Jetzt lesen wir auch
`distance` (Meter).

## Der Ablauf auf einen Blick

```
Browser   Klick «Speichern» → fetch POST /api/stellenanzeigen
   │
Backend   stellenanzeige_anlegen()                         Abschnitt 4
   │        ├─ stellenanzeige_speichern()  → id 42          (Linas Code)
   │        └─ arbeitsweg_eintragen(42, daten)             Abschnitt 3
   │             ├─ wohnadresse_lesen()                     (US 30004)
   │             ├─ arbeitsweg_berechnen()                  Abschnitt 2
   │             │    ├─ koordinaten_suchen() ×2            (US 30001)
   │             │    └─ route_abfragen()                   Abschnitt 1  → OpenRouteService
   │             └─ arbeitsweg_speichern(42, {...})         Abschnitt 5  → Datenbank
   │
Browser   {"id": 42, "fahrzeit_auto_in_minuten": 95,
           "strecke_auto_in_metern": 138268} → Meldung      Abschnitt 6
```

**Umbenennungen:** Weil die Funktionen jetzt mehr als die Fahrzeit liefern,
haben sie neue Namen bekommen.

| Vorher (US 30001) | Jetzt (US 30002) |
|---|---|
| `fahrzeit_in_sekunden_abfragen()` | `route_abfragen()` |
| `fahrzeit_berechnen()` | `arbeitsweg_berechnen()` |
| `fahrzeit_speichern()` | `arbeitsweg_speichern()` |

| Datei | Was sich geändert hat |
|---|---|
| `src/app/arbeitsweg.py` | `route_abfragen()` und `arbeitsweg_berechnen()` liefern beide Werte |
| `src/app/datenbank.py` | `arbeitsweg_speichern()` schreibt beide Spalten |
| `src/app/stellenanzeigen_routes.py` | Imports, `arbeitsweg_eintragen()`, Antwort der Route |
| `public/index.html` | Kilometer an die Meldung anhängen |
| `tests/test_arbeitsweg.py` | 3 angepasste Tests |
| `tests/test_stellenanzeige_speichern.py` | 1 angepasster Test von Lina |

Die Datenbank musste **nicht** geändert werden: Die Spalte
`strecke_auto_in_metern` gab es schon seit Linas Erweiterung der Datenbank.

---

## 1. Route abfragen: die ganze Zusammenfassung zurückgeben

[`src/app/arbeitsweg.py`, Zeilen 119–143](../../../src/app/arbeitsweg.py#L119-L143)

**Wozu:** Fragt den Kartendienst nach der Autoroute von A nach B. Neu gibt sie
nicht nur die Sekunden zurück, sondern die ganze Zusammenfassung mit Dauer
**und** Strecke.

```python
def route_abfragen(start, ziel, api_schluessel):              # ← neu (Name)
    antwort = requests.post(
        ROUTE_URL,
        json={"coordinates": [start, ziel]},
        headers={"Authorization": api_schluessel},
        timeout=ZEITLIMIT_IN_SEKUNDEN,
    )

    return antwort.json()["routes"][0]["summary"]              # ← neu
```

**Der Reihe nach:**
1. `requests.post(...)` → schickt die zwei Punkte an den Kartendienst, wie
   bisher.
2. `return antwort.json()["routes"][0]["summary"]` → **neu:** Vorher stand am
   Schluss noch `["duration"]`. Jetzt hören wir eine Stufe früher auf und
   geben das ganze Dictionary zurück: `{"distance": 138267.6, "duration": 5682.0}`.

*Warum:* So bekommen wir beide Werte aus **einer** Anfrage. Die Story schliesst
eine zusätzliche Abfrage nur für die Strecke ausdrücklich aus.

*Kein `raise_for_status()` mehr:* Früher stand vor dem `return` noch
`antwort.raise_for_status()`, auch in `koordinaten_suchen()`. Es ist
weggefallen, weil es nichts mehr beiträgt. Meldet der Dienst einen Fehler
(falscher Schlüssel, keine Route), schickt er `{"error": ...}`. Dann fehlt
`routes` bzw. `features`, die Funktion bricht ab, und das `except` in
`arbeitsweg_berechnen()` fängt es auf. Das Ergebnis ist dasselbe.

## 2. Hauptfunktion: beide Werte umrechnen

[`src/app/arbeitsweg.py`, Zeilen 150–188](../../../src/app/arbeitsweg.py#L150-L188)

**Wozu:** Setzt Adresssuche und Routenabfrage zusammen. Neu gibt sie ein
Dictionary mit beiden Werten zurück statt nur der Minuten.

```python
def arbeitsweg_berechnen(wohnadresse, arbeitsadresse, api_schluessel):  # ← neu (Name)
    try:
        start = koordinaten_suchen(wohnadresse, api_schluessel)
        ziel = koordinaten_suchen(arbeitsadresse, api_schluessel)
        route = route_abfragen(start, ziel, api_schluessel)             # ← neu
    except Exception:
        return {"fahrzeit_auto_in_minuten": None, "strecke_auto_in_metern": None}  # ← neu

    return {                                                            # ← neu
        "fahrzeit_auto_in_minuten": round(route["duration"] / 60),
        "strecke_auto_in_metern": round(route["distance"]),
    }
```

**Der Reihe nach:**
1. `start = ...`, `ziel = ...` → beide Adressen in Punkte übersetzen, wie
   bisher.
2. `route = route_abfragen(...)` → **neu:** holt die Zusammenfassung mit Dauer
   und Strecke (Abschnitt 1).
3. `except Exception: return {... None ...}` → **neu:** Scheitert irgendetwas,
   sind **beide** Werte `None`. Die Story verlangt, dass dann beide leer
   bleiben.
4. `return {...}` → **neu:** rechnet beide Werte in ganze Zahlen um:
   - Fahrzeit: `5682 / 60 = 94.7` → `round()` → **95** Minuten (wie bisher).
   - Strecke: `138267.6` → `round()` → **138268** Meter. Sie bleibt in Metern.

*Warum ganze Zahlen:* Die Datenbankspalten speichern nur ganze Zahlen
(`INTEGER`).

*Warum Meter und nicht Kilometer:* So ist es im Datenmodell und in
[ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md) festgelegt
(`strecke_auto_in_metern`). In der Datenbank steht der genaue Wert; in
Kilometer rechnet erst das Frontend um, nur für die Anzeige.

*Warum ein Dictionary:* Zwei Werte lassen sich nicht mit einer einzelnen Zahl
zurückgeben. Die Schlüssel heissen gleich wie die Datenbankspalten, so sieht
man sofort, welcher Wert wohin gehört.

## 3. Arbeitsweg-Teil in der Route

[`src/app/stellenanzeigen_routes.py`, Zeilen 68–100](../../../src/app/stellenanzeigen_routes.py#L68-L100)

**Wozu:** Bündelt alles, was nach dem Speichern für den Arbeitsweg passiert.
Geändert haben sich nur die Namen und dass jetzt das Dictionary
weitergereicht wird.

```python
def arbeitsweg_eintragen(stellen_id, daten):
    datenbank_url = current_app.config["DATABASE"]

    arbeitsadresse = {
        "strasse": daten.get("inseratadresse_strasse"),
        "postleitzahl": daten.get("inseratadresse_postleitzahl"),
        "ort": daten.get("inseratadresse_ort"),
    }

    wohnadresse = wohnadresse_lesen(datenbank_url)

    arbeitsweg = arbeitsweg_berechnen(                          # ← neu
        wohnadresse,
        arbeitsadresse,
        current_app.config["OPENROUTESERVICE_API_KEY"],
    )

    arbeitsweg_speichern(datenbank_url, stellen_id, arbeitsweg)  # ← neu

    return arbeitsweg                                           # ← neu
```

**Der Reihe nach:**
1. Arbeitsadresse aus dem Formular zusammenstellen und Wohnadresse aus der
   Datenbank holen, wie bisher.
2. `arbeitsweg = arbeitsweg_berechnen(...)` → **neu:** Das Ergebnis ist jetzt
   das Dictionary mit beiden Werten.
3. `arbeitsweg_speichern(...)` → **neu:** gibt das ganze Dictionary an die
   Datenbank weiter (Abschnitt 5).
4. `return arbeitsweg` → gibt es an die Route zurück.

Dazu die zwei geänderten Imports oben in der Datei
([Zeilen 22–23](../../../src/app/stellenanzeigen_routes.py#L22-L23)):

```python
from .arbeitsweg import arbeitsweg_berechnen                                     # ← neu
from .datenbank import arbeitsweg_speichern, stellenanzeige_speichern, wohnadresse_lesen  # ← neu
```

## 4. Antwort der Speicherroute

[`src/app/stellenanzeigen_routes.py`, Zeilen 135–151](../../../src/app/stellenanzeigen_routes.py#L135-L151)

**Wozu:** Schickt dem Browser die `id` der Stelle und neu beide Werte des
Arbeitswegs.

```python
    arbeitsweg = arbeitsweg_eintragen(neue_id, daten)           # ← neu

    return (
        jsonify(
            {
                "id": neue_id,
                "fahrzeit_auto_in_minuten": arbeitsweg["fahrzeit_auto_in_minuten"],  # ← neu
                "strecke_auto_in_metern": arbeitsweg["strecke_auto_in_metern"],      # ← neu
            }
        ),
        201,
    )
```

**Der Reihe nach:**
1. `arbeitsweg = arbeitsweg_eintragen(...)` → berechnet und speichert den
   Arbeitsweg (Abschnitt 3).
2. `jsonify({...})` → baut die Antwort mit drei Feldern: `id`, Fahrzeit und
   **neu** die Strecke in Metern. `None` wird in JSON zu `null`.
3. `201` → «erstellt», auch wenn der Arbeitsweg fehlt. Die Stelle ist ja
   gespeichert.

## 5. Beide Werte in der Datenbank eintragen

[`src/app/datenbank.py`, Zeilen 301–334](../../../src/app/datenbank.py#L301-L334)

**Wozu:** Trägt Fahrzeit und Strecke bei der schon gespeicherten Stelle nach.

```python
def arbeitsweg_speichern(datenbank_url, stellen_id, arbeitsweg):  # ← neu (Name)
    with verbindung_oeffnen(datenbank_url) as verbindung:
        verbindung.execute(
            """
            UPDATE stellenanzeigen
            SET fahrzeit_auto_in_minuten = %s,
                strecke_auto_in_metern = %s,                      -- ← neu
                geaendert_am = CURRENT_TIMESTAMP
            WHERE id = %s AND benutzer_id = %s
            """,
            (
                arbeitsweg["fahrzeit_auto_in_minuten"],
                arbeitsweg["strecke_auto_in_metern"],             # ← neu
                stellen_id,
                aktuelle_benutzer_id(),
            ),
        )
```

**Der Reihe nach:**
1. `with verbindung_oeffnen(...)` → Verbindung öffnen. Am Ende werden die
   Änderungen bestätigt und die Verbindung geschlossen, wie bisher.
2. `UPDATE ... SET ...` → ändert die bestehende Zeile der Stelle. **Neu** ist
   die Zeile `strecke_auto_in_metern = %s`.
3. Die Werte in der Klammer füllen die `%s` der Reihe nach: Fahrzeit,
   **Strecke**, id der Stelle, id des Benutzers.

*Warum beide in einem UPDATE:* So passen Fahrzeit und Strecke immer zusammen.
Es kann nicht passieren, dass nur einer der beiden Werte gespeichert wird.

## 6. Anzeige im Browser

[`public/index.html`, Zeilen 333–347](../../../public/index.html#L333-L347)

**Wozu:** Hängt an die Bestätigung neu auch die Kilometer an.

```javascript
if (daten.fahrzeit_auto_in_minuten === null) {
    this.erfolgsmeldung += " Arbeitsweg konnte nicht berechnet werden.";
} else {
    const strecke_in_km =                                       // ← neu
        (daten.strecke_auto_in_metern / 1000).toFixed(1);       // ← neu
    this.erfolgsmeldung +=
        ` Fahrzeit mit dem Auto: ${daten.fahrzeit_auto_in_minuten} Minuten,` +
        ` Strecke: ${strecke_in_km} km`;                         // ← neu
}
```

**Der Reihe nach:**
1. `if (... === null)` → Ist die Fahrzeit leer, ist auch die Strecke leer.
   Dann erscheint der Hinweis, wie bisher.
2. `daten.strecke_auto_in_metern / 1000` → **neu:** Meter in Kilometer:
   `138268 / 1000 = 138.268`.
3. `.toFixed(1)` → **neu:** rundet auf eine Nachkommastelle: `"138.3"`.
4. Die Meldung bekommt hinter den Minuten `, Strecke: 138.3 km`.

## 7. Tests

[`tests/test_arbeitsweg.py`](../../../tests/test_arbeitsweg.py)

| Test | Prüft |
|---|---|
| `test_treffer_mit_nur_einem_ort_ergibt_keine_fahrzeit` | angepasst: bei nur einem Ort sind **beide** Werte leer |
| `test_speicherroute_liefert_und_speichert_den_arbeitsweg` | angepasst: 5682 s → 95 Minuten, 138267.6 m → 138268 Meter, Route speichert beide Werte, schickt beide an den Browser, und es gibt nur **eine** Routenabfrage (`routenberechnung.assert_called_once()`) |
| `test_gescheiterte_berechnung_verhindert_das_speichern_nicht` | angepasst: bei Zeitlimit bleiben **beide** leer, Stelle trotzdem gespeichert (201) |

`routenantwort()` nimmt jetzt neben der Dauer auch die Strecke entgegen.

In Linas Test `test_speicherroute_bestaetigt_neuen_eintrag`
([`tests/test_stellenanzeige_speichern.py`](../../../tests/test_stellenanzeige_speichern.py))
kam das Feld `strecke_auto_in_metern` in der erwarteten Antwort dazu.

---

## Mögliche Fragen der Dozierenden

**«Warum speichert ihr Meter und zeigt Kilometer an?»**
In der Datenbank steht der genaue Wert in einer klaren Einheit (Meter, so wie
der Kartendienst ihn liefert). Kilometer mit einer Nachkommastelle sind nur
für die Anzeige gedacht. Will man später anders runden oder sortieren, hat man
den genauen Wert noch.

**«Macht ihr für die Strecke eine zweite Anfrage an den Kartendienst?»**
Nein. Die Routenantwort enthält Dauer und Strecke zusammen in `summary`. Wir
lesen einfach beide aus. Der Test der Speicherroute prüft, dass es bei einer
Berechnung genau eine Routenabfrage gibt.
