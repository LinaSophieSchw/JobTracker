# Learninglog – Mirko

### 2026-10-24 – Use Case 2 dokumentieren: README und US 20001

**Was haben wir gemacht?**
Für Use Case 2 (Stellenanzeigen verwalten) ein README erstellt: Ziel,
Story-Liste US 20001 bis US 20005 mit Endpunkten, Oberfläche, Abgrenzung zu
Use Case 1 und Use Case 3, offene und entschiedene Punkte
(`docs/Use_cases/Use_Case_2/README.md`). Danach die erste Story ausführlich nach
der Vorlage der anderen Use Cases geschrieben
(`docs/Use_cases/Use_Case_2/20001-uebersicht-aller-stellen.md`). Commit
`c2b7641` auf dem Branch `docs/20000-use-case-2`.

**Warum haben wir das gemacht?**
Die Story-Liste hängt vom Umfang ab. Steht der Umfang fest, müssen die Stories
später nicht umgebaut werden. Bewusst wird nur die erste Story ausführlich
geschrieben und umgesetzt, bevor die nächste folgt. Alternative wäre gewesen,
alle Stories vorab zu schreiben, wie bei Use Case 1 und Use Case 3.

**Welche Auswirkungen hat das?**
- Entscheide von Mirko: Status-Dropdown im Formular statt in der Übersicht;
  keine Suche und kein Filter (wie in ADR 0010 vorgeschlagen); vorerst keine
  Maske zum Ändern des Profils, der Demo-Benutzer bleibt fest hinterlegt.
- Abgesprochen mit der verantwortlichen Person von Use Case 1: Die Übersicht
  wird zur Startseite, Mirko baut die Umschaltung in `public/index.html`, die
  Person von Use Case 1 prüft den Pull Request.
- Offen: Mit Fabio klären, wer den `PUT` für bestehende Stellen baut (vor
  US 20003). ADR 0010 hat noch den Status «Vorgeschlagen»; die Annahme ist ein
  Teamentscheid.

**Welche Konzepte wurden behandelt?**
- Vertical Slice: eine Story geht vom Frontend über das Backend bis zur
  Datenbank; zuerst Lesen (US 20001), dann Schreiben (US 20003).
- Pull Request: Anfrage, einen Branch nach einem Review in `master` zu
  übernehmen.
- Branch und Worktree: Ein Branch ist ein Entwicklungsstrang in Git, ein
  Worktree ein zusätzlicher Ordner, in dem ein Branch ausgecheckt ist.

**Eigenleistung und KI-Unterstützung**
- Mirko: Entscheide zu Status-Dropdown, Suche/Filter, Profilmaske und Sortierung
  (neueste zuerst); Absprache mit Use Case 1; Prüfung der Story-Liste.
- KI (Claude): Lesen der Projektdokumente, Vorschlag der Story-Liste, Entwurf
  von README und US 20001, Commit und Push nach Zustimmung.

**Persönliche Reflexion – von Mirko zu ergänzen**
Antwort auf die Kontrollfrage, warum die Person von Use Case 1 den Pull Request
prüft: «weil sie Überschneidungen hat mit meinem UC und die Änderungen sie
betreffen.»

Offen: Was kann ich jetzt selbst erklären, und was würde ich bei der nächsten
Story anders machen?

**Nächster Lernschritt**
US 20001 umsetzen, beginnend mit der Datenbankfunktion in `datenbank.py`.
Offene Kontrollfrage: Warum ist es sinnvoll, US 20001 (nur lesen) vor US 20003
(speichern) umzusetzen?

### 2026-10-24 – US 20001 umsetzen: Übersicht aller Stellen

**Was haben wir gemacht?**
US 20001 als Vertical Slice in sechs Schritten umgesetzt, von unten nach oben,
auf dem Branch `feature/20001-uebersicht`:

- Datenbank: `stellenanzeigen_lesen()` in `src/app/datenbank.py` liest alle
  Stellen des Demo-Benutzers, die neueste zuerst (`ORDER BY erstellt_am DESC`).
- Backend: Route `GET /api/stellenanzeigen` in
  `src/app/stellenanzeigen_routes.py`, bei Datenbankfehler 503 ohne technische
  Details.
- Tests: 7 Unittests in `tests/test_stellenanzeigen_uebersicht.py`, mit Mock
  statt echter Datenbank, darunter ein Test, dass keine Arbeitswegberechnung
  ausgelöst wird.
- Frontend: Tabelle mit Titel, Firma, Arbeitsort, Status (Anzeigetext) und
  Arbeitsweg (km, min) in `public/index.html`; Umschalten zwischen Übersicht
  und Formular mit «+ Neue Stelle» und «← Zurück zur Übersicht».

Commits `b672b35`, `b836525`, `14af916`, `05cc31e`.

**Warum haben wir das gemacht?**
Bei einer Story, die Daten anzeigt, fliessen die Daten von der Datenbank zum
Browser; darum wurde unten begonnen. Nach jedem Schritt war etwas
ausprobierbar, und das Backend wurde vor dem Frontend committet.

**Welche Auswirkungen hat das?**
- Die Übersicht ist die Startseite; das Formular aus Use Case 1 erscheint über
  «+ Neue Stelle» (mit Use Case 1 abgesprochen).
- Entscheid von Mirko: Nach dem Speichern bleibt das Formular offen, wie in
  US 30006 von Fabio, damit Arbeitsweg oder Hinweis sichtbar bleiben. US 20001
  und ADR 0010 wurden angepasst. Verworfen: direkt zur Übersicht wechseln, wie
  ursprünglich in ADR 0010 und der Story geplant.
- Prüfung mit der echten Neon-Datenbank zuerst offen, weil lokal die `.env`
  mit `DATABASE_URL` fehlte. Nachgetragen am 24.10.2026: Mirko hat `.env`
  angelegt und alle drei Prüfungen bestanden (Stellen erscheinen, neue Stelle
  speichern, neue Stelle steht nach «← Zurück zur Übersicht» zuoberst).
- Bemerkt, nicht geändert: ADR 0010 sagt «keine Erfolgsmeldungen», das
  Formular zeigt aber nach dem Speichern eine Bestätigung.

**Welche Konzepte wurden behandelt?**
- Route und HTTP-Methoden: dieselbe Adresse, GET liest, POST schickt Daten.
- SQL-Abfrage mit `WHERE` und `ORDER BY ... DESC`; Tupel aus `fetchall()` in
  Dictionaries mit Namen umwandeln.
- Mock und `monkeypatch`: Datenbank in Tests ersetzen; Funktion dort ersetzen,
  wo sie verwendet wird. Hilfsfunktionen in Tests nicht mit `test` beginnen.
- Vue: `data()`, `v-for`, `v-if`/`v-else`, `mounted()`; «Wir ändern die Daten,
  Vue passt das HTML an.»
- `.env`: Geheimnisse wie die Datenbankadresse gehören nicht in Git.
- Linter: VS-Code-Erweiterung Flake8 prüfte mit 79 statt den im Projekt
  festgelegten 88 Zeichen; Flake8 deaktiviert, Ruff verwendet.

**Eigenleistung und KI-Unterstützung**
- Mirko: Freigabe des Plans, Bestätigung der Sortierung «neueste zuerst»,
  Entscheid «Formular bleibt nach dem Speichern offen», Absprache mit Use Case 1,
  Prüfung im Browser, Freigabe der Commits.
- KI (Claude): Code, Tests und Erklärungen zu jedem Schritt, Prüfung im Browser
  mit Beispieldaten, Commits und Push nach Zustimmung.

**Persönliche Reflexion – von Mirko zu ergänzen**
Antworten auf Kontrollfragen in dieser Sitzung, wie gegeben:
- Ohne `ORDER BY`: «dann wäre sie entweder alphabetisch oder willkürlich»
  (Ergänzung: ohne `ORDER BY` ist die Reihenfolge nicht festgelegt, nicht
  alphabetisch).
- Meter erst im Frontend umrechnen: «weil in der Datenbank die Rohdaten stehen
  sollen für die Weiterverwendung.»
- Ohne `stellen_laden()` in `zur_uebersicht()`: «die aktuellste Stelle würde
  nicht mitgenommen werden.»

Offen: Was kann ich jetzt selbst erklären, und welcher Teil war am schwierigsten
zu verstehen?

**Nächster Lernschritt**
Review und Merge des Pull Requests. Danach US 20002: Stelle aus der Übersicht
öffnen.
