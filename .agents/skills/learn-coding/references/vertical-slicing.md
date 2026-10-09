# Vertical Slicing

## Was ein Vertical Slice ist

Eine Webapplikation hat Schichten (n-Tier-Modell aus dem Unterricht):

```
            Slice
              │
┌─────────────┼─────────────┐
│ Frontend    ▓  (HTML/JS im Browser)
├─────────────┼─────────────┤
│ Backend     ▓  (Python/Flask, Web Service)
├─────────────┼─────────────┤
│ Datenbank   ▓
└─────────────┼─────────────┘
```

Ein Vertical Slice ist ein schmaler, senkrechter Schnitt durch alle Schichten,
der genau **eine User Story** umsetzt, z. B. «eine neue Bewerbung erfassen».
Am Ende eines Slices kann man im Browser etwas tun, und es kommt bis in die
Datenbank und wieder zurück.

Das Gegenteil wäre horizontal: zuerst alle Tabellen, dann alle Routen, dann
alle Seiten. Das Problem dabei: Erst ganz am Schluss merkt man, ob die Teile
zusammenpassen, und bis dahin kann man nichts zeigen.

Ein Slice darf anfangs in einer Schicht sehr dünn sein, z. B. noch kein
Styling im Frontend oder vorerst nur in einer Python-Liste oder Datei
gespeichert statt in der Datenbank. Wichtig ist, dass er einmal ganz
durchläuft. Danach wird er Schritt für Schritt dicker.

## Reihenfolge für eine Story «Daten erfassen»

Diese Reihenfolge entspricht dem Vorgehen aus dem Unterricht. Nach jedem
Schritt kann man etwas ausprobieren.

| # | Schicht | Schritt | So sieht man, dass es geht |
|---|---------|---------|----------------------------|
| 0 | Backend | **Server läuft** (nur einmal pro Projekt): Flask startet, eine Route liefert die Startseite aus. | Browser zeigt die Seite unter der Adresse, die Flask im Terminal ausgibt (z. B. `http://127.0.0.1:5000`; auf macOS ist Port 5000 oft durch AirPlay belegt, dann einen anderen Port wählen) |
| 1 | Frontend | **Eingabemaske** in HTML: Formular mit den nötigen Feldern, ohne Styling. | Formular erscheint im Browser |
| 2 | Frontend | **Daten abschicken:** Beim Klick werden die Formulardaten an eine Backend-URL geschickt (z. B. mit `fetch` als JSON). | Im Browser-Netzwerk-Tab sieht man den Request |
| 3 | Backend | **Daten entgegennehmen:** Route nimmt die Daten an und gibt sie vorerst einfach zurück. | Antwort erscheint im Browser oder Terminal |
| 4 | Backend/DB | **Speichern:** zuerst ruhig in einer Python-Liste oder Datei, damit der Slice durchläuft; danach (eigener Schritt) in der Datenbank. | Daten sind nach dem Abschicken gespeichert |
| 5 | alle | **Anzeigen:** Backend gibt die gespeicherten Daten zurück, Frontend zeigt sie als Liste. | Neuer Eintrag erscheint in der Liste |
| 6 | Tests | **Unittests** für die Logik und die Routen. | `uv run pytest` ist grün |
| 7 | optional | **Verdicken:** Validierung, Fehlermeldungen, Styling – jeweils als eigener kleiner Schritt. | je nach Schritt |

Die Aufgabenstellung verlangt am Ende eine echte Datenbank. Die Liste oder
Datei in Schritt 4 ist nur ein Zwischenstand. Der Agent sagt das beim Bauen
dazu, damit niemand denkt, es sei schon fertig.

## Reihenfolge für eine Story «Daten anzeigen, suchen, filtern»

Hier fliessen die Daten vor allem von unten nach oben, also beginnt man
dort, wo die Daten liegen:

1. Datenbank-Abfrage als Python-Funktion (mit Test).
2. Backend-Route, die das Ergebnis als JSON liefert. Im Browser direkt die URL
   aufrufen und das JSON anschauen.
3. Frontend ruft die Route auf und zeigt die Daten an.
4. Eingaben (Suchfeld, Filter) im Frontend, die als Parameter mitgeschickt
   werden.

## Wie gross ist ein Slice?

- Eine Person schafft ihn in ein bis drei Arbeitssitzungen.
- Am Ende kann man ihn im Browser vorführen.
- Er lässt sich in einem Satz als User Story beschreiben.

Ist eine Story grösser, wird sie geteilt, z. B. «Bewerbung erfassen» zuerst
nur mit Firma und Stelle, und «Status ändern» später als eigener Slice.

Die Aufgabenstellung verlangt mindestens zwei wesentliche Operationen, also
mindestens zwei solche User Stories, die funktionieren.

## Schichtenbild für die Erklärungen

Nach jedem Schritt zeigt der Agent den Stand, damit das Gesamtbild sichtbar
bleibt:

```
Story: Neue Bewerbung erfassen

Frontend   ✅ Formular (static/index.html)   ✅ fetch beim Klick
Backend    ✅ POST /api/bewerbungen          ⬅️ jetzt: speichern
Datenbank  ⬜ Tabelle bewerbungen
Tests      ⬜
```

## Beispiel: Plan für den JobTracker

> **User Story:** Als Bewerber:in möchte ich eine neue Bewerbung mit Firma
> und Stelle erfassen, damit ich den Überblick behalte.
>
> Danach funktioniert: Formular ausfüllen, «Speichern» klicken, die Bewerbung
> erscheint in der Liste darunter.
>
> 1. Frontend – `src/app/static/index.html`: Formular mit Firma und Stelle
> 2. Frontend – `index.html`: beim Klick Daten als JSON an
>    `POST /api/bewerbungen` schicken
> 3. Backend – `src/app/__init__.py`: Route nimmt die Daten entgegen
> 4. Backend – vorerst in einer Liste speichern, danach in der Datenbank
> 5. Backend + Frontend: `GET /api/bewerbungen` und Anzeige als Liste
> 6. Tests – `tests/test_bewerbungen.py`
>
> Noch nicht in diesem Slice: Status ändern, Löschen, Styling.

## Typische Fehler, die der Agent vermeidet

- Zuerst das komplette Datenbankschema für alle zukünftigen Features bauen.
- Zuerst das CSS schön machen, bevor irgendetwas gespeichert wird.
- Ein Backend bauen, das man nur im Test, aber nie im Browser sehen kann.
- Mehrere Stories gleichzeitig anfangen und keine fertig machen.
