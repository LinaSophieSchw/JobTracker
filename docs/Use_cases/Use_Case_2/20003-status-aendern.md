# US 20003 – Status einer Stelle ändern

Status: In Arbeit

Datum: 2026-10-29

## User Story

Als Nutzer möchte ich den Status einer geöffneten Stelle ändern und speichern,
damit ich sehe, wie weit meine Bewerbung ist.

## Umfang des Vertical Slice

Status im Formular wählen → «Speichern» → Backend → PostgreSQL → Anzeige im
Formular und in der Übersicht.
Die Story ändert nur den `status` einer bestehenden Stelle. Alle anderen
Felder bleiben unverändert.

Gemeinsame Festlegungen für diesen Slice:

- Im Zustand «Bestehend» des Stellen-Formulars
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md))
  erscheinen ein **Dropdown «Status»** und wieder **«Speichern»**. Das
  Dropdown zeigt die Anzeigetexte aus Abschnitt 5 im
  [Datenmodell](../../datenmodell.md), z.B. «Vorstellungsgespräch» für
  `interview`.
- Eine **neue Stelle** hat kein Dropdown. Sie startet immer mit
  `gespeichert`.
- Das Frontend schickt `PUT /api/stellenanzeigen/<id>` mit nur
  `{"status": "<wert>"}`.
- Das Backend prüft den Wert. Ist er keiner der sechs erlaubten Status,
  antwortet es mit **400** und einer Meldung. Gibt es keine Stelle mit dieser
  `id` beim Demo-Benutzer, antwortet es mit **404** (Regel B1).
- `geaendert_am` wird auch bei einer reinen Statusänderung neu gesetzt
  (Regel Z1).
- **Bei jedem Speichern wird der Arbeitsweg neu berechnet.** Der `PUT` ruft
  dafür die bestehende Funktion `arbeitsweg_eintragen()` aus Use Case 3
  unverändert auf, mit den gespeicherten Adressen der Stelle. So wird eine
  früher gescheiterte Berechnung wiederholt
  ([US 30003](../Use_Case_3/30003-arbeitsweg-beim-erneuten-speichern.md)).
  Entschieden am 29.10.2026 (Mirko), siehe O2 im [README](README.md).
- **Nach dem Speichern bleibt das Formular offen.** Der Arbeitsweg-Kasten
  zeigt die neuen Werte, oder es erscheint der Hinweis «Arbeitsweg konnte
  nicht berechnet werden.». Wie bei neuen Stellen (US 20001, US 30006);
  ersetzt für bestehende Stellen den Plan «nach dem Speichern zur Übersicht».
  Entschieden am 29.10.2026 (Mirko).

## Ablauf

1. Der Nutzer öffnet eine Stelle aus der Übersicht (US 20002).
2. Er wählt im Dropdown einen neuen Status und klickt auf «Speichern».
3. Das Frontend schickt `PUT /api/stellenanzeigen/<id>` mit `{"status": ...}`.
4. Das Backend prüft den Status, speichert ihn bei der Stelle und setzt
   `geaendert_am`.
5. Es liest die Stelle mit ihren gespeicherten Adressen und berechnet den
   Arbeitsweg neu (`arbeitsweg_eintragen()`).
6. Es antwortet mit `id`, `status`, `fahrzeit_auto_in_minuten` und
   `strecke_auto_in_metern`.
7. Das Frontend zeigt den Arbeitsweg oder den Hinweis an. Zurück in der
   Übersicht erscheint der neue Status.

## Akzeptanzkriterien

- [ ] Im Zustand «Bestehend» zeigt das Dropdown den gespeicherten Status der
      Stelle.
- [ ] Nach «Speichern» ist der neue Status in der Datenbank gespeichert und
      erscheint in der Übersicht.
- [ ] `geaendert_am` ist nach dem Speichern neu gesetzt.
- [ ] Ein unbekannter Status gibt 400 mit Meldung; nichts wird gespeichert.
- [ ] Eine unbekannte `id` oder eine Stelle eines anderen Benutzers gibt 404.
- [ ] Jedes Speichern berechnet den Arbeitsweg neu; das Ergebnis oder der
      Hinweis erscheint im Formular.
- [ ] Scheitert die Berechnung, ist der Status trotzdem gespeichert.
- [ ] Eine neue Stelle zeigt kein Dropdown und wird wie bisher mit `POST`
      gespeichert.
- [ ] Unittests prüfen die Datenbankfunktion und die Route: Erfolg,
      ungültiger Status, unbekannte Stelle.

## Schrittweise Umsetzung

1. **Datenbank:** In `datenbank.py` eine Funktion ergänzen, die den Status
   einer Stelle des Demo-Benutzers ändert und `geaendert_am` setzt. Sie meldet,
   ob eine Stelle gefunden wurde.
2. **Backend:** In `stellenanzeigen_routes.py` die Route
   `PUT /api/stellenanzeigen/<id>` ergänzen: Status prüfen, speichern, Stelle
   lesen, `arbeitsweg_eintragen()` aufrufen, antworten.
3. **Test:** Unittests im Stil von `tests/test_stellenanzeige_oeffnen.py`.
4. **Frontend:** In `public/index.html` das Dropdown im Zustand «Bestehend»
   ergänzen und beim Öffnen mit dem gespeicherten Status füllen.
5. **Frontend:** «Speichern» im Zustand «Bestehend» wieder einblenden und dort
   den `PUT` schicken; Arbeitsweg oder Hinweis anzeigen.

## Noch nicht enthalten

- Weitere Felder ändern, auch die Arbeitsadresse (US 20004). Dann speichert
  derselbe `PUT` auch die Adresse, und die Neuberechnung verwendet sie.
- Nach dem ersten Speichern einer neuen Stelle direkt in den Zustand
  «Bestehend» wechseln (im Frontend `geoeffnete_stelle_id = daten.id` nach
  dem `POST`). Heute erscheint das Dropdown erst nach «← Zurück zur
  Übersicht» und erneutem Öffnen; ein zweites «Speichern» meldet, dass die
  Stelle schon existiert (US 30006). Bewusst zurückgestellt am 29.10.2026
  (Mirko), weil es das Speichern neuer Stellen aus Use Case 1 und US 30006
  ändert. Idee für US 20004, mit Use Case 1 und Use Case 3 absprechen.
- Status direkt in der Übersicht ändern.
- Verlauf der Statusänderungen.
- Stelle löschen (US 20005).

## Technische Prüfung vor der Umsetzung

- `arbeitsweg_eintragen(stellen_id, daten)` liest aus `daten` nur
  `inseratadresse_strasse`, `inseratadresse_postleitzahl` und
  `inseratadresse_ort`. `stellenanzeige_mit_id_lesen()` aus US 20002 liefert
  diese Felder mit denselben Namen. Darum kann der `PUT` die gelesene Stelle
  direkt übergeben, ohne Änderung an Use Case 3.
- Die Tabelle prüft den Status schon mit `CHECK`. Das Backend prüft ihn
  trotzdem vorher, damit der Browser eine verständliche Meldung statt eines
  Datenbankfehlers erhält.
- Das Formular gehört zu Use Case 1. Den Pull Request prüft die
  verantwortliche Person von Use Case 1.
