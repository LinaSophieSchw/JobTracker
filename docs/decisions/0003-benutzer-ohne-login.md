# Ein Benutzer ohne Login, vorbereitet für mehrere Benutzer

Datum: 2026-10-19

## Status

Angenommen

## Kontext

Ein Login ist für Version 1 zu aufwendig (Teambesprechung vom 12.10.2026).
Das Profil braucht aber einen Ort für Name und Wohnadresse, und eine spätere
Erweiterung auf mehrere Benutzer soll ohne Umbau des Datenmodells möglich sein.
Die Applikation ist öffentlich erreichbar.

## Betrachtete Optionen

- **Option 1: Ohne Benutzerbezug.** Am einfachsten. Für mehrere Benutzer
  müssten später jede Tabelle und jede Abfrage geändert und bestehende Daten
  migriert werden.
- **Option 2: Tabelle `benutzer` und Spalte `benutzer_id` ab Start, ohne
  Login.** Wenig Mehraufwand jetzt. Ein Login ersetzt später nur die Funktion,
  die den aktuellen Benutzer liefert.
- **Option 3: Login sofort.** Registrierung, Passwörter, Sitzungen und
  Berechtigungen. Für Version 1 zu viel.

## Entscheidung

Option 2 bestätigt: Tabelle `benutzer` und Spalte `benutzer_id` ab Start,
ohne Login.

## Begründung

Der Mehraufwand ist klein (eine Tabelle, eine Spalte, eine Funktion), solange
noch keine Daten bestehen. Später wäre dieselbe Änderung eine Migration mit
Risiko.

## Konsequenzen

- Tabelle `benutzer` mit genau einem Datensatz (`id` 1). Das Profil ist dieser
  Datensatz.
- Jede Abfrage auf `stellenanzeigen` filtert über `aktuelle_benutzer_id()`,
  die heute immer 1 liefert (Regel B1 im [Datenmodell](../datenmodell.md)).
- SQLite prüft Fremdschlüssel nur mit `PRAGMA foreign_keys = ON` pro
  Verbindung.
- Jede Person mit der URL sieht und ändert alle Daten. Deshalb enthält die
  öffentliche Instanz nur Demodaten.
- Später ersetzt ein Login die Funktion `aktuelle_benutzer_id()` durch den
  angemeldeten Benutzer. Das Datenmodell bleibt.
