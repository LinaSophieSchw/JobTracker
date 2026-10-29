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

### 2026-10-25 – US 20002: Stelle aus der Übersicht öffnen

**Was haben wir gemacht?**
US 20002 als eigene Story beschrieben
(`docs/Use_cases/Use_Case_2/20002-stelle-oeffnen.md`) und als Vertical Slice
umgesetzt:
- Datenbank: `stellenanzeige_mit_id_lesen()` in `src/app/datenbank.py` liest
  eine Stelle über ihre `id`, nur für den Demo-Benutzer.
- Backend: Route `GET /api/stellenanzeigen/<id>` in
  `src/app/stellenanzeigen_routes.py`; unbekannte Stelle → 404.
- Tests: 8 Unittests in `tests/test_stellenanzeige_oeffnen.py`.
- Frontend: Klick auf eine Zeile der Übersicht öffnet die Stelle im
  Stellen-Formular im Zustand «Bestehend» (`public/index.html`).

**Warum haben wir das gemacht?**
Ohne Öffnen kann man eine Stelle später weder ändern noch löschen (US 20003
bis US 20005). Das bestehende Formular wird wiederverwendet statt einer eigenen
Detailansicht (ADR 0005). «Speichern» und «Löschen» sind im Zustand
«Bestehend» vorerst ausgeblendet, weil die heutige Speicherroute immer eine
neue Stelle anlegt und so Duplikate entstehen würden.

**Welche Auswirkungen hat das?**
Eine Stelle lässt sich per Klick öffnen und ansehen. Änderungen im Formular
werden noch nicht gespeichert; das folgt mit US 20003. Die Antwort enthält
schon den `status`, damit US 20003 ihn nutzen kann.

**Welche Konzepte wurden behandelt?**
- Platzhalter in der Route: `<int:stellen_id>` nimmt die Zahl aus der Adresse.
- `fetchone()` statt `fetchall()`: eine Zeile oder `None`.
- HTTP-Statuscodes: 200 OK, 404 nicht gefunden, 503 Dienst nicht verfügbar.
- Warum 404 auch bei der Stelle eines fremden Benutzers: Die Antwort verrät
  nicht, dass es die `id` gibt (Regel B1).
- Unittests: prüfen einzelne Funktionen automatisch, bleiben im Repo und
  schützen vor Rückschritten; Mock ersetzt die Datenbank.
- Vue: `@click` auf einer Tabellenzeile, `v-if` mit einer Zustandsvariable
  (`geoeffnete_stelle_id`), Template-Strings mit `${...}`.
- Git-Worktree: zweiter Arbeitsordner mit eigenem Branch; VS Code muss diesen
  Ordner öffnen, und die `.env` muss dort ebenfalls liegen.

**Eigenleistung und KI-Unterstützung**
- Mirko: Entscheide zu Klick auf die ganze Zeile, 404-Verhalten, nur «Zurück»
  im Zustand «Bestehend» und PR-Prüfung durch Use Case 1; Freigabe der Story;
  Tests im Browser (Route und Oberfläche); Freigabe der Commits.
- KI (Claude): Story-Entwurf, Code, Unittests und Erklärungen zu jedem Schritt,
  Commits nach Zustimmung.

**Persönliche Reflexion – von Mirko zu ergänzen**
Offen: Was kann ich jetzt selbst erklären, und welcher Teil war am schwierigsten
zu verstehen?

**Nächster Lernschritt**
Pull Request für US 20002 öffnen und von Use Case 1 prüfen lassen. Vor US 20003
mit Fabio den offenen Punkt O2 klären: Wer baut den `PUT`, und wie wird die
Neuberechnung des Arbeitswegs (US 30003) eingebunden?

### 2026-10-29 – US 20003: Status einer Stelle ändern

**Was haben wir gemacht?**
US 20003 beschrieben (`docs/Use_cases/Use_Case_2/20003-status-aendern.md`),
den offenen Punkt O2 entschieden und die Story als Vertical Slice umgesetzt:
- Datenbank: `status_speichern()` und die Konstante `ERLAUBTE_STATUS` in
  `src/app/datenbank.py`; `UPDATE` mit `geaendert_am`, Rückmeldung über
  `rowcount`.
- Backend: Route `PUT /api/stellenanzeigen/<id>` in
  `src/app/stellenanzeigen_routes.py`: Status speichern, Stelle lesen,
  Arbeitsweg mit Fabios `arbeitsweg_eintragen()` unverändert neu berechnen.
- Tests: 9 Unittests in `tests/test_status_aendern.py`.
- Frontend (`public/index.html`): Status-Dropdown und «Speichern» im Zustand
  «Bestehend», Hilfsfunktion `arbeitsweg_texte_setzen()`.

**Warum haben wir das gemacht?**
Der Status zeigt den Stand der Bewerbung. Die Neuberechnung bei jedem
Speichern erfüllt US 30003, ohne Fabios Code zu ändern: Die gelesene Stelle
enthält genau die Adressfelder, die seine Funktion braucht. Reihenfolge
speichern → lesen → rechnen, damit ab US 20004 auch eine geänderte Adresse
verwendet wird. Betrachtete Alternativen: keine Neuberechnung bei reiner
Statusänderung; nach dem ersten Speichern direkt in den Zustand «Bestehend»
wechseln (zurückgestellt, berührt Use Case 1 und US 30006).

**Welche Auswirkungen hat das?**
Der Status einer geöffneten Stelle lässt sich speichern und erscheint in der
Übersicht. Jeder Klick auf «Speichern» fragt OpenRouteService an. Fabio muss
informiert werden; den Stand von US 30003 führt er selbst nach.

**Welche Konzepte wurden behandelt?**
- HTTP-Methoden: `GET` lesen, `POST` neu anlegen, `PUT` Bestehendes ändern;
  `fetch` ohne `method` schickt `GET`. 200 statt 201 bei einer Änderung.
- 405 «Method Not Allowed»: Server lief mit altem Code; `flask run --debug`
  lädt Änderungen automatisch neu. HTML-Fehlerseite statt JSON führt zu
  «Unexpected token '<'».
- `rowcount`, `ValueError` → 400, `pytest.raises`, Mock-Aufrufe prüfen mit
  `call_args` und `assert_not_called()`.
- Vue: `<select>` mit `v-model` (zwei Richtungen) gegenüber `:value` (eine
  Richtung); `v-for` über ein Objekt; `v-if`/`v-else` für zwei Knöpfe;
  `try`/`catch`/`finally`.
- Die Übersicht lädt nur beim Öffnen der Seite oder bei «Zurück» neu.

**Eigenleistung und KI-Unterstützung**
- Mirko: Entscheide zu Neuberechnung bei jedem Speichern, Formular bleibt
  offen, Variante A (kein direkter Wechsel nach dem ersten Speichern); Test
  des `PUT` in der Browser-Konsole inkl. Fehlersuche (405); Tests im Browser;
  Freigabe der Commits.
- KI (Claude): Story-Entwurf, Code, Unittests und Erklärungen mit Alternativen
  und Kontrollfragen, Commits nach Zustimmung.

**Persönliche Reflexion – von Mirko zu ergänzen**
Antworten auf Kontrollfragen in dieser Sitzung, wie gegeben:
- Wo finde ich `POST`? Antwort zu `fetch` ohne `method`: «fetchall dann wird
  das auf alles angewandt» (Ergänzung: ohne `method` schickt `fetch` ein
  `GET`; `fetchall` gehört zur Datenbank).
- Zweites «Speichern» nach dem Anlegen: «Nein es sollte stehen, dass sie
  bereits existiert.»
- `status_speichern()` bei fremder Stelle: «404 weil die stelle in der DB zwar
  gefunden wird jedoch nicht für den richtigen nutzer» (Ergänzung: die
  Funktion liefert `False`, erst die Route macht 404; die Datenbank findet
  wegen `AND benutzer_id` gar keine Zeile).
- 405 beim `PUT`: «weil der server gestartet wurde und erst dann die PUT
  funktion erstellt wurde.»
- `assert_not_called()` bei unbekannter Stelle: «sonst würde immer etwas
  erwartet werden vom kartendienst und es würde immer versucht gerechnet zu
  werden.»
- `v-model` statt `:value` und `finally`: offen, im Chat erklärt.

Offen: Was kann ich jetzt selbst erklären, und welcher Teil war am schwierigsten
zu verstehen?

**Nächster Lernschritt**
Fabio über den `PUT` informieren, Pull Request für US 20003 öffnen und von
Use Case 1 prüfen lassen. Danach US 20004: weitere Angaben und die
Arbeitsadresse über denselben `PUT` speichern.
