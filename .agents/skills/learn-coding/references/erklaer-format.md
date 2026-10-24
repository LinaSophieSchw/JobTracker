# Erklärformat nach jeder Umsetzung

Nach jeder Änderung im Code erklärt der Agent im Chat, **was wo geändert
wurde und was es macht**, immer in diesem Format. Es gilt für neue Funktionen
ebenso wie für Vereinfachungen, Umbauten und Fehlerbehebungen. Eine
Stichwortliste wie «Backend: `arbeitsweg.py` geändert» genügt nicht.

Gewünscht vom Team (Fabio, 24.10.2026), weil jede Person jede Codestelle in
der Präsentation erklären können muss.

## Aufbau

Pro Schritt bzw. pro geänderter Datei ein Block:

1. **Überschrift:** «Schritt N ist fertig: <was jetzt funktioniert>»
2. **Ort:** «Ergänzt/Geändert in `<datei>`: <was>, ab Zeile N.» Die Datei als
   anklickbarer Link mit Zeile.
3. **«Wozu gibt es den neuen Teil?»** In 1–3 Sätzen, wozu der Code da ist,
   dazu ein konkretes Beispiel als kleiner Codeblock (z. B.
   `Bundesplatz 3, Bern → Bahnhofstrasse 12, Zug = 95 Minuten`).
4. **«Was der neue Teil macht, der Reihe nach»:**
   - Jede Funktion ist ein nummerierter Punkt, beginnend mit ihrer Kopfzeile:
     `def name(...):` und einem kurzen Satz, was sie tut.
   - Darunter die Schritte in der Reihenfolge, in der sie ablaufen. Jeder
     Schritt beginnt mit dem Codestück, auf das er sich bezieht:
     `codestück` → Erklärung in Alltagssprache.
   - Wo es nicht offensichtlich ist: «Warum es das braucht: …».
   - Bei Änderungen an bestehendem Code sagen, was vorher war und was **neu**
     ist. Weggefallene Zeilen durchgestrichen zeigen (~~`zeile`~~ → weg).
5. Optional am Schluss: **«Was heisst …?»** für einen neuen Kernbegriff und
   **«Wie es ins Ganze passt»** als kleines ASCII-Bild.

## Flughöhe

- Nicht Zeile für Zeile, sondern die Codestücke, die man in der Präsentation
  zeigen würde.
- Keine Interna von Bibliotheken, keine langen Tabellen, keine Fachbegriffe
  ohne Not.
- Lieber kürzer und nachfragen, ob mehr Tiefe gewünscht ist.

## Beispiel

```markdown
## Schritt 2 ist fertig: Die Datei berechnet jetzt die Fahrzeit

Ergänzt in `src/app/arbeitsweg.py`: drei neue Funktionen ab Zeile 89.

**Wozu gibt es den neuen Teil?**
In Schritt 1 haben wir gelernt, eine Adresse in einen Punkt auf der Karte zu
übersetzen. Jetzt fragen wir den Kartendienst: «Wie lange fährt man mit dem
Auto von Punkt A nach Punkt B?» Die Antwort rechnen wir in Minuten um:

    Bundesplatz 3, Bern  →  Bahnhofstrasse 12, Zug   =   95 Minuten

**Was der neue Teil macht, der Reihe nach**

1. `def fahrzeit_in_sekunden_abfragen(start, ziel, api_schluessel):` fragt
   nach der Fahrzeit.
   1. `antwort = requests.post(ROUTE_URL, json={"coordinates": [start, ziel]}, ...)`
      → schickt die zwei Punkte an den Kartendienst.
      * Nur zwei Punkte heisst: einfacher Hinweg.
      * `post` statt `get`, weil wir die Punkte mitschicken müssen.
   2. `return antwort.json()["routes"][0]["summary"]["duration"]` → holt die
      Fahrzeit aus der Antwort, zum Beispiel `5682.0` Sekunden.

2. `def fahrzeit_berechnen(wohnadresse, arbeitsadresse, api_schluessel):` ist
   die Hauptfunktion. Die Speicherroute ruft nur diese eine Funktion auf.
   1. `try:` → «Versuch Folgendes». Darin die Arbeitsschritte:
      * `start = koordinaten_suchen(wohnadresse, ...)` → Wohnadresse wird zu
        Punkt A.
      * `ziel = koordinaten_suchen(arbeitsadresse, ...)` → Arbeitsadresse wird
        zu Punkt B.
   2. `except Exception: return None` → fängt jeden Abbruch auf und gibt
      «keine Fahrzeit» zurück.
      * Warum alle gleich? Die Story verlangt in jedem Fall dieselbe Meldung
        ohne technische Details.
   3. `return round(sekunden / 60)` → Aus 5682 Sekunden werden 95 Minuten.
```
