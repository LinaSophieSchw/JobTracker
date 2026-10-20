# Use Case 1 – Stellenanzeige erfassen

Stand: 2026-10-20

Die Stories teilen den bisherigen grossen Ablauf in einzeln prüfbare Schritte.
Grundlage ist [Mirkos Datenmodell](../../datenmodell.md).
Die ergänzenden Abläufe sind daraus und aus den Entscheidungsdokumenten
abgeleitet. Alle vier aufgeführten Stories gehören zum geplanten Pflichtumfang.

| Reihenfolge | User Story | Stand |
|---|---|---|
| 1 | [US 10001 – Titelvorschau](10001-stellenlink-erfassen.md) | Umgesetzt; ohne Speichern |
| 2 | [US 10002 – Weitere Felder laden und bearbeiten](10002-weitere-felder-vorschauen.md) | Geplant |
| 3 | [US 10003 – In PostgreSQL speichern](10003-stellenanzeige-speichern.md) | Geplant |
| 4, teilweise bereits mit US 10002 | [US 10004 – Manuell bearbeiten und ergänzen](10004-manuell-erfassen.md) | Geplant; verpflichtend |

Die zuvor vorgeschlagenen Stories 10005 und 10006 wurden auf Wunsch vorerst
entfernt. Die zugehörigen Felder und Regeln im Datenmodell bleiben bestehen;
die Verwaltung bereits gespeicherter Einträge wird mit Use Case 2 abgestimmt.

## Bearbeitbare Angaben und feste Felder

Importiert werden nach Prüfung der Verfügbarkeit:
Titel, Firma, Arbeitsort, Adresse, Pensum und Stellenbeschreibung.
Alle diese Angaben sind im Vorschauformular bearbeitbar.
Fehlende Angaben bleiben leer und können ergänzt werden.

Lohn, Status, Bewerbungsdatum und Notizen sind manuelle Angaben.
IDs, Benutzerzuordnung und Zeitstempel setzt das System.
Fahrzeit kommt gegebenenfalls aus Use Case 3 und ist nicht bearbeitbar.
Die URL bleibt nach erfolgreicher Vorschau und bei bestehenden Einträgen
gemäss ADR 0005 nur lesbar; bei manueller Neuerfassung ist sie bearbeitbar.

## Offene technische Punkte

Die konkrete Erkennung aller zusätzlichen Felder ist noch nachzuweisen.
Speichern und erneut Lesen in PostgreSQL sind noch nicht implementiert.
Der erfolgreiche Datenbankstatus bestätigt nur die Verbindung.
Die SQLite-spezifischen Einrichtungs- und Schemaänderungshinweise in
docs/datenmodell.md müssen vor der Speicherumsetzung mit PostgreSQL
abgeglichen und nachgeführt werden. Diese Story-Aufteilung ändert das
vereinbarte Datenmodell nicht.
