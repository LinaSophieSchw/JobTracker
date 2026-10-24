# US 30006 – Arbeitsweg im Stellen-Formular sehen

Status: Umgesetzt (Branch `feature/arbeitsweg-im-formular`)

Datum: 2026-10-24, umgesetzt 2026-10-24

Spickzettel zur Umsetzung: [30006-spickzettel.md](30006-spickzettel.md)

## User Story

Als Nutzer möchte ich Strecke und Fahrzeit nach dem Speichern direkt im Stellen-Formular in nur lesbaren Feldern sehen, damit ich den Arbeitsweg bei den übrigen Angaben der Stelle finde und nicht nur in einer kurzen Bestätigungsmeldung.

## Umfang des ersten Vertical Slice

Nach den Stories 30001 und 30002 werden die bereits berechneten und gespeicherten Werte an einem festen Ort im Formular angezeigt. Unter der Stellenbeschreibung erscheint ein Kasten «Arbeitsweg mit dem Auto» mit den Feldern **Strecke** und **Fahrzeit**. So sieht es auch [ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md) vor: Die Fahrzeit erscheint als nur lesbares Feld, das Use Case 3 liefert.

Gemeinsame Festlegungen für diesen Slice:

- Die Felder gehören zum Stellen-Formular von **Use Case 1**. Use Case 3 liefert nur die Werte. Die Änderung am Formular ist mit Lina (Use Case 1) abgesprochen (24.10.2026).
- Die beiden Felder sind **nur lesbar**. Der Nutzer kann sie nicht selbst ausfüllen.
- Berechnet wird weiterhin ausschliesslich beim Klick auf **«Speichern»** ([US 30001](30001-fahrzeit-beim-ersten-speichern.md)). Backend, Berechnung und Datenbank bleiben unverändert.
- **Gespeicherte Stellen können im Formular nicht bearbeitet werden.** Das Speichern legt immer eine neue Stelle an. Ist der Link schon gespeichert, bricht es ab. Das Bearbeiten gespeicherter Stellen gehört zu **Use Case 2**, die Neuberechnung dabei zu [US 30003](30003-arbeitsweg-beim-erneuten-speichern.md).
- Scheitert die Arbeitswegberechnung, bleiben beide Felder leer, und es erscheint ausschliesslich: **«Arbeitsweg konnte nicht berechnet werden.»**

## Ablauf

1. Der Nutzer lädt eine Stelle über den Link oder wählt «Von Hand erfassen». Der Kasten «Arbeitsweg» ist leer.
2. Er klickt auf «Speichern». Die Anwendung speichert die Stelle und berechnet den Arbeitsweg wie bisher.
3. Bei Erfolg stehen Strecke in Kilometern (z. B. «44.5 km») und Fahrzeit in Minuten (z. B. «44 min») im Kasten. Oben steht «Stellenanzeige gespeichert (ID: …).».
4. Scheitert die Berechnung, bleiben beide Felder leer, und an die Bestätigung wird «Arbeitsweg konnte nicht berechnet werden.» angehängt.
5. Das Formular bleibt nach dem Speichern offen, damit die Werte sichtbar sind.
6. Klickt der Nutzer nochmals auf «Speichern», wird nichts gespeichert und nichts neu berechnet. Es erscheint «Diese Stelle ist bereits gespeichert (ID: …) und kann hier nicht bearbeitet werden.». Die Werte im Kasten bleiben stehen.

## Akzeptanzkriterien

- [x] Unter der Stellenbeschreibung gibt es einen Kasten «Arbeitsweg mit dem Auto» mit den Feldern Strecke und Fahrzeit.
- [x] Beide Felder sind nur lesbar.
- [x] Vor dem ersten Speichern sind beide Felder leer, auch nach dem Laden einer weiteren Stelle oder nach «Von Hand erfassen».
- [x] Nach erfolgreichem Speichern zeigt der Kasten die Strecke in Kilometern mit einer Nachkommastelle und die Fahrzeit in Minuten.
- [x] Strecke und Fahrzeit stehen nicht mehr zusätzlich in der Bestätigungsmeldung.
- [x] Scheitert die Berechnung, bleiben beide Felder leer, und der vereinbarte Hinweis erscheint. Die Stelle bleibt gespeichert.
- [x] Das Formular bleibt nach dem Speichern sichtbar.
- [x] Ein erneuter Klick auf «Speichern» meldet, dass die Stelle bereits gespeichert ist und hier nicht bearbeitet werden kann. Die Werte im Kasten bleiben erhalten.
- [x] Backend, Berechnung und Datenbankschema bleiben unverändert, ausser dem Text der Meldung bei einem doppelten Link.

## Schrittweise Umsetzung

1. Frontend: Kasten mit zwei nur lesbaren Feldern und zwei neuen Anzeigewerten ergänzen. Beim Laden und bei «Von Hand erfassen» die Werte leeren.
2. Frontend: Nach dem Speichern die Werte aus der Antwort des Backends in den Kasten schreiben und das Formular offen lassen.
3. Backend: Die Meldung bei einem doppelten Link um «und kann hier nicht bearbeitet werden» ergänzen und den Unittest anpassen.
4. Im Browser prüfen: Erfolg, gescheiterte Berechnung, erneuter Klick auf «Speichern».

## Noch nicht enthalten

- Bearbeiten und erneutes Speichern gespeicherter Stellen; gehört zu Use Case 2.
- Neuberechnung beim erneuten Speichern; folgt in [US 30003](30003-arbeitsweg-beim-erneuten-speichern.md).
- Anzeige der gespeicherten Werte beim Öffnen einer bestehenden Stelle; gehört zur Detailansicht von Use Case 2.
- Nachträgliches Berechnen für Stellen, die ohne Arbeitsweg gespeichert wurden (z. B. Stelle 11).
- Sperren des Speichern-Buttons nach dem ersten Speichern; die Meldung genügt.
- Gestaltung mit CSS.

## Technische Prüfung vor der Umsetzung

### Befund vom 24.10.2026

| Frage | Befund |
|---|---|
| Liefert das Backend die Werte schon? | Ja. `POST /api/stellenanzeigen` antwortet mit `id`, `fahrzeit_auto_in_minuten` und `strecke_auto_in_metern` ([US 30002](30002-streckenlaenge-ergaenzen.md)). |
| Warum sah man die Werte nicht im Formular? | Sie wurden nur an die Bestätigung angehängt, und `vorschau_vorhanden = false` blendete das Formular nach dem Speichern aus. |
| Was passiert beim zweiten Klick? | `stellenanzeige_speichern()` findet den Link schon und bricht mit einer Meldung ab. Die Berechnung wird nicht erreicht. |
| Test im Browser | Fall «schon gespeichert» mit dem echten Backend und dem Link von Stelle 11. Erfolg (44522 m → «44.5 km», 44 → «44 min») und gescheiterte Berechnung mit simulierten Antworten, damit keine Testdaten in der Datenbank landen. |
| Unittests | `uv run pytest`: 39 bestanden. |
