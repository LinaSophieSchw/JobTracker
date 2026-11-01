# US 20004 – Weitere Angaben einer Stelle bearbeiten

Status: Umgesetzt

Datum: 2026-11-01

## User Story

Als Nutzer möchte ich die Angaben einer geöffneten Stelle ändern und speichern,
damit ich Fehler aus dem Import korrigieren und die Stelle aktuell halten kann.

## Umfang des Vertical Slice

Felder im Formular ändern → «Speichern» → Backend → PostgreSQL → Anzeige im
Formular und in der Übersicht.

Die Story erweitert den Speichervorgang aus
[US 20003](20003-status-aendern.md). Statt nur des Status speichert derselbe
`PUT` jetzt alle Felder des Formulars.

Gemeinsame Festlegungen für diesen Slice:

- Im Zustand «Bestehend» des Stellen-Formulars
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md))
  sind diese Felder änderbar: **Status, Titel, Firma, Arbeitsort, Strasse mit
  Hausnummer, Postleitzahl, Adressort, Pensum und Stellenbeschreibung.**
- Der Anzeigenlink (`url`) bleibt fest und wird nicht mitgeschickt.
- **Das Frontend schickt immer alle Felder** mit
  `PUT /api/stellenanzeigen/<id>`, auch die unveränderten. Das Backend
  überschreibt die ganze Stelle mit diesen Werten. Ein `PUT` mit nur
  `{"status": ...}` wie in US 20003 gibt es danach nicht mehr. Entschieden am
  01.11.2026 (Mirko), weil ein einziger, vollständiger Speichervorgang
  einfacher zu prüfen und zu testen ist als ein Speichern einzelner Felder.
- Das Backend prüft die Felder **gleich wie beim Erfassen** (Use Case 1):
  Titel und Firma sind Pflicht, die übrigen Textfelder dürfen leer sein, die
  Maximallängen gelten wie beim `POST`. Dazu kommt die Prüfung des Status aus
  US 20003. Ist etwas ungültig, antwortet es mit **400** und einer Meldung;
  nichts wird gespeichert.
- Gibt es keine Stelle mit dieser `id` beim Demo-Benutzer, antwortet es mit
  **404** (Regel B1).
- `geaendert_am` wird bei jedem Speichern neu gesetzt (Regel Z1).
- **Der Arbeitsweg wird bei jedem Speichern neu berechnet**, wie in US 20003,
  jetzt mit der eben gespeicherten Arbeitsadresse. Es gibt keinen Vergleich,
  ob sich die Adresse geändert hat. Entschieden am 01.11.2026 (Mirko), siehe
  O2 im [README](README.md).
- Nach dem Speichern bleibt das Formular offen und zeigt «Gespeichert.» sowie
  den Arbeitsweg oder den Hinweis «Arbeitsweg konnte nicht berechnet werden.»,
  wie in US 20003.

## Ablauf

1. Der Nutzer öffnet eine Stelle aus der Übersicht (US 20002).
2. Er ändert ein oder mehrere Felder und klickt auf «Speichern».
3. Das Frontend schickt `PUT /api/stellenanzeigen/<id>` mit allen Feldern
   des Formulars und dem Status.
4. Das Backend prüft die Werte, speichert sie bei der Stelle und setzt
   `geaendert_am`.
5. Es liest die Stelle mit ihren gespeicherten Adressen und berechnet den
   Arbeitsweg neu (`arbeitsweg_eintragen()`).
6. Es antwortet mit `id`, `status`, `fahrzeit_auto_in_minuten` und
   `strecke_auto_in_metern`.
7. Das Frontend zeigt den Arbeitsweg oder den Hinweis an. Zurück in der
   Übersicht erscheinen die geänderten Angaben.

## Akzeptanzkriterien

- [x] Im Zustand «Bestehend» lassen sich alle Felder ausser dem Anzeigenlink
      ändern.
- [x] Nach «Speichern» sind alle geänderten Felder in der Datenbank
      gespeichert; Titel, Firma, Arbeitsort und Status erscheinen geändert in
      der Übersicht.
- [x] Der Anzeigenlink bleibt unverändert.
- [x] `geaendert_am` ist nach dem Speichern neu gesetzt.
- [x] Ein leerer Titel oder eine leere Firma gibt 400 mit Meldung; nichts wird
      gespeichert.
- [x] Ein unbekannter Status gibt weiterhin 400 mit Meldung.
- [x] Eine unbekannte `id` oder eine Stelle eines anderen Benutzers gibt 404.
- [x] Nach einer Änderung der Arbeitsadresse wird der Arbeitsweg mit der neuen
      Adresse berechnet; das Ergebnis oder der Hinweis erscheint im Formular.
      Geprüft mit Unittest; im Browser noch offen, weil die Berechnung am
      01.11.2026 bei allen Stellen scheiterte (Fabio korrigiert, Use Case 3).
- [x] Scheitert die Berechnung, sind die Angaben trotzdem gespeichert.
- [x] Eine neue Stelle wird wie bisher mit `POST` gespeichert.
- [x] Unittests prüfen die Datenbankfunktion und die Route: Erfolg,
      fehlende Pflichtfelder, ungültiger Status, unbekannte Stelle.

## Schrittweise Umsetzung

1. **Datenbank:** In `datenbank.py` die Prüfung der Formularfelder so
   aufteilen, dass sie auch ohne `url` verwendet werden kann. Die Funktion aus
   US 20003 so erweitern, dass sie alle Felder und den Status speichert und
   `geaendert_am` setzt. Sie meldet weiterhin, ob eine Stelle gefunden wurde.
2. **Test:** Die Tests aus `tests/test_status_aendern.py` auf den
   vollständigen `PUT` anpassen und um fehlende Pflichtfelder ergänzen.
3. **Backend:** Die Route `PUT /api/stellenanzeigen/<id>` übergibt alle
   Angaben statt nur des Status. Der Rest (Stelle lesen, Arbeitsweg
   berechnen, antworten) bleibt gleich.
4. **Frontend:** In `public/index.html` schickt `stelle_aktualisieren()` alle
   Felder des Formulars mit, nicht nur den Status.

## Noch nicht enthalten

- Nach dem ersten Speichern einer neuen Stelle direkt in den Zustand
  «Bestehend» wechseln. Bleibt zurückgestellt (siehe US 20003), weil es das
  Speichern aus Use Case 1 und US 30006 ändert. Entschieden am 01.11.2026
  (Mirko): Diese Story bleibt so einfach wie möglich.
- Arbeitsweg nur neu berechnen, wenn sich die Adresse geändert hat.
- Ändern des Anzeigenlinks.
- Stelle löschen (US 20005).

## Technische Prüfung vor der Umsetzung

- `stellenanzeige_eingaben_pruefen()` aus Use Case 1 prüft heute alle Felder,
  verlangt aber auch die `url`. Für den `PUT` braucht es dieselbe Prüfung ohne
  `url`. Das Speichern neuer Stellen darf sich dadurch nicht ändern; die Tests
  aus Use Case 1 müssen weiter grün sein.
- Das Formular füllt beim Öffnen schon alle Felder (US 20002). Im Frontend
  muss nur der Inhalt des `PUT` erweitert werden.
- Das Formular und die Prüfung der Felder gehören zu Use Case 1. Den Pull
  Request prüft die verantwortliche Person von Use Case 1.
