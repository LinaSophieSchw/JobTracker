# Use Case 1 – Stellenanzeigen erfassen

Stand: 2026-11-17

**Status:** Implementiert

## Ziel

Die Nutzerin übernimmt eine Stellenanzeige über einen jobs.ch-Link, prüft die
erkannten Angaben, ergänzt oder korrigiert sie und speichert die Stelle.
Alternativ erfasst sie die Angaben von Hand. Beide Wege verwenden dasselbe
Formular und dieselbe Speicherfunktion.

## User Stories

| Reihenfolge | User Story | Endpunkt | Stand im Code |
|---|---|---|---|
| 1 | [US 10001 – Stellenlink einfügen und Stellentitel prüfen](10001-stellenlink-erfassen.md) | `POST /api/stellenanzeigen/vorschau` | Implementiert; Grundlage der erweiterten Vorschau |
| 2 | [US 10002 – Weitere Anzeigenfelder laden und bearbeiten](10002-weitere-felder-vorschauen.md) | derselbe Vorschau-Endpunkt, erweitert | Implementiert |
| 3 | [US 10003 – Geprüfte Stellenanzeige in PostgreSQL speichern](10003-stellenanzeige-speichern.md) | `POST /api/stellenanzeigen` | Implementiert |
| 4 | [US 10004 – Angaben manuell bearbeiten und ergänzen](10004-manuell-erfassen.md) | dieselbe Speicherroute; kein eigener Importaufruf beim manuellen Einstieg | Implementiert |

Die Stories erweitern den Ablauf schrittweise: zuerst Titelvorschau, dann
weitere Felder, anschliessend Speicherung und der zusätzliche manuelle
Einstieg. Eine Vorschau allein legt noch keinen Datenbankeintrag an.

## Ablauf

1. In der Übersicht «+ Neue Stelle» wählen.
2. Einen unterstützten jobs.ch-Link einfügen und «Informationen laden» wählen
   oder über «Von Hand erfassen» direkt das leere Formular öffnen.
3. Die Angaben im Formular prüfen, korrigieren und ergänzen.
4. «Speichern» übermittelt die Formularwerte an das Flask-Backend.
5. Das Backend prüft die Werte, bestimmt den Demo-Benutzer und speichert die
   Stelle in PostgreSQL. Ein bereits gespeicherter Link wird abgelehnt.
6. Nach dem Anlegen ergänzt Use Case 3 den Arbeitsweg, soweit berechenbar.
   Die Oberfläche zeigt die neue ID und den Arbeitsweg beziehungsweise den
   Hinweis zur fehlgeschlagenen Berechnung. Das Formular bleibt offen.

«Abbrechen» verwirft eine ungespeicherte Erfassung. Über «← Zurück zur
Übersicht» wird die Liste neu geladen; deren Darstellung gehört zu Use Case 2.

## Oberfläche und Angaben

Das Stellen-Formular wird auch von Use Case 2 verwendet
([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)).
Beim Import bleibt der normalisierte Anzeigenlink nur lesbar. Bei der
manuellen Neuerfassung ist er bearbeitbar; ein zuvor eingegebener Link wird
übernommen.

Bearbeitbar sind Titel, Firma, Arbeitsort, Pensum und Stellenbeschreibung
sowie die drei Felder der Arbeitsadresse:

- `inseratadresse_strasse`: Strasse mit Hausnummer
- `inseratadresse_postleitzahl`: Postleitzahl
- `inseratadresse_ort`: Ort der Adresse

Arbeitsort und genaue Arbeitsadresse bleiben getrennt. Der Arbeitsort kann
mehrere Ortsnamen enthalten; die Adresse dient der Arbeitswegberechnung.
Fahrzeit und Strecke werden nur angezeigt, nicht von Hand eingegeben.

## Regeln

- Importiert werden nur unterstützte deutsche HTTPS-Links von `www.jobs.ch`:
  Anzeigenlinks und Suchlinks mit gültiger `jobid`. Auch manuell erfasste
  Stellen benötigen einen unterstützten Link
  ([ADR 0006](../../decisions/0006-import-nur-von-jobs-ch.md)).
- Beim Import werden strukturierte Anzeigendaten der passenden Stellen-ID
  zugeordnet. Fehlende optionale Angaben bleiben leer. Die Beschreibung wird
  als Text ohne ausführbares HTML übernommen.
- Beim Speichern sind Link, Titel und Firma Pflicht. Das Backend prüft
  Texttypen und Maximallängen und normalisiert den Link.
- Die drei Adressfelder sind optional. Es gibt keine Prüfung auf ein
  bestimmtes Adressformat; Texttyp und Maximallängen werden dennoch geprüft.
- Der Benutzer wird serverseitig bestimmt. Version 1 verwendet den
  gemeinsamen Demo-Benutzer mit `id` 1, ohne Login.
- Pro Benutzer darf derselbe normalisierte Anzeigenlink nur einmal bestehen.
  Bei einem Duplikat erscheint ein Hinweis mit der vorhandenen ID.
- Neue Stellen erhalten den Status `gespeichert`. Gespeicherte Anzeigen
  werden über Use Case 2 weiter bearbeitet, nicht erneut als neue Stelle angelegt.

## Voraussetzungen

- Eingerichtete PostgreSQL-Datenbank bei Neon mit den Tabellen `benutzer`
  und `stellenanzeigen` gemäss [Datenmodell](../../datenmodell.md).
- Hinterlegter Demo-Benutzer aus
  [US 30004](../Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md).
- Konfigurierte `DATABASE_URL`. Für einen erfolgreichen Import muss jobs.ch
  erreichbar sein; der manuelle Einstieg benötigt keinen Vorschauabruf.
- Für die zusätzliche Arbeitswegberechnung: `OPENROUTESERVICE_API_KEY` und
  geeignete Adressen. Ein fehlendes Routenergebnis verhindert das vorherige
  Anlegen der Stelle nicht.

## Abgrenzung

| Was | Wo |
|---|---|
| Link prüfen, Vorschau importieren, manuell erfassen und neue Stelle speichern | Use Case 1 |
| Gemeinsames Stellen-Formular und Arbeitsadressfelder | Use Case 1; Wiederverwendung durch Use Case 2 |
| Übersicht, bestehende Stellen öffnen, ändern und löschen | [Use Case 2](../Use_Case_2/README.md) |
| Demo-Wohnadresse, Arbeitsweg berechnen und Ergebniswerte ergänzen | [Use Case 3](../Use_Case_3/README.md) |

Nicht enthalten sind andere Stellenportale, automatische Lohnerkennung,
Login und persönliche Profile, das Versenden einer Bewerbung sowie eine
Bewertung durch einen Fit-Score.

## Umsetzung und Prüfung

- [Frontend](../../../public/index.html): Vorschau, manuelle Erfassung und
  Übermittlung der Formularwerte mit Vue und JavaScript.
- [Import](../../../src/app/stellenanzeige_erfassen.py): Linkprüfung,
  Abruf und Auslesen der Anzeige.
- [Flask-Routen](../../../src/app/stellenanzeigen_routes.py): Vorschau und
  Anlegen einer Stelle; anschliessender Aufruf der Arbeitswegberechnung.
- [Datenbank](../../../src/app/datenbank.py): Eingabeprüfung und Speicherung.
- [Importtests](../../../tests/test_stellenanzeige.py) und
  [Speichertests](../../../tests/test_stellenanzeige_speichern.py): unter
  anderem Linknormalisierung, Zuordnung, Felder, Pflichtangaben, Duplikate
  und Fehlerantworten. Externe Zugriffe werden simuliert.

Start und Testausführung sind im [Projekt-README](../../../README.md)
beschrieben. Mock-Tests allein beweisen keine dauerhafte Online-Speicherung.

## Noch nachzuführen

- US 10002 und US 10004 tragen noch den früheren Planungsstatus. US 10002
  beschreibt ausserdem noch ein gemeinsames Adressfeld. Diese Übersicht
  beschreibt bereits die implementierten drei Adressfelder; die einzelnen
  Story-Dokumente sind entsprechend nachzuführen.
