# US 20005 – Stelle löschen

Status: Umgesetzt

Datum: 2026-11-01

## User Story

Als Nutzer möchte ich eine geöffnete Stelle löschen, damit Stellen, die mich
nicht mehr interessieren, aus meiner Übersicht verschwinden.

## Umfang des Vertical Slice

«Löschen» im Formular → Rückfrage → Backend → PostgreSQL → zurück zur
Übersicht ohne die gelöschte Stelle.

Gemeinsame Festlegungen für diesen Slice:

- Im Zustand «Bestehend» des Stellen-Formulars
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md))
  erscheint neben «Speichern» die Schaltfläche **«Löschen»**. Eine neue Stelle
  hat keine Schaltfläche «Löschen».
- Vor dem Löschen fragt die Oberfläche mit dem Browser-Dialog `confirm()`
  nach: «Stelle wirklich löschen?» mit «OK» und «Abbrechen»
  ([ADR 0010](../../decisions/0010-minimale-oberflaeche.md)). Bei
  «Abbrechen» passiert nichts. Entschieden am 01.11.2026 (Mirko), weil eine
  Zeile JavaScript genügt und es zur minimalen Oberfläche passt.
- Das Frontend schickt `DELETE /api/stellenanzeigen/<id>` ohne Inhalt.
- **Die Stelle wird endgültig gelöscht.** Das Backend entfernt die Zeile mit
  `DELETE` aus der Tabelle `stellenanzeigen`. Es gibt keinen Papierkorb und
  kein Wiederherstellen. Wer eine Stelle nur abschliessen will, wählt den
  Status «Zurückgezogen» oder «Absage». Entschieden am 01.11.2026 (Mirko),
  weil «nur ausblenden» eine neue Spalte und Änderungen an Übersicht und
  Öffnen bräuchte.
- Es wird nur eine Stelle des Demo-Benutzers gelöscht (Regel B1). Gibt es
  keine Stelle mit dieser `id` beim Demo-Benutzer, antwortet das Backend mit
  **404** und einer kurzen Fehlermeldung.
- Bei Erfolg antwortet das Backend mit **204 «No Content»** ohne Inhalt.
  Entschieden am 01.11.2026 (Mirko), weil es nach dem Löschen nichts mehr
  zurückzugeben gibt.
- **Nach dem Löschen wechselt die Oberfläche zur Übersicht** und lädt sie neu.
  Die gelöschte Stelle erscheint dort nicht mehr. Entschieden am 01.11.2026
  (Mirko), weil das Formular sonst eine Stelle zeigen würde, die es nicht mehr
  gibt.
- Scheitert das Löschen, bleibt das Formular offen und zeigt die
  Fehlermeldung.

## Ablauf

1. Der Nutzer öffnet eine Stelle aus der Übersicht (US 20002).
2. Er klickt auf «Löschen» und bestätigt die Rückfrage mit «OK».
3. Das Frontend schickt `DELETE /api/stellenanzeigen/<id>`.
4. Das Backend löscht die Stelle mit dieser `id` und der `benutzer_id` des
   Demo-Benutzers aus der Tabelle `stellenanzeigen`.
5. Es antwortet mit 204 ohne Inhalt.
6. Das Frontend wechselt zur Übersicht und lädt sie neu.

## Akzeptanzkriterien

- [x] Im Zustand «Bestehend» erscheint «Löschen»; bei einer neuen Stelle
      nicht.
- [x] Vor dem Löschen erscheint die Rückfrage; «Abbrechen» löscht nichts.
- [x] Nach «OK» ist die Stelle aus der Datenbank entfernt, und die Übersicht
      erscheint ohne sie.
- [x] Ein erfolgreiches `DELETE` gibt 204 ohne Inhalt.
- [x] Eine unbekannte `id` oder eine Stelle eines anderen Benutzers gibt 404;
      nichts wird gelöscht.
- [x] Ist die Datenbank nicht erreichbar, erscheint eine kurze Meldung ohne
      technische Details (503).
- [x] Unittests prüfen die Datenbankfunktion und die Route: Erfolg, unbekannte
      Stelle, Datenbankfehler.

## Schrittweise Umsetzung

1. **Datenbank:** In `datenbank.py` eine Funktion ergänzen, die eine Stelle
   des Demo-Benutzers löscht. Sie meldet wie `stellenanzeige_aktualisieren()`
   mit `rowcount`, ob eine Stelle gefunden wurde.
2. **Backend:** In `stellenanzeigen_routes.py` die Route
   `DELETE /api/stellenanzeigen/<id>` ergänzen.
3. **Test:** Unittests im Stil von `tests/test_status_aendern.py`.
4. **Frontend:** In `public/index.html` «Löschen» im Zustand «Bestehend»
   einblenden, mit `confirm()` nachfragen, `DELETE` schicken und danach zur
   Übersicht wechseln.

## Noch nicht enthalten

- Gelöschte Stellen wiederherstellen (Papierkorb).
- Mehrere Stellen auf einmal löschen.
- Löschen direkt aus der Übersicht.

## Technische Prüfung vor der Umsetzung

- Die Tabelle `stellenanzeigen` wird von keiner anderen Tabelle referenziert.
  Ein `DELETE` scheitert darum nicht an einem Fremdschlüssel.
- Der Arbeitsweg (Use Case 3) ist in derselben Zeile gespeichert und
  verschwindet mit ihr. Use Case 3 ist nicht betroffen.
- Bei 204 schickt das Backend keinen Inhalt. Das Frontend darf darum bei
  Erfolg nicht `antwort.json()` lesen, sonst entsteht ein Fehler.
- Das Formular gehört zu Use Case 1. Den Pull Request prüft die
  verantwortliche Person von Use Case 1.
