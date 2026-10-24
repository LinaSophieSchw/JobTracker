# US 20001 – Übersicht aller Stellen sehen

Status: Umgesetzt

Datum: 2026-10-24

## User Story

Als Nutzer möchte ich beim Öffnen der Anwendung alle erfassten Stellen in einer
Liste sehen, damit ich den Überblick über meine Stellen und den Stand meiner
Bewerbungen behalte.

## Umfang des ersten Vertical Slice

Frontend → Backend → PostgreSQL → Anzeige der Liste.
Die Story liest nur. Sie ändert keine Daten.

Gemeinsame Festlegungen für diesen Slice:

- Die Übersicht ist die **Startseite** der Anwendung
  ([ADR 0010](../../decisions/0010-minimale-oberflaeche.md)).
- Sie ist eine **reine Liste** mit den Spalten **Titel, Firma, Arbeitsort,
  Status und Arbeitsweg**. Keine Suche, kein Filter, keine Sortierung nach
  Spalten.
- Die Liste zeigt die **neueste Stelle zuerst** (nach `erstellt_am`).
- Es werden nur die Stellen des Demo-Benutzers gelesen
  (`aktuelle_benutzer_id()`, Regel B1 im [Datenmodell](../../datenmodell.md)).
- Der **Status** erscheint mit seiner Anzeige aus Abschnitt 5 im Datenmodell,
  z.B. `interview` als «Vorstellungsgespräch».
- Der **Arbeitsweg** zeigt die gespeicherten Werte aus Use Case 3: Strecke in
  Kilometern und Fahrzeit in Minuten. Sind sie leer, bleibt die Zelle leer.
  Die Übersicht löst keine Berechnung aus.
- Die Schaltfläche **«+ Neue Stelle»** öffnet das bestehende Stellen-Formular
  aus Use Case 1. **«← Zurück zur Übersicht»** im Formular führt zurück und
  lädt die Übersicht neu.
- Nach dem Speichern bleibt das Formular offen, damit Arbeitsweg oder Hinweis
  sichtbar bleiben ([US 30006](../Use_Case_3/30006-arbeitsweg-im-formular-anzeigen.md)).
  Entschieden am 24.10.2026 (Mirko); ersetzt den ursprünglichen Plan, nach dem
  Speichern direkt zur Übersicht zu wechseln.
- Ist noch keine Stelle gespeichert, bleibt die Liste leer. Es erscheint keine
  zusätzliche Meldung.

## Ablauf

1. Der Nutzer öffnet die Anwendung.
2. Das Frontend fragt `GET /api/stellenanzeigen` ab.
3. Das Backend liest alle Stellen des Demo-Benutzers aus der Tabelle
   `stellenanzeigen`, neueste zuerst.
4. Es antwortet mit einer JSON-Liste. Jede Stelle enthält `id`, `titel`,
   `firma`, `arbeitsort`, `status`, `strecke_auto_in_metern` und
   `fahrzeit_auto_in_minuten`.
5. Das Frontend zeigt die Stellen als Liste an.

## Akzeptanzkriterien

- [x] Beim Öffnen der Anwendung erscheint die Übersicht.
- [x] `GET /api/stellenanzeigen` liefert alle Stellen des Demo-Benutzers als
      JSON-Liste, neueste zuerst.
- [x] Jede Zeile zeigt Titel, Firma, Arbeitsort, Status und Arbeitsweg.
- [x] Der Status erscheint mit dem Anzeigetext aus dem Datenmodell.
- [x] Der Arbeitsweg erscheint in Kilometern und Minuten; fehlen die Werte,
      bleibt die Zelle leer.
- [x] Ohne gespeicherte Stellen liefert das Backend eine leere Liste, und die
      Übersicht zeigt keine Zeilen.
- [x] Eine neu gespeicherte Stelle erscheint nach «← Zurück zur Übersicht»
      oben in der Übersicht.
- [x] «+ Neue Stelle» öffnet das Stellen-Formular.
- [x] Das Laden der Übersicht ändert keine Daten und löst keine
      Arbeitswegberechnung aus.
- [x] Unittests prüfen die Route mit leerer und mit gefüllter Liste.

## Schrittweise Umsetzung

1. **Datenbank:** In `datenbank.py` eine Funktion ergänzen, die alle Stellen
   des Demo-Benutzers liest, neueste zuerst.
2. **Backend:** In `stellenanzeigen_routes.py` die Route
   `GET /api/stellenanzeigen` ergänzen, die diese Funktion aufruft und JSON
   zurückgibt. Mit dem Browser direkt unter `/api/stellenanzeigen` prüfen.
3. **Test:** Unittests für die Route im Stil der bestehenden Tests schreiben.
4. **Frontend:** In `public/index.html` die Liste anzeigen, zuerst nur mit Titel
   und Firma.
5. **Frontend:** Die übrigen Spalten ergänzen, mit Anzeigetext für den Status
   und Kilometern für die Strecke.
6. **Frontend:** Übersicht als Startseite einrichten, «+ Neue Stelle» mit dem
   Formular verbinden und «← Zurück zur Übersicht» ergänzen.

## Noch nicht enthalten

- Öffnen einer Stelle per Klick auf eine Zeile (US 20002).
- Status ändern, Stelle bearbeiten oder löschen (US 20003 bis US 20005).
- Suche, Filter und Sortierung nach Spalten.
- Seitenweise Anzeige bei vielen Stellen.
- Berechnung des Arbeitswegs (Use Case 3).

## Technische Prüfung vor der Umsetzung

- Prüfen, wie `public/index.html` heute aufgebaut ist und wie Übersicht und
  Formular darin umgeschaltet werden können, ohne einen zweiten Screen als
  eigene Datei zu bauen.
- Mit Use Case 1 abgestimmt (2026-10-24): Die Übersicht wird zur Startseite,
  das Formular erscheint über «+ Neue Stelle». Mirko baut die Umschaltung in
  `public/index.html` in dieser Story. Den Pull Request prüft die
  verantwortliche Person von Use Case 1
  ([ADR 0005](../../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)).
- Prüfen, wie die bestehenden Tests die Datenbank ersetzen, und dasselbe
  Vorgehen für die neue Route verwenden.
