# Ein Formular für Vorschau, Erfassung, Detail und Bearbeitung

Datum: 2026-10-19

## Status

Angenommen

## Kontext

Use Case 1 (Stellenanzeige erfassen) braucht ein Formular für die Vorschau und
die manuelle Erfassung. Use Case 2 (Stellenanzeigen verwalten) braucht eine
Detailansicht und eine Bearbeitung. Die Stellenbeschreibung ist lang und passt
nicht in eine Zeile der Übersicht.

## Betrachtete Optionen

- **Option 1: Eigene Detailansicht und eigenes Bearbeitungsformular.** Zwei
  Ansichten mit denselben Feldern, doppelter Aufwand.
- **Option 2: Zeile in der Übersicht aufklappen.** Zum Bearbeiten braucht es
  trotzdem ein Formular.
- **Option 3: Ein Formular für alles.** Eine Ansicht, die zwei Use Cases
  gemeinsam nutzen.

## Entscheidung

Option 3 angenommen: ein Formular für alles.

Das Formular kennt drei Zustände:

| Zustand | Auslöser | Feld `url` | Schaltflächen |
|---|---|---|---|
| Neu aus Vorschau | Vorschau erfolgreich (Use Case 1) | nur lesbar | Speichern, Abbrechen |
| Neu manuell | Vorschau fehlgeschlagen oder «Von Hand erfassen» (Use Case 1) | bearbeitbar, vorausgefüllt falls vorhanden | Speichern, Abbrechen |
| Bestehend | Klick auf eine Zeile der Übersicht (Use Case 2) | nur lesbar, als Link zur Anzeige | Speichern, Löschen, Zurück |

Die Stellenbeschreibung ist ein grosses Textfeld. Die Fahrzeit erscheint als
nur lesbares Feld, das Use Case 3 liefert.

## Begründung

Eine Ansicht statt zwei. Der Benutzer sieht beim Erfassen und beim Bearbeiten
dieselben Felder am selben Ort.

## Konsequenzen

- Das Formular gehört zu Use Case 1. Use Case 2 verwendet es, Use Case 3
  ergänzt die Fahrzeit.
- Änderungen am Formular sprechen die Verantwortlichen von Use Case 1 und
  Use Case 2 ab. Pull Requests am Formular prüft jeweils die andere Person.
- Die Felder des Formulars entsprechen der Tabelle `stellenanzeigen` im
  [Datenmodell](../datenmodell.md).
