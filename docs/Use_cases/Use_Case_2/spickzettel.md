# Spickzettel Use Case 2 – Stellenanzeigen verwalten

Stand: 2026-11-01 · Umgesetzt von Mirko · Use Case: [README](README.md)

Vorbereitung für die Präsentation. Ein Spickzettel für alle fünf Stories von
Use Case 2, weil sie zusammen einen Kreis bilden: sehen → öffnen → ändern →
löschen. Wer ihn gelesen hat, kann jeden Klick vom Browser bis zur Datenbank
und zurück erklären.

In den Codeblöcken fehlen die Kommentare; im Code stehen sie. Zeilenangaben
gelten für den Stand vom 01.11.2026.

## Wozu gibt es Use Case 2?

Use Case 1 legt Stellen an, Use Case 3 berechnet den Arbeitsweg. Use Case 2
sorgt dafür, dass man mit den gespeicherten Stellen **arbeiten** kann:

| Story | Was der Nutzer tut | HTTP-Anfrage | SQL |
|---|---|---|---|
| [US 20001](20001-uebersicht-aller-stellen.md) | Übersicht sehen | `GET /api/stellenanzeigen` | `SELECT` alle |
| [US 20002](20002-stelle-oeffnen.md) | Zeile anklicken, Stelle öffnen | `GET /api/stellenanzeigen/<id>` | `SELECT` eine |
| [US 20003](20003-status-aendern.md) | Status ändern | `PUT /api/stellenanzeigen/<id>` | `UPDATE` |
| [US 20004](20004-angaben-bearbeiten.md) | alle Angaben ändern | derselbe `PUT`, erweitert | `UPDATE` |
| [US 20005](20005-stelle-loeschen.md) | Stelle löschen | `DELETE /api/stellenanzeigen/<id>` | `DELETE` |

**Die wichtigste Idee:** Alle vier Routen verwenden **dieselbe Adresse**.
Flask unterscheidet sie an der **HTTP-Methode**: GET liest, PUT ändert,
DELETE löscht. Das ist das Muster «REST»: Die Adresse sagt *welche* Stelle,
die Methode sagt *was* mit ihr passiert.

## Drei Sprachen, drei Schichten

```
Browser (Vue)        ── HTTP: GET / PUT / DELETE ──▶   Flask (Python)   ── SQL ──▶   PostgreSQL
public/index.html         fetch(...)                   stellenanzeigen_       datenbank.py      (Neon)
                                                       routes.py
```

| Begriff | Was es ist |
|---|---|
| `fetch` | JavaScript-Funktion im Browser, die eine Anfrage an den Server schickt |
| `body` | Daten, die eine Anfrage mitbringt (bei uns JSON); GET und DELETE brauchen keinen |
| GET, POST, PUT, DELETE | HTTP-Methoden: lesen, neu anlegen, ersetzen, löschen |
| Route | Python-Funktion, die Flask bei einer bestimmten Adresse + Methode aufruft |
| SQL | Sprache, mit der Python die Datenbank fragt: `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| `%s` | Platzhalter im SQL; der Wert geht getrennt mit (Schutz vor SQL-Injection) |
| PostgreSQL | die Datenbank-Software; Neon betreibt sie für uns in der Cloud |

## Der Ablauf auf einen Blick

```
Seite öffnen    mounted() → stellen_laden() → GET /api/stellenanzeigen
                  → stellenanzeigen_auflisten() → stellenanzeigen_lesen()      Abschnitt 1

Zeile klicken   stelle_oeffnen(id) → GET /api/stellenanzeigen/7
                  → stellenanzeige_oeffnen() → stellenanzeige_mit_id_lesen()   Abschnitt 2

«Speichern»     stelle_aktualisieren() → PUT /api/stellenanzeigen/7
                  → stellenanzeige_aendern()
                      ├─ stellenanzeige_aktualisieren()                         Abschnitt 3
                      ├─ stellenanzeige_mit_id_lesen()
                      └─ arbeitsweg_eintragen()          (Use Case 3, Fabio)

«Löschen»       stelle_loeschen() → confirm() → DELETE /api/stellenanzeigen/7
                  → stellenanzeige_entfernen() → stellenanzeige_loeschen()      Abschnitt 4
                  → zur_uebersicht()
```

| Datei | Was Use Case 2 dort gebaut hat |
|---|---|
| `src/app/datenbank.py` | `stellenanzeigen_lesen()`, `stellenanzeige_mit_id_lesen()`, `stellenfelder_pruefen()`, `stellenanzeige_aktualisieren()`, `stellenanzeige_loeschen()`, Konstante `ERLAUBTE_STATUS` |
| `src/app/stellenanzeigen_routes.py` | vier Routen: auflisten, öffnen, ändern, entfernen |
| `public/index.html` | Übersicht als Startseite, Umschalten Übersicht ↔ Formular, Zustand «Bestehend», Status-Dropdown, «Löschen» |
| `tests/` | 4 Testdateien mit 34 Tests (Abschnitt 5) |

---

## 1. Übersicht aller Stellen (US 20001)

### Datenbank

[`src/app/datenbank.py`, ab Zeile 354](../../../src/app/datenbank.py#L354)

```python
def stellenanzeigen_lesen(datenbank_url):
    with verbindung_oeffnen(datenbank_url) as verbindung:
        zeilen = verbindung.execute(
            """
            SELECT id, titel, firma, arbeitsort, status,
                   strecke_auto_in_metern, fahrzeit_auto_in_minuten
            FROM stellenanzeigen
            WHERE benutzer_id = %s
            ORDER BY erstellt_am DESC
            """,
            (aktuelle_benutzer_id(),),
        ).fetchall()

    stellen = []
    for zeile in zeilen:
        stellen.append({"id": zeile[0], "titel": zeile[1], ...})
    return stellen
```

- **Nur die Spalten der Übersicht**, ohne die lange Stellenbeschreibung. Das
  spart Daten, die niemand anschaut.
- `WHERE benutzer_id = %s`: nur Stellen des Demo-Benutzers (Regel B1).
- `ORDER BY erstellt_am DESC`: neueste zuerst. `DESC` heisst absteigend.
- `fetchall()` liefert alle Zeilen als Tupel. Die Schleife macht daraus
  Dictionaries mit Namen, damit das Frontend `stelle.titel` statt `zeile[1]`
  schreiben kann.

### Route

[`src/app/stellenanzeigen_routes.py`, ab Zeile 183](../../../src/app/stellenanzeigen_routes.py#L183)

```python
@stellenanzeigen.get("/api/stellenanzeigen")
def stellenanzeigen_auflisten():
    try:
        stellen = stellenanzeigen_lesen(current_app.config["DATABASE"])
    except psycopg.Error:
        return jsonify({"fehler": "Übersicht derzeit nicht verfügbar."}), 503
    return jsonify(stellen)
```

Dieselbe Adresse wie das Anlegen aus Use Case 1 (`POST`). Flask
unterscheidet an der Methode.

### Frontend

[`public/index.html`, Tabelle ab Zeile 86, `stellen_laden()` ab Zeile 390](../../../public/index.html#L86)

```html
<tr v-for="stelle in stellen" :key="stelle.id" @click="stelle_oeffnen(stelle.id)">
    <td>{{ stelle.titel }}</td>
    ...
    <td>{{ status_anzeigen(stelle.status) }}</td>
    <td>{{ arbeitsweg_anzeigen(stelle) }}</td>
</tr>
```

```js
async stellen_laden() {
    const antwort = await fetch("/api/stellenanzeigen");
    const daten = await antwort.json();
    ...
    this.stellen = daten;
}
```

- `v-for` wiederholt die Zeile für jede Stelle; `:key` hilft Vue, die
  Zeilen auseinanderzuhalten.
- `status_anzeigen()` übersetzt den gespeicherten Wert in den Anzeigetext,
  z. B. `interview` → «Vorstellungsgespräch» (Konstante `STATUS_ANZEIGE`,
  Zeile 319).
- `mounted()` ruft `stellen_laden()` beim Öffnen der Seite auf; darum ist die
  Übersicht die Startseite.

---

## 2. Stelle öffnen (US 20002)

### Datenbank

[`src/app/datenbank.py`, ab Zeile 403](../../../src/app/datenbank.py#L403)

```python
def stellenanzeige_mit_id_lesen(datenbank_url, stellen_id):
    with verbindung_oeffnen(datenbank_url) as verbindung:
        zeile = verbindung.execute(
            """
            SELECT id, url, titel, ..., status,
                   strecke_auto_in_metern, fahrzeit_auto_in_minuten
            FROM stellenanzeigen
            WHERE id = %s AND benutzer_id = %s
            """,
            (stellen_id, aktuelle_benutzer_id()),
        ).fetchone()

    if zeile is None:
        return None
    return {"id": zeile[0], "url": zeile[1], ...}
```

- `fetchone()` statt `fetchall()`: Es kann höchstens eine Zeile geben, weil
  die `id` eindeutig ist.
- `AND benutzer_id = %s`: Eine Stelle eines anderen Benutzers wird gar nicht
  gefunden.

### Route

[`src/app/stellenanzeigen_routes.py`, ab Zeile 208](../../../src/app/stellenanzeigen_routes.py#L208)

```python
@stellenanzeigen.get("/api/stellenanzeigen/<int:stellen_id>")
def stellenanzeige_oeffnen(stellen_id):
    ...
    if stelle is None:
        return jsonify({"fehler": "Diese Stelle wurde nicht gefunden."}), 404
    return jsonify(stelle)
```

- `<int:stellen_id>` ist ein **Platzhalter in der Adresse**. Bei
  `/api/stellenanzeigen/7` übergibt Flask die 7 als Zahl an `stellen_id`.
  `int:` lässt nur Zahlen durch; `/api/stellenanzeigen/abc` gibt automatisch
  404.
- «Gibt es nicht» und «gehört jemand anderem» geben **beide 404**. So verrät
  die Antwort nicht, ob es die id bei jemand anderem gibt.

### Frontend

[`public/index.html`, `stelle_oeffnen()` ab Zeile 422](../../../public/index.html#L422)

```js
async stelle_oeffnen(stellen_id) {
    const antwort = await fetch(`/api/stellenanzeigen/${stellen_id}`);
    const daten = await antwort.json();
    ...
    this.stellentitel = daten.titel || "";
    ...
    this.geoeffnete_stelle_id = daten.id;
    this.status = daten.status;
    this.ansicht = "formular";
}
```

- **Ein Formular für Erfassen und Bearbeiten**
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)).
  `geoeffnete_stelle_id` entscheidet über den Zustand: `null` = neue Stelle,
  eine Zahl = «Bestehend».
- `|| ""` macht aus `null` einen leeren Text, damit im Feld nicht «null»
  steht.

---

## 3. Stelle ändern (US 20003 und US 20004)

US 20003 hat nur den Status gespeichert. US 20004 hat denselben `PUT` auf
alle Felder ausser der `url` erweitert. Hier steht der heutige Stand.

### Prüfung wiederverwenden

[`src/app/datenbank.py`, ab Zeile 231](../../../src/app/datenbank.py#L231)

```python
def stellenanzeige_eingaben_pruefen(daten):      # Use Case 1, Erfassen
    ...
    url = textfeld_pruefen(daten.get("url"), "Link", pflicht=True)
    return {
        "url": anzeigenlink_bestimmen(url),
        **stellenfelder_pruefen(daten),
    }


def stellenfelder_pruefen(daten):                # neu in US 20004
    ...
    return {
        "titel": textfeld_pruefen(daten.get("titel"), "Titel", pflicht=True, ...),
        "firma": textfeld_pruefen(daten.get("firma"), "Firma", pflicht=True, ...),
        ...
    }
```

- **Knackpunkt:** Die Prüfung aus Use Case 1 verlangte immer eine `url`. Beim
  Ändern gibt es keine. Statt die Prüfung zu kopieren, haben wir sie in zwei
  Teile getrennt. Erfassen und Ändern verwenden **dieselben Regeln** (Titel
  und Firma Pflicht, Maximallängen), und das Erfassen verhält sich gleich wie
  vorher.
- `**` schüttet das Dictionary von `stellenfelder_pruefen()` in das neue
  Dictionary aus.

### Datenbank

[`src/app/datenbank.py`, ab Zeile 454](../../../src/app/datenbank.py#L454)

```python
def stellenanzeige_aktualisieren(datenbank_url, stellen_id, daten):
    geprueft = stellenfelder_pruefen(daten)

    status = daten.get("status")
    if status not in ERLAUBTE_STATUS:
        raise ValueError("Bitte einen gültigen Status wählen.")

    with verbindung_oeffnen(datenbank_url) as verbindung:
        ergebnis = verbindung.execute(
            """
            UPDATE stellenanzeigen
            SET titel = %s, firma = %s, arbeitsort = %s,
                inseratadresse_strasse = %s, inseratadresse_postleitzahl = %s,
                inseratadresse_ort = %s, pensum = %s, stellenbeschreibung = %s,
                status = %s,
                geaendert_am = CURRENT_TIMESTAMP
            WHERE id = %s AND benutzer_id = %s
            """,
            (geprueft["titel"], ..., status, stellen_id, aktuelle_benutzer_id()),
        )

    return ergebnis.rowcount == 1
```

- Erst prüfen, dann speichern. Ein ungültiger Wert erreicht die Datenbank nie.
- `ERLAUBTE_STATUS`: die sechs Werte aus dem Datenmodell. Die Tabelle prüft
  sie mit `CHECK` auch, aber nur mit einem technischen Fehler. Die eigene
  Prüfung liefert eine verständliche Meldung.
- Die `url` kommt im `UPDATE` **nicht vor**. Darum bleibt der Anzeigenlink
  fest, auch wenn jemand eine mitschickt.
- `geaendert_am = CURRENT_TIMESTAMP` bei jedem Speichern (Regel Z1).
- `rowcount` sagt, wie viele Zeilen geändert wurden: 1 = gefunden,
  0 = nicht gefunden. Daraus macht die Route 404.

### Route

[`src/app/stellenanzeigen_routes.py`, ab Zeile 241](../../../src/app/stellenanzeigen_routes.py#L241)

```python
@stellenanzeigen.put("/api/stellenanzeigen/<int:stellen_id>")
def stellenanzeige_aendern(stellen_id):
    daten = request.get_json(silent=True)
    try:
        gefunden = stellenanzeige_aktualisieren(datenbank_url, stellen_id, daten)
        if not gefunden:
            return jsonify({"fehler": "Diese Stelle wurde nicht gefunden."}), 404
        stelle = stellenanzeige_mit_id_lesen(datenbank_url, stellen_id)
    except ValueError as fehler:
        return jsonify({"fehler": str(fehler)}), 400
    except psycopg.Error:
        return jsonify({"fehler": "Speichern derzeit nicht möglich. ..."}), 503

    arbeitsweg = arbeitsweg_eintragen(stellen_id, stelle)

    return jsonify({"id": stellen_id, "status": stelle["status"], ...})
```

- `request.get_json()` holt den `body` der Anfrage als Dictionary.
- **Zusammenarbeit mit Use Case 3:** Nach dem Speichern ruft die Route Fabios
  `arbeitsweg_eintragen()` **unverändert** auf. Weil zuerst gespeichert und
  dann gelesen wird, rechnet sie automatisch mit der **neuen** Adresse
  (Entscheid O2 im [README](README.md)).
- 200 statt 201: Es ist nichts Neues entstanden, die Stelle wurde geändert.

### Frontend

[`public/index.html`, `stelle_aktualisieren()` ab Zeile 487](../../../public/index.html#L487)

```js
const antwort = await fetch(`/api/stellenanzeigen/${this.geoeffnete_stelle_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        titel: this.stellentitel,
        firma: this.firma,
        ...
        status: this.status,
    }),
});
```

- Es gehen **immer alle Felder** mit, auch unveränderte. Das Backend
  überschreibt die ganze Stelle. Entschieden, weil das einfacher zu prüfen und
  zu testen ist als einzelne Felder.
- Zwei Knöpfe «Speichern» mit `v-if` / `v-else`: neue Stelle → `POST`
  (Use Case 1), geöffnete Stelle → `PUT`.
- Das Status-Dropdown (`<select v-model="status">`) erscheint nur im Zustand
  «Bestehend». Eine neue Stelle startet immer mit `gespeichert`.
- Nach dem Speichern bleibt das Formular offen und zeigt «Gespeichert.» und
  den Arbeitsweg oder den Hinweis.

---

## 4. Stelle löschen (US 20005)

### Datenbank

[`src/app/datenbank.py`, ab Zeile 518](../../../src/app/datenbank.py#L518)

```python
def stellenanzeige_loeschen(datenbank_url, stellen_id):
    with verbindung_oeffnen(datenbank_url) as verbindung:
        ergebnis = verbindung.execute(
            """
            DELETE FROM stellenanzeigen
            WHERE id = %s AND benutzer_id = %s
            """,
            (stellen_id, aktuelle_benutzer_id()),
        )
    return ergebnis.rowcount == 1
```

- **Endgültig:** Die Zeile verschwindet, mit ihr der Arbeitsweg. Kein
  Papierkorb. Zum Abschliessen ohne Löschen gibt es die Status
  «Zurückgezogen» und «Absage».
- Ohne `WHERE` wären **alle** Stellen weg. Beim Löschen ist die doppelte
  Bedingung besonders wichtig, weil man es nicht rückgängig machen kann.

### Route

[`src/app/stellenanzeigen_routes.py`, ab Zeile 297](../../../src/app/stellenanzeigen_routes.py#L297)

```python
@stellenanzeigen.delete("/api/stellenanzeigen/<int:stellen_id>")
def stellenanzeige_entfernen(stellen_id):
    try:
        geloescht = stellenanzeige_loeschen(current_app.config["DATABASE"], stellen_id)
    except psycopg.Error:
        return jsonify({"fehler": "Löschen derzeit nicht möglich. ..."}), 503
    if not geloescht:
        return jsonify({"fehler": "Diese Stelle wurde nicht gefunden."}), 404
    return "", 204
```

- **204 «No Content»:** erledigt, aber nichts zurückzuschicken.
- Die Route heisst `stellenanzeige_entfernen`, weil `stellenanzeige_loeschen`
  schon die Datenbankfunktion ist. Zwei gleiche Namen in einer Datei würden
  sich überschreiben.

### Frontend

[`public/index.html`, Knopf ab Zeile 287, `stelle_loeschen()` ab Zeile 536](../../../public/index.html#L536)

```js
async stelle_loeschen() {
    if (!confirm("Stelle wirklich löschen?")) {
        return;
    }
    ...
    const antwort = await fetch(`/api/stellenanzeigen/${this.geoeffnete_stelle_id}`,
                                { method: "DELETE" });
    if (!antwort.ok) {
        const daten = await antwort.json();
        throw new Error(daten.fehler || "Löschen fehlgeschlagen.");
    }
    this.zur_uebersicht();
}
```

- `confirm()` ist ein Dialog des Browsers mit «OK» und «Abbrechen». Er liefert
  `true` oder `false`. Eine Zeile Code, passt zur minimalen Oberfläche
  ([ADR 0010](../../decisions/0010-minimale-oberflaeche.md)).
- **Kein `body`:** Die id in der Adresse genügt.
- **Knackpunkt:** Bei 204 ist die Antwort leer. `antwort.json()` würde einen
  Fehler werfen. Darum lesen wir JSON nur im Fehlerfall.
- Danach `zur_uebersicht()`: Die Stelle gibt es nicht mehr, also auch kein
  Formular.

---

## 5. Tests

Alle Tests laufen **ohne echte Datenbank**. Ein Mock (`MagicMock`) ersetzt die
Verbindung; in den Routentests ersetzt ein Mock die Datenbankfunktion und
Fabios Arbeitswegberechnung. Sonst würde ein Test echte Stellen ändern oder
löschen und den Kartendienst fragen.

| Datei | Tests | Prüft unter anderem |
|---|---|---|
| [`test_stellenanzeigen_uebersicht.py`](../../../tests/test_stellenanzeigen_uebersicht.py) | 7 | Dictionaries mit Namen, nur eigene Stellen neueste zuerst, leere Liste, 503, keine Arbeitswegberechnung |
| [`test_stellenanzeige_oeffnen.py`](../../../tests/test_stellenanzeige_oeffnen.py) | 8 | alle Felder mit Namen, `None` ohne Treffer, nur beim Demo-Benutzer, 404, id ohne Zahl, 503, keine Arbeitswegberechnung |
| [`test_status_aendern.py`](../../../tests/test_status_aendern.py) | 13 | alle Felder bereinigt gespeichert, url nie geändert, leere Pflichtfelder, ungültiger Status, 400/404/503, Arbeitswegberechnung |
| [`test_stelle_loeschen.py`](../../../tests/test_stelle_loeschen.py) | 6 | `DELETE` mit id **und** Benutzer, 204 ohne Inhalt, 404, 503 |

Typische Werkzeuge: `monkeypatch.setattr()` (Funktion ersetzen),
`pytest.raises(ValueError)` (erwarteter Fehler), `assert_not_called()` (z. B.
keine Berechnung bei 404), `call_args` (womit wurde aufgerufen?).

Im Browser geprüft: Übersicht, Öffnen, Status und Angaben ändern, leerer
Titel → 400, Löschen mit «Abbrechen» und «OK» (mit einer eigens angelegten
Teststelle).

---

## Entscheide auf einen Blick

| Entscheid | Gewählt | Verworfen, weil |
|---|---|---|
| Suche/Filter in der Übersicht | keine | ADR 0010, minimale Oberfläche |
| Detailansicht | dasselbe Formular, Zustand «Bestehend» | eigene Seite wäre doppelter Code (ADR 0005) |
| Was der PUT schickt | immer alle Felder | nur geänderte Felder bräuchte pro Feld eine Entscheidung im Backend |
| Arbeitsweg beim Speichern | immer neu berechnen | Vergleich alt/neu wäre zusätzlicher Code |
| Löschen | endgültig | «ausblenden» bräuchte neue Spalte und Änderungen an Übersicht und Öffnen |
| Rückfrage | `confirm()` | eigener Dialog: mehr Code, nur schöner |
| Antwort beim Löschen | 204 ohne Inhalt | 200 mit JSON wäre möglich, aber es gibt nichts zurückzugeben |
| Nach dem Speichern | Formular bleibt offen | sonst sieht man Arbeitsweg und Meldung nicht |
| Nach dem Löschen | zurück zur Übersicht | das Formular würde eine Stelle zeigen, die es nicht mehr gibt |

---

## Mögliche Fragen der Dozierenden

**«Warum haben Öffnen, Ändern und Löschen dieselbe Adresse?»**
Die Adresse beschreibt *die Sache* (Stelle 7), die HTTP-Methode *die Aktion*.
Flask ruft je nach Methode eine andere Funktion auf. Das ist üblich (REST) und
macht die Schnittstelle leicht lesbar.

**«Was passiert, wenn jemand die id einer fremden Stelle schickt?»**
Jede SQL-Abfrage hat `WHERE id = %s AND benutzer_id = %s`. Eine fremde Stelle
wird nicht gefunden, die Route antwortet mit 404. Die Antwort ist gleich wie
bei einer id, die es nicht gibt, und verrät darum nichts.

**«Warum prüft ihr den Status im Backend, wenn das Dropdown nur gültige Werte
anbietet?»**
Das Frontend kann man umgehen, z. B. mit einem `fetch` in der
Browser-Konsole. Prüfungen, auf die man sich verlassen muss, gehören ins
Backend. Die Datenbank prüft zusätzlich mit `CHECK`.

**«Was ist die technische Herausforderung in Use Case 2?»**
Der gemeinsame Speichervorgang mit den anderen Use Cases: Die Prüfung aus
Use Case 1 musste ohne `url` funktionieren, ohne das Erfassen zu verändern,
und die Arbeitswegberechnung aus Use Case 3 musste nach jedem Speichern mit
der neuen Adresse laufen, ohne Fabios Code zu ändern. Gelöst durch Aufteilen
der Prüfung und die Reihenfolge «speichern → lesen → berechnen».

**«Warum lest ihr bei DELETE kein JSON?»**
Bei Erfolg antwortet das Backend mit 204 ohne Inhalt. Ein `antwort.json()`
auf eine leere Antwort wirft einen Fehler. Nur im Fehlerfall schickt das
Backend eine Meldung als JSON.

## Bekannte Grenzen

- Nach dem ersten Speichern einer **neuen** Stelle wechselt das Formular noch
  nicht in den Zustand «Bestehend». Wer gleich weiterbearbeiten will, geht
  über die Übersicht. Bewusst zurückgestellt, weil es Use Case 1 betrifft.
- Der Arbeitsweg wird beim Ändern neu berechnet. Am 01.11.2026 scheiterte die
  Berechnung bei allen Stellen; Fabio korrigiert das in Use Case 3.
