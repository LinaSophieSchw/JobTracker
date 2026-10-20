# US 10001 – Stellenlink einfügen und Stellentitel prüfen

Status: Umgesetzt (Titelvorschau; keine Speicherung)

Datum: 2026-10-20

## User Story

Als Nutzerin möchte ich einen jobs.ch-Stellenlink einfügen und den erkannten
Stellentitel sehen und korrigieren können, damit ich die Erkennung prüfen kann.

## Umfang

Erster kleiner Ablauf vom Linkfeld über das Backend zurück zur bearbeitbaren
Vorschau. Als fachliche Angabe wird zunächst nur der Titel ausgelesen.
Die frühere Story US 00001 wird hier auf den tatsächlich umgesetzten Umfang
begrenzt. Speicherung folgt separat in [US 10003](10003-stellenanzeige-speichern.md).

## Ablauf

1. Einen deutschen jobs.ch-Anzeigenlink oder Suchlink mit jobid einfügen.
2. „Informationen laden“ anklicken.
3. Den erkannten Titel anzeigen und bei Bedarf korrigieren.

## Akzeptanzkriterien

- [x] Ein jobs.ch-Link kann eingegeben werden.
- [x] Anzeigenlinks und Suchlinks mit einer gültigen jobid werden unterstützt.
- [x] Der Titel wird aus der Anzeige gelesen und im Formular angezeigt.
- [x] Der angezeigte Titel kann vor einer späteren Speicherung geändert werden.
- [x] Ein ungültiger Link oder ein fehlender Titel führt zu einer Fehlermeldung.
- [x] Der Vorschauabruf speichert keine Stellenanzeige.

## Prüfung und Nachweise

Die Titelvorschau wurde lokal und auf Vercel manuell bestätigt.
Automatische Tests für Titelerkennung, Linkprüfung und Vorschau sind vorhanden.
Die PostgreSQL-Verbindungsprüfung ist ein technischer Zwischenstand und
beweist noch keine Speicherung einer Stellenanzeige.

## Noch nicht enthalten

Weitere Felder, Speichern, Übersicht und Bearbeiten bestehender Einträge.

## Grundlagen

[Datenmodell](../../datenmodell.md), insbesondere Abschnitt 9, und
[ADR 0006](../../decisions/0006-import-nur-von-jobs-ch.md).
