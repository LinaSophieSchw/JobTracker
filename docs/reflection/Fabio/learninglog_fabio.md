# Learninglog – Fabio

## 2026-10-20 – Wireframes, Prototyp und Entscheide zur Oberfläche

**Was haben wir gemacht?**
Fabio liess Wireframes und einen klickbaren Prototyp erstellen, um zu sehen,
welche Screens und Funktionen die Applikation braucht
([docs/wireframes](../../wireframes/README.md)). Ergebnis sind drei Screens
(Übersicht, Stellen-Formular, Profil) und eine Liste der nötigen
Backend-Aufrufe. Daraus entstanden die Entscheide
[ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md) bis
[ADR 0010](../../decisions/0010-minimale-oberflaeche.md). Linas Entscheidung
zu PostgreSQL wurde als
[ADR 0007](../../decisions/0007-postgresql-bei-neon.md) nachgetragen.
Datenmodell und Stories von Use Case 3 wurden angeglichen. Die Stories von
Use Case 1 passt die Person an, die Use Case 1 bearbeitet.

**Warum haben wir das gemacht?**
Die Use Cases standen einzeln nebeneinander, und es fehlte eine Vorstellung,
wie die Applikation als Ganzes funktioniert. Die Wireframes dienten nicht dem
Design, sondern dem Verständnis der Abläufe.

**Welche Auswirkungen hat das?**
Beim Zeichnen wurden Widersprüche zwischen Dokumenten sichtbar, zum Beispiel
beim Adressformat und beim externen Dienst. Fabio
legte fest:

- Adressen ändern gehört zu Use Case 2.
- Felder für Arbeitsadresse und Arbeitsweg gehören zum Formular von Use Case 1,
  ebenso das Profil mit Wohnadresse. Die Stories dazu bleiben in Use Case 3
  nur als Reserve (US 30004 und 30005).
- Use Case 3 berechnet nur den Arbeitsweg, mit OpenRouteService.
- «+ Neue Stelle» ist gesperrt, bis ein Profil gespeichert ist.
- Es gibt keine Hinweis- oder Erfolgsmeldungen.

Die Vorschläge (ADR 0009 und 0010) muss das Team noch bestätigen.

**Welche Konzepte wurden behandelt?**
Wireframe und klickbarer Prototyp als Mittel, Anforderungen zu klären;
Zuordnung von Funktionen zu Use Cases; Decision Records mit Status
«Vorgeschlagen» und «Ersetzt durch».

**Eigenleistung und KI-Unterstützung**
Fabio gab Ziel und Rahmen vor, beantwortete die offenen Fragen und traf die
oben genannten Entscheide. Die Stories zu Use Case 3 brachte er mit; wie sie
entstanden sind, ist hier nicht festgehalten. Der Agent zeichnete Wireframes
und Prototyp, wies auf Widersprüche hin und entwarf die ADRs sowie die
Anpassungen an Datenmodell und Stories.

**Persönliche Reflexion – von Fabio zu ergänzen**
Was hat das Durchklicken des Prototyps gezeigt, das in den Use-Case-Texten
nicht sichtbar war?

**Nächster Lernschritt**
Mit dem Team die vorgeschlagenen ADRs im
Pull Request besprechen.

## 2026-10-21 – Fest hinterlegter Benutzer statt Profilerfassung

**Was haben wir gemacht?**
Die Stories von Use Case 3 wurden an die Teambesprechung vom 21.10.2026
angepasst. US 30004 beschreibt neu, dass ein Demo-Benutzer mit Wohnadresse in
drei Feldern fest im System hinterlegt wird
([US 30004](../../Use_cases/Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md)).
Sie ist keine Reserve mehr, sondern die erste Story von Use Case 3. Die
Stories 30001 bis 30003, 30005 und das
[README](../../Use_cases/Use_Case_3/README.md) verweisen nicht mehr auf ein
Profil.

**Warum haben wir das gemacht?**
Die Absprache vom Montag zum Profil wurde im Team unterschiedlich verstanden.
Im Code ist bereits ein Dummy-Benutzer angelegt, dem alle Stellen zugeordnet
werden. Das Team lässt das vorläufig so, bis geklärt ist, wer das Profil
anlegen übernimmt. Fabio legte fest, dass das Hardcoden des Benutzers eine
eigene Story in Use Case 3 ist und es keine Maske zur Erfassung des Nutzers
gibt.

**Welche Auswirkungen hat das?**
Stellen können ohne vorheriges Profil gespeichert werden. Die
Arbeitswegberechnung liest die Wohnadresse des Demo-Benutzers aus der
Datenbank. Offen: Im Code liegt die Wohnadresse noch in einer einzigen Spalte;
Datenmodell (Abschnitt 3, Regel B2) und ADR 0010 gehen noch von einer
Profilerfassung und einer Sperre von «+ Neue Stelle» aus. Der Eintrag vom
20.10.2026 nennt US 30004 noch als Reserve; das ist damit überholt.

**Welche Konzepte wurden behandelt?**
Testdaten bzw. Seed-Daten, die beim Anlegen der Datenbank eingefügt werden;
Abhängigkeiten zwischen Stories und deren Reihenfolge.

**Eigenleistung und KI-Unterstützung**
Fabio brachte das Ergebnis der Teambesprechung ein und entschied, das
Hardcoden als Story zu führen. Der Agent formulierte US 30004 neu, passte die
übrigen Stories und das README an und wies auf die offenen Widersprüche in
Datenmodell, ADR 0010 und Code hin.

**Persönliche Reflexion – von Fabio zu ergänzen**
Was hätte geholfen, das Missverständnis zur Absprache vom Montag früher zu
bemerken?

**Nächster Lernschritt**
Mit Lina klären, wer die Umstellung der Wohnadresse auf drei Spalten übernimmt
und wer Datenmodell und ADR 0010 anpasst.

## 2026-10-21 – US 30004 umgesetzt, Merge-Konflikt mit Linas Stand gelöst

**Was haben wir gemacht?**
US 30004 wurde auf dem Branch `feature/30004-demo-benutzer` umgesetzt und als
Pull Request #17 eröffnet. Neu ist die Funktion `wohnadresse_lesen()` in
`src/app/datenbank.py`; sie liest die Wohnadresse des Demo-Benutzers in drei
Teilen aus der Datenbank. Dazu kamen drei Unittests in
`tests/test_datenbank.py`, Anpassungen an `docs/datenmodell.md` (Abschnitt 3,
Regel B2) und ADR 0010 sowie ein
[Spickzettel für die Präsentation](../../Use_cases/Use_Case_3/30004-spickzettel.md).
Mit der Verbindungsadresse von Lina in der lokalen `.env` wurde die Funktion
einmal gegen die Neon-Datenbank geprüft (nur lesend).

Während der Arbeit hatte Lina mit PR #16 die Tabelle `benutzer` ebenfalls auf
drei Adressspalten umgestellt. Beim Mergen von `master` in den Branch entstand
ein Merge-Konflikt in `tabellen_erstellen()`. Beide Versionen waren inhaltlich
gleich; übernommen wurde Linas Version, dazu kam nur `wohnadresse_lesen()`.
Damit ist der offene Punkt aus dem vorherigen Eintrag (Wohnadresse in einer
Spalte) erledigt.

**Warum haben wir das gemacht?**
Die Arbeitswegberechnung braucht einen Startpunkt. Die Arbeitsadresse kommt
beim Speichern aus dem Formular, die Wohnadresse steht nur in der Datenbank.
Eine eigene Funktion ist einzeln testbar und in US 30001 und 30003
wiederverwendbar. Linas Version wurde übernommen, weil sie bereits auf
`master` war; so ändert der Pull Request ihren Code nicht.

**Welche Auswirkungen hat das?**
Die Wohnadresse kann für US 30001 gelesen werden. Mit PR #16 sind auch die
Felder der Arbeitsadresse und die Spalten für Fahrzeit und Strecke vorhanden;
US 30001 ist damit nicht mehr blockiert. Offen: Linas Code-Kommentar spricht
von «Fabios Profilerfassung», die es laut US 30004 vorläufig nicht gibt. Die
Verbindungsadresse wurde im Chat mit dem Agenten geteilt; Lina sollte das
Neon-Passwort zurücksetzen. Unklar ist, ob die verwendete Datenbank Linas
gemeinsame ist; vor dem Speichern von Testdaten klären.

**Welche Konzepte wurden behandelt?**
Merge-Konflikt: Zwei Personen ändern dieselben Zeilen, Git markiert die Stelle
mit `<<<<<<<`, `=======` und `>>>>>>>` und ein Mensch entscheidet. Idempotenz
(`CREATE TABLE IF NOT EXISTS`, `ON CONFLICT DO NOTHING`). SQL-Platzhalter
`%s` gegen SQL-Injection. Mocks in Tests und ihre Grenzen. Connection String
und `.env` als Ort für Geheimnisse.

**Eigenleistung und KI-Unterstützung**
Fabio sprach den Umbau mit Lina ab, gab die Freigaben für Plan, Commit, Merge
und Pull Request und richtete die `.env` mit der Verbindungsadresse ein. Er
fragte nach, ob beim Start jedes Mal ein neuer Benutzer entsteht und wozu
`wohnadresse_lesen()` nötig ist. Er liess einen Test löschen, der ohne echte
Datenbank kaum etwas prüft, verlangte eine Beschreibung des Zwecks im
Testcode und gab Form und Inhalt des Spickzettels vor. Der Agent schrieb Code,
Tests und Doku, erklärte die Schritte, löste den Merge-Konflikt und prüfte,
dass der Pull Request Linas Code nicht verändert.

**Persönliche Reflexion – von Fabio zu ergänzen**
Wie hätte das Team vermeiden können, dass zwei Personen gleichzeitig dieselbe
Tabelle umbauen?

**Nächster Lernschritt**
Für US 30001 einen API-Schlüssel bei OpenRouteService anlegen und eine erste
Abfrage mit den Beispieladressen ausprobieren.

## 2026-10-24 – US 30001 umgesetzt: Fahrzeit beim ersten Speichern

**Was haben wir gemacht?**
US 30001 wurde auf dem Branch `feature/30001-fahrzeit` als Vertical Slice
umgesetzt (Arbeit vom 22. bis 24.10.2026). Beim Klick auf «Speichern» wird
die Stelle gespeichert, danach die Autofahrzeit von der Wohnadresse des
Demo-Benutzers zur Arbeitsadresse über OpenRouteService berechnet, in
`fahrzeit_auto_in_minuten` eingetragen und im Browser angezeigt («Fahrzeit mit
dem Auto: 95 Minuten» oder «Arbeitsweg konnte nicht berechnet werden.»).

- Neu: `src/app/arbeitsweg.py` (`koordinaten_suchen()`,
  `fahrzeit_in_sekunden_abfragen()`, `fahrzeit_berechnen()`),
  `fahrzeit_speichern()` in `src/app/datenbank.py`,
  `arbeitsweg_eintragen()` in `src/app/stellenanzeigen_routes.py`,
  `tests/test_arbeitsweg.py` mit drei Tests.
- Geändert in Linas Code: ein Aufruf in der Speicherroute, eine Stelle in
  `public/index.html`, ein angepasster Test.
- Doku: Befund der technischen Prüfung in der Story,
  [ADR 0011](../../decisions/0011-strukturierte-adresssuche.md),
  Nachtrag in ADR 0008,
  [Spickzettel](../../Use_cases/Use_Case_3/30001-spickzettel.md).

**Warum haben wir das gemacht?**
Die Story verlangt die Fahrzeit beim ersten Speichern. Vor dem Programmieren
wurde der Kartendienst mit öffentlichen Beispieladressen geprüft. Dabei zeigte
sich, dass die Freitext-Suche eine erfundene Adresse als echte Adresse in Chur
erkennt. Deshalb wurde auf die strukturierte Suche gewechselt und nur ein
Treffer vom Typ `address` verwendet (ADR 0011). Zuerst speichern, dann
rechnen: So bleibt die Stelle auch bei einem Berechnungsfehler gespeichert,
und Linas Speicherfunktion musste nicht geändert werden.

Nach der ersten Fassung liess Fabio den Code verschlanken, damit er jede
Codestelle in der Präsentation erklären kann: Hilfsfunktionen, Testteil,
Vorabprüfungen und ein Test fielen weg; Fehler werden mit einem einzigen
`except Exception` aufgefangen.

**Welche Auswirkungen hat das?**
Die Fahrzeit wird beim Speichern berechnet, gespeichert und angezeigt.
39 Tests laufen durch. Im Browser und gegen Neon wurde der Ablauf mit
Teststellen geprüft; diese wurden danach gelöscht. Offen:
- Anzeige beim erneuten Öffnen gehört zur Detailansicht von Use Case 2.
- Der Schlüssel muss online in den Vercel-Einstellungen eingetragen werden.
- Fällt die Datenbank genau zwischen Speichern und Eintragen aus, erscheint
  ein Fehler, obwohl die Stelle gespeichert ist (bewusst in Kauf genommen).
- Commit und Pull Request stehen noch aus.

**Welche Konzepte wurden behandelt?**
Externer Web Service mit API-Schlüssel; Geocoding (Adresse → Koordinaten);
HTTP-Anfragen mit `requests.get` und `requests.post`; Parameter in der URL
(`params`) und Header; Statuscodes (200, 403, 404) und `raise_for_status()`;
Zeitlimit; JSON; Fehler auslösen und auffangen (`raise`, `try`/`except`);
`None` in Python und `null` in JSON; `UPDATE` statt `INSERT`;
Umgebungsvariablen und `.env`; Mocks und `monkeypatch` in Tests; Gegenprobe,
ob Tests bei eingebauten Fehlern rot werden.

**Eigenleistung und KI-Unterstützung**
Fabio legte das OpenRouteService-Konto an und trug den Schlüssel selbst in die
`.env` ein. Er mergte PR #17 und gab den Plan frei. Er übernahm die
Empfehlungen zur strukturierten Suche und zum Umgang mit «erneut öffnen». Er
strich drei geplante Tests, fragte nach, ob eine Adresse beim ersten Speichern
sofort berechnet wird, und liess sich `antwort`, `raise_for_status()` und
`params` erklären. Er legte fest, wie Erklärungen aussehen sollen (Zweck,
Schritte in Reihenfolge mit Codestück, Warum, nicht zu detailliert) und dass
sie auch als Kommentare in den Code gehören. Er bestimmte die Teamregel, Code
anderer nur nach Absprache zu ändern, und gab an, dass die Änderungen an
Linas Code mit ihr abgesprochen sind. Er wählte die neun Vereinfachungen und
erlaubte Teststellen in Neon.

Der Agent führte die technische Prüfung durch, schrieb Code, Tests und Doku,
erklärte die Schritte, prüfte den Ablauf im Browser und gegen Neon und machte
die Gegenprobe der Tests.

**Persönliche Reflexion – von Fabio zu ergänzen**
Welche Codestellen kann ich jetzt ohne Spickzettel erklären, und bei welchen
brauche ich ihn noch?

**Nächster Lernschritt**
Änderungen mit dem Skill `end-coding` committen und als Pull Request
eröffnen; mit Lina klären, dass die Detailansicht von Use Case 2 die Spalte
`fahrzeit_auto_in_minuten` anzeigt.
