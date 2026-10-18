# US 00001 – Stellenlink erfassen und Stellentitel speichern

Status: Geplant

Datum: 2026-10-18

## User Story

Als Nutzerin möchte ich einen Stellenlink einfügen und den erkannten
Stellentitel speichern, damit ich die Stelle in meiner Übersicht wiederfinde.

## Umfang des ersten Vertical Slice

Ein durchgängiger Ablauf vom Formular über das Flask-Backend zur lokalen
SQLite-Datenbank und zurück zur Übersicht. Zunächst werden nur jobs.ch-Links
unterstützt und nur Link und Stellentitel als fachliche Angaben gespeichert.
Der Eintrag dient der Verwaltung einer Stelle; es wird keine Bewerbung versendet.

## Ablauf

1. Im Frontend einen Link zu einer jobs.ch-Stellenanzeige einfügen.
2. Mit „Informationen laden“ den Abruf über das Flask-Backend auslösen.
3. Den erkannten Stellentitel anzeigen und vor dem Speichern korrigieren können.
4. Mit „Speichern“ den Link und den bestätigten Titel in SQLite ablegen.
5. Den gespeicherten Eintrag in der Übersicht anzeigen.

## Akzeptanzkriterien

- [ ] Ein Link zu einer jobs.ch-Stellenanzeige kann eingegeben werden.
- [ ] Unterstützt werden direkte Anzeigenlinks und Suchlinks mit einer `jobid`.
- [ ] „Informationen laden“ übernimmt den erkannten Stellentitel in ein
  bearbeitbares Feld; der Abruf allein speichert noch keinen Eintrag.
- [ ] Der Titel kann vor dem Speichern korrigiert werden.
- [ ] Link und bestätigter, nicht leerer Titel werden lokal in SQLite gespeichert.
- [ ] Der gespeicherte Eintrag erscheint mit Link und Titel in der Übersicht.
- [ ] Der Eintrag bleibt nach Neuladen der Seite und einem Serverneustart erhalten.
- [ ] Bei ungültigen oder nicht unterstützten Links, nicht erreichbaren Anzeigen
  oder fehlendem Titel erscheint eine verständliche Meldung. Es wird kein
  unvollständiger Eintrag automatisch gespeichert.

## Schrittweise Umsetzung

1. Den Python-Abruf und die Titelerkennung an einer konkreten Anzeige prüfen.
2. Linkfeld, Backend-Abruf und bearbeitbare Titelvorschau verbinden.
3. Datenbanktabelle und Speichern ergänzen.
4. Gespeicherte Einträge im Frontend anzeigen.
5. Erkennung, Fehlerbehandlung, Speichern und Abrufen automatisch testen.

## Noch nicht enthalten

- Automatische Übernahme von Firma und Arbeitsort oder weiteren Feldern.
- Unterstützung beliebiger Stellenportale.
- Google Maps, Scoring und zusätzliche Filter.
- Versenden von Bewerbungen oder Anmeldung bei Stellenportalen.
- Dauerhafte Online-Datenspeicherung auf Vercel; dieser Slice wird lokal geprüft.

## Technische Prüfung vor der Umsetzung

Der vorgesehene einfache Python-Abruf mit `requests` und `beautifulsoup4` muss
für die Beispielanzeige noch bestätigt werden. Falls die Seite so nicht
auslesbar ist, wird das weitere Vorgehen abgestimmt.

Beispielanzeige:
[jobs.ch – Helikopterpilotin / Helikopterpilot](https://www.jobs.ch/de/stellenangebote/detail/ac2fdcb3-f807-41b3-8914-d973ec426dd4/).

Die Links werden im Backend auf den unterstützten Anbieter geprüft; interne
oder lokale Zieladressen und Weiterleitungen dorthin dürfen nicht abgerufen
werden. Netzwerkaufrufe erhalten ein Zeitlimit. Automatische Tests verwenden
gespeicherte Beispieldaten oder simulierte Antworten statt Live-Abrufen.
