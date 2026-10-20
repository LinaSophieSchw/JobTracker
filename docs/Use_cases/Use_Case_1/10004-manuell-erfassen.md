# US 10004 – Angaben manuell bearbeiten und ergänzen

Status: Geplant – verpflichtender Bestandteil von Use Case 1

Datum: 2026-10-20

## User Story

Als Nutzerin möchte ich importierte Angaben manuell bearbeiten und fehlende
Angaben ergänzen können, damit ich eine korrekte Stellenanzeige speichern kann.
Auch bei einem fehlgeschlagenen Import soll eine manuelle Erfassung möglich sein.

## Ablauf

1. Nach dem Import das bearbeitbare Formular prüfen oder „Von Hand erfassen“ wählen.
2. Erkannte Werte korrigieren, fehlende Angaben ergänzen und den Link beibehalten.
3. Dasselbe Formular und dieselbe Speicherfunktion wie beim Import verwenden.

## Akzeptanzkriterien

- [ ] Manueller Einstieg ist direkt und nach einem Importfehler möglich.
- [ ] Alle fachlichen Importfelder sind nach der Vorschau manuell bearbeitbar.
- [ ] Bereits erkannte Werte bleiben beim Ergänzen anderer Felder erhalten.
- [ ] Bei manueller Neuerfassung ist die URL bearbeitbar; nach erfolgreicher Vorschau bleibt sie nur lesbar.
- [ ] Auch manuell werden nur die vereinbarten deutschen jobs.ch-Links akzeptiert.
- [ ] Titel und Firma müssen vor dem Speichern ergänzt werden.
- [ ] Alle übrigen fachlichen Eingabefelder können entsprechend dem Datenmodell gepflegt werden.
- [ ] Abbrechen erzeugt keinen Datensatz.
- [ ] Speichern nutzt die Prüfungen aus US 10003.

## Prüfung

Korrigieren erkannter Werte, Ergänzen fehlender Angaben, manuellen Einstieg,
vorausgefüllten Link und erfolgreichen beziehungsweise abgelehnten
Speicherversuch testen.

## Abgrenzung

Die manuelle Bearbeitung ist verpflichtend und wird bereits beim Formular
aus US 10002 berücksichtigt. US 10004 beschreibt zusätzlich den manuellen
Einstieg und den Umgang mit fehlgeschlagenem Import. Das Bearbeiten bereits
gespeicherter Einträge gehört zu Use Case 2 und ist hier nicht enthalten.

## Grundlagen

[US 10003](10003-stellenanzeige-speichern.md),
[ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md),
[ADR 0006](../../decisions/0006-import-nur-von-jobs-ch.md).
