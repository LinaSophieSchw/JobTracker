# US 30004 – Demo-Benutzer mit Wohnadresse fest im System hinterlegen

Status: Umgesetzt (PR #17) – Voraussetzung für die Stories 30001 bis 30003

Datum: 2026-10-21, umgesetzt 2026-10-21

Spickzettel zur Umsetzung: [30004-spickzettel.md](30004-spickzettel.md)

## User Story

Als Nutzer möchte ich, dass ein Benutzer mit Wohnadresse fest im System hinterlegt ist, damit alle erfassten Stellen diesem Benutzer zugeordnet werden und die Wohnadresse als Ausgangspunkt für die Arbeitswegberechnung zur Verfügung steht, ohne dass ich zuerst ein Profil erfassen muss.

## Hintergrund

In der Teambesprechung vom 21.10.2026 wurde festgehalten, dass vorläufig kein Profil erfasst wird. Stattdessen ist ein Dummy-Benutzer im System angelegt, dem alle erfassten Stellen zugeordnet werden. Das bleibt so, bis geklärt ist, wer das Profil anlegen übernimmt. Eine Maske zur Erfassung des Nutzers kann später ergänzt werden; in Version 1 gibt es keine.

## Umfang des ersten Vertical Slice

Der Demo-Benutzer wird beim Anlegen der Tabellen automatisch mit Name und Wohnadresse in die Datenbank geschrieben. Die Wohnadresse besteht aus drei Feldern. Die Arbeitswegberechnung liest sie von dort. Es gibt keine Oberfläche, über die der Benutzer oder seine Wohnadresse erfasst oder geändert wird.

Gemeinsame Festlegungen für diesen Slice:

- Die Wohnadresse ist beim Demo-Benutzer **fest in drei Feldern hinterlegt**: **Strasse mit Hausnummer, Postleitzahl und Ort** ([ADR 0009](../../decisions/0009-adresse-in-drei-feldern.md)).
- **Es gibt keine Maske zur Erfassung des Nutzers.** Name und Wohnadresse werden im Code festgelegt und nicht über die Oberfläche eingegeben.
- Alle Stellen gehören über `benutzer_id` zum Demo-Benutzer mit `id` 1; `aktuelle_benutzer_id()` liefert immer 1 ([ADR 0003](../../decisions/0003-benutzer-ohne-login.md)).
- Es werden **keine Eingabevalidierungen** vorgenommen.
- **Schweiz ist fest vorgegeben.** Es gibt keine Länderauswahl.
- Verwendet wird eine öffentliche Beispieladresse ohne Bezug zu realen Personen (Vorschlag: Bundesplatz 3, 3005 Bern).

## Ablauf

1. Die Anwendung legt beim Start die Tabellen an.
2. Fehlt der Demo-Benutzer mit `id` 1, schreibt sie ihn mit Name und Wohnadresse in drei Feldern in die Tabelle `benutzer`.
3. Ist der Demo-Benutzer bereits vorhanden, bleibt er unverändert.
4. Jede neu gespeicherte Stelle wird dem Demo-Benutzer zugeordnet.
5. Beim Speichern einer Stelle liest die Arbeitswegberechnung die Wohnadresse des Demo-Benutzers aus der Datenbank.

## Akzeptanzkriterien

- [x] Nach dem Anlegen der Tabellen existiert in `benutzer` genau ein Datensatz mit `id` 1.
- [x] Der Datensatz enthält einen Namen sowie die Wohnadresse in den Spalten `wohnadresse_strasse` (mit Hausnummer), `wohnadresse_postleitzahl` und `wohnadresse_ort`.
- [x] Wiederholtes Anlegen der Tabellen erzeugt keinen zweiten Benutzer und verändert den vorhandenen nicht.
- [x] Jede gespeicherte Stelle erhält `benutzer_id` 1. Die ID wird nicht aus Formulareingaben übernommen.
- [x] Stellen können sofort gespeichert werden; es muss vorher kein Profil erfasst werden.
- [x] Die Wohnadresse kann für die Arbeitswegberechnung aus der Datenbank gelesen werden.
- [x] Es gibt keine Maske und keinen Backend-Aufruf zum Erfassen oder Ändern des Benutzers oder seiner Wohnadresse.

## Schrittweise Umsetzung

1. Den bestehenden Demo-Benutzer in `tabellen_erstellen()` prüfen. Er speichert die Wohnadresse heute noch in einer einzigen Spalte `wohnadresse`.
2. Die Tabelle `benutzer` gemäss [Datenmodell](../../datenmodell.md) auf die drei Spalten `wohnadresse_strasse`, `wohnadresse_postleitzahl` und `wohnadresse_ort` umstellen und den Demo-Benutzer entsprechend einfügen.
3. Eine kleine Funktion ergänzen, welche die Wohnadresse des aktuellen Benutzers aus der Datenbank liest.
4. Testen: Benutzer wird angelegt, erneutes Anlegen ändert nichts, Wohnadresse wird in drei Teilen gelesen.

## Noch nicht enthalten

- Maske oder Profilseite zur Erfassung des Nutzers; kann später ergänzt werden.
- Ändern von Name oder Wohnadresse über die Oberfläche.
- Mehrere Benutzer, Anmeldung und Berechtigungen.
- Sperre von «+ Neue Stelle», solange kein Profil existiert; sie entfällt, weil der Benutzer immer vorhanden ist.
- Arbeitswegberechnung; folgt in den Stories 30001 bis 30003.

## Technische Prüfung vor der Umsetzung

Der Demo-Benutzer wird bereits in `src/app/datenbank.py` angelegt, aber mit einer einzigen Spalte `wohnadresse`. Vor der Umsetzung mit Lina abstimmen, wer die Umstellung auf drei Spalten übernimmt, und prüfen, ob in bestehenden Datenbanken (lokal und bei Neon) die Tabelle `benutzer` schon mit der alten Spalte existiert. `CREATE TABLE IF NOT EXISTS` ändert eine vorhandene Tabelle nicht; die Tabelle muss in diesem Fall einmal neu angelegt oder angepasst werden.

Das [Datenmodell](../../datenmodell.md) (Abschnitt 3 und Regel B2) und [ADR 0010](../../decisions/0010-minimale-oberflaeche.md) gehen noch davon aus, dass der Benutzer erst beim ersten Speichern des Profils entsteht und «+ Neue Stelle» bis dahin gesperrt ist. Diese Stellen müssen an den fest hinterlegten Benutzer angepasst werden.
