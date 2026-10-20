# US 10002 – Weitere Anzeigenfelder laden und bearbeiten

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzerin möchte ich nach dem Einfügen eines Stellenlinks alle vorgesehenen
Importangaben in einem bearbeitbaren Formular sehen, damit ich sie prüfen,
korrigieren und fehlende Angaben ergänzen kann.

## Umfang

Erweitert die Titelvorschau aus [US 10001](10001-stellenlink-erfassen.md).
Die Vorschau speichert noch nichts. Die konkrete Auslesbarkeit wird vor der
Implementierung mit passenden Anzeigen und gespeicherten Beispieldaten geprüft.

## Felder

| Feld | Verhalten |
|---|---|
| titel | Bereits erkannt; bearbeitbar, Pflichtfeld beim Speichern |
| firma | Auslesen, wenn vorhanden; bearbeitbar, Pflichtfeld beim Speichern |
| arbeitsort | Ortsnamen; mehrere Orte durch Komma getrennt; bearbeitbar |
| adresse | Erster zur Anzeige gehörender Ort mit Strasse; Format „Strasse Nr, PLZ Ort“; bearbeitbar |
| pensum | Text wie „60–100 %“; bearbeitbar |
| stellenbeschreibung | Reiner Text mit Absätzen; grosses bearbeitbares Textfeld |

Der normalisierte Link wird angezeigt und ist nach erfolgreicher Vorschau
gemäss ADR 0005 nur lesbar. Ein anderer Import wird über das Linkfeld gestartet.
IDs, Benutzerbezug, Zeitstempel und Fahrzeit sind keine editierbaren Importfelder.

## Ablauf

1. Unterstützten Link einfügen und Vorschau anfordern.
2. Backend liest nur Daten der passenden jobid.
3. Formular zeigt erkannte Werte und leere Felder für fehlende Angaben.
4. Nutzerin korrigiert oder ergänzt Werte.
5. Abbrechen verwirft die ungespeicherte Vorschau.

## Akzeptanzkriterien

- [ ] Alle sechs Importfelder werden nach dem Abruf angezeigt und sind bearbeitbar.
- [ ] Fehlende Einzelangaben bleiben leer; es werden keine Inhalte erfunden.
- [ ] Daten anderer Stellen auf derselben Seite werden nicht übernommen.
- [ ] Arbeitsort und vollständige Adresse werden getrennt behandelt.
- [ ] Ohne Strasse bleibt die importierte Adresse leer.
- [ ] Die Stellenbeschreibung enthält Text und Absatzumbrüche, kein ausführbares HTML.
- [ ] Ladezustand und Abruffehler werden verständlich angezeigt.
- [ ] Fehlende Pflichtangaben können vor dem späteren Speichern ergänzt werden.
- [ ] Der Abruf allein schreibt keine Daten in die Datenbank.

## Schrittweise Umsetzung und Prüfung

Firma, Arbeitsort/Adresse, Pensum und Beschreibung nacheinander auslesen.
Gespeicherte Beispiele prüfen vollständige, unvollständige und mehrere
Ortsangaben sowie fremde Stellenempfehlungen auf derselben Seite.
Automatische Tests verwenden keine Live-Abrufe. Browserprüfung mit editierbaren Feldern.

## Noch nicht enthalten

Datenbank-Speicherung, automatische Lohnerkennung und Fahrzeitberechnung.

## Grundlagen

[Datenmodell](../../datenmodell.md), Regeln S3, S4, A1 und I1/I2;
[ADR 0004](../../decisions/0004-adresse-getrennt-vom-arbeitsort.md),
[ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md),
[ADR 0006](../../decisions/0006-import-nur-von-jobs-ch.md).
