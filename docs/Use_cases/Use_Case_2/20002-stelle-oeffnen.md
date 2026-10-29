# US 20002 – Stelle aus der Übersicht öffnen

Status: Umgesetzt

Datum: 2026-10-25

## User Story

Als Nutzer möchte ich eine Stelle aus der Übersicht öffnen, damit ich alle
gespeicherten Angaben zu dieser Stelle sehen kann.

## Umfang des Vertical Slice

Klick in der Übersicht → Backend → PostgreSQL → Anzeige im Stellen-Formular.
Die Story liest nur. Sie ändert keine Daten.

Gemeinsame Festlegungen für diesen Slice:

- Ein **Klick irgendwo auf eine Zeile** der Übersicht öffnet die Stelle. Es
  gibt keinen eigenen Knopf «Öffnen». Die Adresse im Browser ändert sich
  nicht. Entschieden am 25.10.2026 (Mirko).
- Die Stelle erscheint im bestehenden **Stellen-Formular im Zustand
  «Bestehend»** ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)).
  Es gibt keine eigene Detailansicht.
- Im Zustand «Bestehend» ist der Bereich zum Laden eines Links ausgeblendet.
  Das Feld `url` erscheint nur lesbar als **Link zur Anzeige**.
- Das Formular zeigt die Felder, die es heute schon hat: Titel, Firma,
  Arbeitsort, Arbeitsadresse, Pensum, Stellenbeschreibung sowie Strecke und
  Fahrzeit (nur lesbar, aus Use Case 3).
- In dieser Story gibt es im Zustand «Bestehend» **nur «← Zurück zur
  Übersicht»**. «Speichern» und «Löschen» bleiben ausgeblendet, bis US 20003
  und US 20005 sie bauen. Sonst würde «Speichern» die Stelle über den
  bestehenden Speichervorgang ein zweites Mal anlegen. Entschieden am
  25.10.2026 (Mirko).
- Es wird nur eine Stelle des Demo-Benutzers gelesen
  (`aktuelle_benutzer_id()`, Regel B1 im [Datenmodell](../../datenmodell.md)).
- Gibt es keine Stelle mit dieser `id` oder gehört sie einem anderen Benutzer,
  antwortet das Backend mit **404** und einer kurzen Fehlermeldung. Das
  Frontend bleibt in der Übersicht. Entschieden am 25.10.2026 (Mirko).

## Ablauf

1. Der Nutzer klickt in der Übersicht auf eine Zeile.
2. Das Frontend fragt `GET /api/stellenanzeigen/<id>` ab.
3. Das Backend liest die Stelle mit dieser `id` und der `benutzer_id` des
   Demo-Benutzers aus der Tabelle `stellenanzeigen`.
4. Es antwortet mit einem JSON-Objekt mit `id`, `url`, `titel`, `firma`,
   `arbeitsort`, `inseratadresse_strasse`, `inseratadresse_postleitzahl`,
   `inseratadresse_ort`, `pensum`, `stellenbeschreibung`, `status`,
   `strecke_auto_in_metern` und `fahrzeit_auto_in_minuten`.
5. Das Frontend füllt das Formular mit diesen Werten und zeigt es im Zustand
   «Bestehend» an.

`status` wird schon mitgeliefert, damit US 20003 die Antwort direkt verwenden
kann. Angezeigt wird er in dieser Story im Formular noch nicht.

## Akzeptanzkriterien

- [x] Ein Klick auf eine Zeile der Übersicht öffnet das Stellen-Formular mit
      den gespeicherten Angaben dieser Stelle.
- [x] `GET /api/stellenanzeigen/<id>` liefert die Stelle des Demo-Benutzers
      als JSON-Objekt mit den Feldern aus dem Ablauf.
- [x] Für eine unbekannte `id` oder eine Stelle eines anderen Benutzers
      antwortet das Backend mit 404 und einer Fehlermeldung.
- [x] Der Anzeigenlink erscheint nur lesbar als anklickbarer Link.
- [x] Der Bereich zum Laden eines Links ist im Zustand «Bestehend»
      ausgeblendet.
- [x] Strecke und Fahrzeit erscheinen wie nach dem Speichern, z.B. «12.5 km»
      und «18 min»; fehlen die Werte, bleiben die Felder leer. Angepasst am
      25.10.2026: Der Hinweis «Arbeitsweg konnte nicht berechnet werden»
      aus US 30006 gehört zum Speichern und erscheint beim Öffnen nicht.
- [x] Im Zustand «Bestehend» gibt es weder «Speichern» noch «Löschen».
- [x] «← Zurück zur Übersicht» führt zurück zur Übersicht.
- [x] «+ Neue Stelle» öffnet danach wieder ein leeres Formular.
- [x] Das Öffnen ändert keine Daten und löst keine Arbeitswegberechnung aus.
- [x] Unittests prüfen die Route mit einer gefundenen und einer nicht
      gefundenen Stelle.

## Schrittweise Umsetzung

1. **Datenbank:** In `datenbank.py` eine Funktion ergänzen, die eine Stelle
   über ihre `id` liest, nur für den Demo-Benutzer. Gibt es keine, liefert sie
   `None`.
2. **Backend:** In `stellenanzeigen_routes.py` die Route
   `GET /api/stellenanzeigen/<id>` ergänzen. Bei `None` antwortet sie mit 404.
   Im Browser direkt unter `/api/stellenanzeigen/1` prüfen.
3. **Test:** Unittests im Stil von `tests/test_stellenanzeigen_uebersicht.py`
   schreiben: Stelle gefunden, Stelle nicht gefunden.
4. **Frontend:** In `public/index.html` die Zeilen der Übersicht anklickbar
   machen und die Stelle laden, zuerst nur mit Titel und Firma im Formular.
5. **Frontend:** Die übrigen Felder füllen, den Link nur lesbar anzeigen und
   den Zustand «Bestehend» einführen: Linkbereich, «Speichern» und
   «Abbrechen» ausblenden.
6. **Frontend:** Prüfen, dass «+ Neue Stelle» danach wieder ein leeres
   Formular öffnet.

## Noch nicht enthalten

- Status im Formular anzeigen und ändern (US 20003).
- Lohn, Bewerbungsdatum und Notizen im Formular (US 20004).
- Weitere Angaben speichern (US 20004).
- Stelle löschen (US 20005).
- Eigene Adresse pro Stelle im Browser, z.B. `#/stelle/5`.
- Berechnung des Arbeitswegs (Use Case 3).

## Technische Prüfung vor der Umsetzung

- `public/index.html` verwendet Vue über CDN. Übersicht und Formular werden
  mit `v-if` / `v-else` umgeschaltet (US 20001). Den Zustand «Bestehend»
  bilden wir mit einer zusätzlichen Variable, z.B. der `id` der geöffneten
  Stelle. Ist sie gesetzt, ist das Formular im Zustand «Bestehend».
- Das Formular gehört zu Use Case 1
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)).
  Den Pull Request prüft die verantwortliche Person von Use Case 1.
- Die Tests in `tests/test_stellenanzeigen_uebersicht.py` ersetzen
  `verbindung_oeffnen` durch einen Mock. Die neuen Tests verwenden dasselbe
  Vorgehen, mit `fetchone` statt `fetchall`.
- Die Felder im Formular dürfen bearbeitbar bleiben. Weil es noch kein
  «Speichern» gibt, gehen Änderungen beim Zurückgehen verloren. Ab US 20003
  werden sie gespeichert.
