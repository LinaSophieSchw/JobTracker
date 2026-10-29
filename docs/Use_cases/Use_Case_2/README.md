# Use Case 2 – Stellenanzeigen verwalten

Stand: 2026-10-29

**Status:** Entwurf

## Ziel

Der Nutzer behält den Überblick über alle erfassten Stellen und den Stand
seiner Bewerbungen. Er sieht alle Stellen in einer Liste, öffnet eine Stelle,
ändert ihren Status und weitere Angaben und löscht Stellen, die ihn nicht mehr
interessieren.

## User Stories

| Reihenfolge | User Story | Endpunkt | Stand |
|---|---|---|---|
| 1 | [US 20001 – Übersicht aller Stellen sehen](20001-uebersicht-aller-stellen.md) | `GET /api/stellenanzeigen` | Umgesetzt |
| 2 | [US 20002 – Stelle aus der Übersicht öffnen](20002-stelle-oeffnen.md) | `GET /api/stellenanzeigen/<id>` | Umgesetzt |
| 3 | [US 20003 – Status einer Stelle ändern](20003-status-aendern.md) | `PUT /api/stellenanzeigen/<id>` (nur `status`) | In Arbeit |
| 4 | US 20004 – Weitere Angaben einer Stelle bearbeiten | derselbe `PUT`, erweitert | Geplant |
| 5 | US 20005 – Stelle löschen | `DELETE /api/stellenanzeigen/<id>` | Geplant |

Die Stories werden einzeln ausgearbeitet: erst eine Story schreiben und
umsetzen, dann die nächste. So fliessen Erkenntnisse aus der Umsetzung in die
folgenden Stories ein.

Die Reihenfolge geht vom Lesen zum Schreiben. Zuerst muss man die Stellen
sehen und öffnen können, bevor man sie ändert oder löscht.

US 20003 und US 20004 sind bewusst getrennt. US 20003 ist der kleinste
sinnvolle Schritt, um eine bestehende Stelle zu speichern. US 20004 erweitert
denselben Speichervorgang um die übrigen Felder.

## Oberfläche

Use Case 2 verwendet die zwei Screens aus
[ADR 0010](../../decisions/0010-minimale-oberflaeche.md):

- **Übersicht (Startseite):** reine Liste mit Titel, Firma, Arbeitsort,
  Status und Arbeitsweg. Kein Filter, keine Suche. Ein Klick auf eine Zeile
  öffnet die Stelle.
- **Stellen-Formular im Zustand «Bestehend»**
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)):
  Feld `url` nur lesbar als Link zur Anzeige, Schaltflächen «Speichern»,
  «Löschen» und «Zurück». Der Status wird im Formular über ein Dropdown
  gewählt, nicht direkt in der Übersicht.

Nach dem Speichern bleibt das Formular offen, damit Arbeitsweg oder Hinweis
sichtbar sind; mit «← Zurück zur Übersicht» kehrt man zurück. Entschieden am
29.10.2026 (Mirko), wie bei neuen Stellen (US 20001). Vor dem Löschen fragt
die Oberfläche nach.

## Voraussetzungen

- Die Tabelle `stellenanzeigen` gemäss [Datenmodell](../../datenmodell.md).
- Der Demo-Benutzer mit `id` 1 ist fest hinterlegt
  ([US 30004](../Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md)).
- Es sind Stellen gespeichert, aus Use Case 1 oder als Demodaten.
- Das Stellen-Formular aus Use Case 1.

## Abgrenzung

| Was | Wo |
|---|---|
| Stelle erfassen, Stellen-Formular und seine Felder | Use Case 1 |
| Übersicht, Öffnen, Ändern und Löschen bestehender Stellen | Use Case 2 |
| Arbeitsadresse einer bestehenden Stelle ändern | Use Case 2 (US 20004) |
| Arbeitsweg berechnen, auch beim erneuten Speichern | Use Case 3 (US 30003) |
| Demo-Benutzer mit Wohnadresse | Use Case 3 (US 30004) |

Use Case 2 baut den Speichervorgang für bestehende Stellen
(`PUT /api/stellenanzeigen/<id>`). Use Case 3 hängt die Neuberechnung des
Arbeitswegs an denselben Speichervorgang (US 30003). Wer welchen Teil baut,
sprechen die Verantwortlichen von Use Case 2 und Use Case 3 vor US 20003 ab.

Use Case 2 zeigt Fahrzeit und Strecke nur an. Er berechnet sie nicht.

## Status

Erlaubt sind nur die Werte aus Abschnitt 5 im
[Datenmodell](../../datenmodell.md): `gespeichert`, `beworben`, `interview`,
`zusage`, `absage`, `zurueckgezogen`. Jeder Status darf in jeden anderen
wechseln. `geaendert_am` wird auch bei einer reinen Statusänderung neu gesetzt
(Regel Z1).

## Ausserhalb des Umfangs

- Suche und Filter in der Übersicht
  ([ADR 0010](../../decisions/0010-minimale-oberflaeche.md)).
- Status direkt in der Übersicht ändern.
- Sortieren der Übersicht nach Spalten.
- Erfolgs- und Hinweismeldungen nach dem Speichern.
- Ändern des Anzeigenlinks (`url`); er ist nach dem Anlegen fest.
- Verlauf der Statusänderungen.
- Maske zum Ändern des Profils (Name und Wohnadresse des Demo-Benutzers).
- Berechnung des Arbeitswegs (Use Case 3).

## Offene Punkte

Keine.

## Entschiedene Punkte

| Nr. | Thema | Entscheid |
|---|---|---|
| O1 | Profil ändern | Entschieden am 24.10.2026 (Mirko): Vorerst gibt es keine Maske zum Ändern von Name und Wohnadresse. Die Daten des Demo-Benutzers bleiben fest hinterlegt ([US 30004](../Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md)). |
| O2 | Speichervorgang mit Use Case 3 | Entschieden am 29.10.2026 (Mirko): Mirko baut `PUT /api/stellenanzeigen/<id>`. Die Route ruft bei jedem Speichern die bestehende Funktion `arbeitsweg_eintragen()` aus Use Case 3 unverändert auf, mit den gespeicherten Adressen der Stelle ([US 20003](20003-status-aendern.md)). Fabio wird informiert; den Stand von US 30003 führt er selbst nach. |
| O3 | Suche und Filter | Entschieden am 24.10.2026 (Mirko): Use Case 2 baut vorerst keine Suche und keinen Filter, wie in [ADR 0010](../../decisions/0010-minimale-oberflaeche.md) vorgeschlagen. |
