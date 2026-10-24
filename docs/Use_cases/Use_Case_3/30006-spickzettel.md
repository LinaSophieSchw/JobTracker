# Spickzettel US 30006 – Arbeitsweg im Stellen-Formular sehen

Stand: 2026-10-24 · Umgesetzt von Fabio · Story: [US 30006](30006-arbeitsweg-im-formular-anzeigen.md)

Vorbereitung für die Präsentation. US 30006 baut auf
[US 30001](30001-spickzettel.md) und [US 30002](30002-spickzettel.md) auf.
Hier steht **nur, was sich geändert hat**. Wie der Arbeitsweg berechnet und
gespeichert wird, erklären die beiden anderen Spickzettel.

In den Codeblöcken fehlen die Kommentare; im Code stehen sie.
`← neu` markiert neue oder geänderte Zeilen.

## Wozu gibt es diese Story?

Bisher hing der Arbeitsweg nur an der Bestätigungsmeldung, und das Formular
verschwand nach dem Speichern. Jetzt stehen Strecke und Fahrzeit in einem
festen Kasten im Formular, unter der Stellenbeschreibung:

```
Stellenbeschreibung  [ ...langer Text... ]

┌ Arbeitsweg mit dem Auto (wird beim Speichern berechnet) ┐
│ Strecke    [ 44.5 km ]   ← nur lesbar                   │
│ Fahrzeit   [ 44 min  ]   ← nur lesbar                   │
└─────────────────────────────────────────────────────────┘
[Speichern] [Abbrechen]
```

**Die wichtigste Idee:** Das Backend musste dafür nichts Neues lernen. Es
schickte Fahrzeit und Strecke schon seit US 30002 mit. Neu ist nur, **wo**
das Frontend sie hinschreibt.

## Was passiert wann?

| Situation | Kasten | Meldung oben |
|---|---|---|
| Stelle geladen oder «Von Hand erfassen» | leer | – |
| 1. Klick «Speichern», Berechnung klappt | 44.5 km / 44 min | «Stellenanzeige gespeichert (ID: 12).» |
| 1. Klick «Speichern», Berechnung scheitert | leer | «… gespeichert (ID: 12). Arbeitsweg konnte nicht berechnet werden.» |
| 2. Klick «Speichern» | Werte bleiben | «Diese Stelle ist bereits gespeichert (ID: 12) und kann hier nicht bearbeitet werden.» |

## Der Ablauf auf einen Blick

```
Browser   Klick «Speichern» → fetch POST /api/stellenanzeigen
   │
Backend   stellenanzeige_anlegen()                         (unverändert)
   │        ├─ stellenanzeige_speichern()                  Abschnitt 4  (Meldung bei doppeltem Link)
   │        └─ arbeitsweg_eintragen()                      (US 30001/30002)
   │
Browser   {"id": 12, "fahrzeit_auto_in_minuten": 44,
           "strecke_auto_in_metern": 44522}
           → strecke_auto_text = "44.5 km"                  Abschnitt 3
           → fahrzeit_auto_text = "44 min"
           → Kasten zeigt die Werte                         Abschnitt 1
```

| Datei | Was sich geändert hat |
|---|---|
| `public/index.html` | Kasten im HTML, zwei neue Werte in `data()`, Leeren beim Laden, Füllen beim Speichern, Formular bleibt offen |
| `src/app/datenbank.py` | Meldung bei doppeltem Link ergänzt (Linas Code, abgesprochen) |
| `tests/test_stellenanzeige_speichern.py` | 1 angepasster Test von Lina |

Datenbank, Berechnung und Speicherroute wurden **nicht** geändert.

---

## 1. Der Kasten im HTML

[`public/index.html`, Zeilen 163–185](../../../public/index.html#L163-L185)

**Wozu:** Zeigt Strecke und Fahrzeit in zwei Feldern an, in die man nichts
eintippen kann.

```html
<fieldset>                                                          <!-- ← neu -->
    <legend>Arbeitsweg mit dem Auto (wird beim Speichern berechnet)</legend>
    <table>
        <tbody>
            <tr>
                <th scope="row"><label for="strecke_auto">Strecke</label></th>
                <td>
                    <input id="strecke_auto" type="text" :value="strecke_auto_text" readonly>
                </td>
            </tr>
            <tr>
                <th scope="row"><label for="fahrzeit_auto">Fahrzeit</label></th>
                <td>
                    <input id="fahrzeit_auto" type="text" :value="fahrzeit_auto_text" readonly>
                </td>
            </tr>
        </tbody>
    </table>
</fieldset>
```

**Der Reihe nach:**
1. `<fieldset>` mit `<legend>` → zeichnet einen Rahmen mit Titel um die zwei
   Felder. So sieht man, dass sie zusammengehören.
2. `<table>` → dieselbe Anordnung wie im restlichen Formular: links die
   Beschriftung, rechts das Feld.
3. `:value="strecke_auto_text"` → Vue schreibt den Wert ins Feld.
4. `readonly` → Der Nutzer kann nichts eintippen.

*Warum `:value` und nicht `v-model` wie bei den anderen Feldern?*
`v-model` geht in **beide** Richtungen: Wert → Feld und Eingabe → Wert. Das
braucht man, wenn der Nutzer etwas eintippt. `:value` geht nur in **eine**
Richtung: Wert → Feld. Mehr braucht es nicht, weil hier nur das Backend die
Werte liefert. Vergleich: `v-model` ist ein Telefongespräch, `:value` eine
Anzeigetafel.

## 2. Zwei neue Werte und das Leeren

[`public/index.html`, Zeilen 236–239](../../../public/index.html#L236-L239),
[Zeilen 275–277](../../../public/index.html#L275-L277) und
[Zeilen 324–326](../../../public/index.html#L324-L326)

**Wozu:** Vue braucht für jedes Feld einen Wert in `data()`. Bei einer neuen
Stelle müssen beide wieder leer sein.

```javascript
// in data()
strecke_auto_text: "",            // ← neu, z. B. „44.5 km“
fahrzeit_auto_text: "",           // ← neu, z. B. „44 min“

// in stellenanzeige_manuell_erfassen() und stellenanzeige_laden()
this.strecke_auto_text = "";      // ← neu
this.fahrzeit_auto_text = "";     // ← neu
```

**Der Reihe nach:**
1. `strecke_auto_text: ""` → Am Anfang ist der Kasten leer.
2. `this.strecke_auto_text = "";` in den beiden Funktionen → leert den Kasten,
   sobald eine neue Stelle geladen oder «Von Hand erfassen» gewählt wird.

*Warum braucht es das Leeren?* Ohne diese Zeilen stünde nach dem Laden der
nächsten Stelle noch der Arbeitsweg der vorherigen im Kasten. Das wäre eine
falsche Angabe.

*Warum ein fertiger Text statt der Zahl?* Im Feld soll «44.5 km» stehen,
mit Einheit. Den Text bauen wir einmal beim Speichern zusammen
(Abschnitt 3), dann muss das HTML nur noch anzeigen.

## 3. Speichern füllt den Kasten, das Formular bleibt offen

[`public/index.html`, Zeilen 375–394](../../../public/index.html#L375-L394)

**Wozu:** Schreibt die Werte aus der Antwort des Backends in den Kasten
statt in die Meldung.

```javascript
if (daten.fahrzeit_auto_in_minuten === null) {
    this.strecke_auto_text = "";                                        // ← neu
    this.fahrzeit_auto_text = "";                                       // ← neu
    this.erfolgsmeldung += " Arbeitsweg konnte nicht berechnet werden.";
} else {
    const strecke_in_km =
        (daten.strecke_auto_in_metern / 1000).toFixed(1);
    this.strecke_auto_text = `${strecke_in_km} km`;                     // ← neu
    this.fahrzeit_auto_text = `${daten.fahrzeit_auto_in_minuten} min`;  // ← neu
}
// this.vorschau_vorhanden = false;                                    ← weg
```

**Der Reihe nach:**
1. `if (... === null)` → Die Berechnung ist gescheitert. Der Kasten bleibt
   leer, und der Hinweis kommt an die Meldung, wie bisher.
2. `(daten.strecke_auto_in_metern / 1000).toFixed(1)` → Meter in Kilometer
   mit einer Nachkommastelle: `44522 / 1000 = 44.522` → `"44.5"`. Das gab es
   schon in US 30002.
3. `` this.strecke_auto_text = `${strecke_in_km} km` `` → **neu:** schreibt
   «44.5 km» in den Kasten. Vorher wurde der Text an die Meldung angehängt.
4. `` this.fahrzeit_auto_text = `${...} min` `` → **neu:** schreibt «44 min»
   in den Kasten.
5. ~~`this.vorschau_vorhanden = false;`~~ → **weg.** Diese Zeile hat das ganze
   Formular nach dem Speichern ausgeblendet. Dann hätte man den gefüllten
   Kasten nie gesehen.

*Was passiert beim zweiten Klick?* Das Backend meldet einen Fehler
(Abschnitt 4). Dann springt der Code in den `catch`-Block, der nur die
Fehlermeldung setzt. Den Kasten fasst er nicht an, deshalb bleiben die Werte
stehen.

*Was ist `` `${...}` ``?* Ein Text mit Platzhaltern (Template-String). Was
zwischen `${` und `}` steht, setzt JavaScript als Wert ein:
`` `${44} min` `` ergibt `"44 min"`.

## 4. Klarere Meldung bei einem doppelten Link

[`src/app/datenbank.py`, Zeilen 291–297](../../../src/app/datenbank.py#L291-L297)

**Wozu:** Sagt dem Nutzer, warum ein zweiter Klick auf «Speichern» nichts
speichert.

```python
raise ValueError(
    f"Diese Stelle ist bereits gespeichert (ID: {vorhanden[0]}) "  # ← neu
    "und kann hier nicht bearbeitet werden."                      # ← neu
)
```

**Der Reihe nach:**
1. `raise ValueError(...)` → bricht das Speichern ab. Die Route macht daraus
   eine Antwort mit Status 400 und der Meldung, wie bisher.
2. Die zwei Texte stehen direkt hintereinander. Python setzt sie zu **einem**
   Text zusammen. So bleibt jede Zeile unter 88 Zeichen.
3. **Neu** ist der Zusatz «und kann hier nicht bearbeitet werden».

*Warum braucht es den Zusatz?* Das Formular bleibt jetzt nach dem Speichern
offen, und man kann noch darin tippen. Wer etwas ändert und nochmals
speichert, soll nicht glauben, die Änderung sei gespeichert. Das Bearbeiten
gespeicherter Stellen kommt mit Use Case 2.

## 5. Test

[`tests/test_stellenanzeige_speichern.py`, Zeilen 170–199](../../../tests/test_stellenanzeige_speichern.py#L170-L199)

| Test | Prüft |
|---|---|
| `test_speichern_meldet_bestehenden_eintrag` | angepasst (Linas Test): Die Meldung enthält die ID **und** den Zusatz «und kann hier nicht bearbeitet werden» |

Das Frontend haben wir im Browser geprüft: den doppelten Link mit dem echten
Backend (Link von Stelle 11), Erfolg und gescheiterte Berechnung mit
vorgetäuschten Antworten, damit keine Testdaten in der Datenbank landen.

---

## Mögliche Fragen der Dozierenden

**«Warum wird beim zweiten Klick auf ‹Speichern› nicht neu berechnet?»**
Die Speicherroute `POST /api/stellenanzeigen` legt immer eine **neue** Stelle
an. Gibt es den Link schon, bricht sie ab, bevor die Berechnung kommt. Eine
bestehende Stelle zu aktualisieren (`PUT /api/stellenanzeigen/<id>`) gehört zu
Use Case 2. Die Neuberechnung dabei ist unsere geplante Story US 30003.

**«Warum habt ihr das Backend für die Anzeige nicht geändert?»**
Es war nicht nötig. Die Speicherroute schickte Fahrzeit und Strecke schon
seit US 30002 mit. Es fehlte nur ein fester Platz im Formular. Deshalb ist
die Änderung fast nur im Frontend; im Backend kam nur der klarere Text der
Meldung dazu.
