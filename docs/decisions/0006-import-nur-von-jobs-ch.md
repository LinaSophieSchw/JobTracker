# Import nur von jobs.ch über die Anzeigenseite

Datum: 2026-10-19

## Status

Angenommen

## Kontext

Use Case 1 soll Angaben aus einem Link lesen. Jedes Stellenportal ist anders
aufgebaut. Die User Story
[Stellenlink erfassen](../Use_cases/Use_Case_1/10001-stellenlink-erfassen.md)
liest bereits den Titel von jobs.ch. Ein Test von Mirko (Seitenquelltext mit
`Ctrl+U`) zeigte strukturierte Daten vom Typ `JobPosting` und jobs.ch-eigene
Ortsangaben mit den Feldern `street`, `postalCode` und `city`. Ein Feld
`streetAddress` nach dem Standard schema.org wurde nicht gefunden.

## Betrachtete Optionen

- **Option 1: Mehrere Portale.** Grösserer Nutzen, aber pro Portal ein eigener
  Leser und eigene Tests.
- **Option 2: Allgemeiner Leser für `JobPosting`.** Funktioniert auf vielen
  Seiten. Auf jobs.ch fehlt darin aber die Strasse, also nur ein Teil der
  Angaben.
- **Option 3: Nur jobs.ch.** Ein Leser, testbar mit gespeicherten Seiten.
- **Option 4: Kein Import, nur manuell.** Einfach, aber der Kernnutzen von
  Use Case 1 fehlt.

## Entscheidung

Option 3: nur jobs.ch. Akzeptiert werden Anzeigenlinks und Suchlinks mit
`jobid`; abgerufen wird immer der Anzeigenlink. Auch die manuelle Erfassung
akzeptiert nur jobs.ch-Links. Entschieden von Mirko am 17. und 19.10.2026,
abgestimmt mit der User Story «Stellenlink erfassen».

## Begründung

Ein Portal genügt für den Zweck der Semesterarbeit, und jobs.ch ist in der
Schweiz verbreitet. Ein einziger Leser bleibt für Anfänger überschaubar und mit
gespeicherten Seiten testbar.

## Konsequenzen

- Ändert jobs.ch den Seitenaufbau, liefert der Import weniger Angaben. Die
  manuelle Erfassung bleibt möglich.
- Die Adresse stammt aus jobs.ch-eigenen Daten, nicht aus einem Standard. Sie
  kann sich ohne Ankündigung ändern.
- Die Seite enthält auch Daten anderer Stellen. Der Import verwendet nur Daten
  der eigenen jobid (Regel I1 im [Datenmodell](../datenmodell.md)).
- Die robots.txt von jobs.ch sperrt für Crawler Pfade nach dem Muster
  `/de/stellenangebote/detail/*/*/*`. Der Anzeigenlink mit nur der jobid fällt
  nach unserer Lesart nicht darunter; ein Werkzeug, das robots.txt beachtet,
  konnte die Seite am 19.10.2026 abrufen. Wir rufen nur einzelne Anzeigen auf
  Knopfdruck ab und crawlen nicht. Die Nutzungsbedingungen von jobs.ch wurden
  nicht geprüft. Bewusst eingegangenes Risiko.
- Auf Vercel kommen die Abrufe standardmässig aus den USA. Früh mit einem
  deployten Abruf prüfen.
- Französische und englische jobs.ch-Links werden abgelehnt.
- Tests rufen jobs.ch nie live ab, sondern verwenden gespeicherte Seiten aus
  `tests/fixtures/`.
