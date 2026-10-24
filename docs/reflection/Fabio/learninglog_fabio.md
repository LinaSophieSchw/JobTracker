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

## 2026-10-24 – US 30002 umgesetzt: Streckenlänge ergänzen

**Was haben wir gemacht?**
US 30002 wurde auf dem Branch `feature/30002-streckenlaenge` umgesetzt. Beim
Speichern einer Stelle wird neben der Fahrzeit auch die Strecke aus derselben
Routenantwort übernommen, in `strecke_auto_in_metern` gespeichert und im
Browser angezeigt («Fahrzeit mit dem Auto: 95 Minuten, Strecke: 138.3 km»).

- Geändert: `arbeitsweg_berechnen()` (vorher `fahrzeit_berechnen()`) in
  `src/app/arbeitsweg.py` fragt die Route jetzt selbst ab; die eigene
  Funktion `fahrzeit_in_sekunden_abfragen()` ist weggefallen, `arbeitsweg_speichern()` (vorher
  `fahrzeit_speichern()`) in `src/app/datenbank.py`, `arbeitsweg_eintragen()`
  und die Antwort der Speicherroute in `src/app/stellenanzeigen_routes.py`,
  Anzeige in `public/index.html`.
- Tests: drei angepasste Tests in `tests/test_arbeitsweg.py` (der Test der
  Speicherroute prüft auch Umrechnung und einzige Routenabfrage), ein
  angepasster Test von Lina in `tests/test_stellenanzeige_speichern.py`.
- Doku: Befund in der Story,
  [Spickzettel](../../Use_cases/Use_Case_3/30002-spickzettel.md), Hinweis im
  Spickzettel von US 30001, Stand in der Übersicht von Use Case 3.

**Warum haben wir das gemacht?**
Die Story verlangt die Strecke zusätzlich zur Fahrzeit, ohne zusätzliche
Abfrage. Die technische Prüfung von US 30001 hatte schon gezeigt, dass
`distance` in Metern in derselben Antwort steht wie `duration`. Die Spalte
`strecke_auto_in_metern` gab es bereits; eine Schemaänderung war nicht nötig.
Entscheide: In der Datenbank ganze Meter, im Browser Kilometer mit einer
Nachkommastelle. Beide Werte werden als Dictionary weitergegeben, dessen
Schlüssel gleich heissen wie die Datenbankspalten. Die Funktionen wurden
umbenannt, weil sie nicht mehr nur die Fahrzeit liefern.

**Welche Auswirkungen hat das?**
Strecke und Fahrzeit werden zusammen berechnet, in einem `UPDATE`
gespeichert und angezeigt; scheitert die Berechnung, bleiben beide leer.
39 Tests laufen durch. Eine echte Abfrage Bern–Zug ergab 95 Minuten und
138268 Meter. Die Anzeige wurde im Browser mit simulierten Serverantworten
(Erfolg und Fehler) geprüft; ein Durchlauf gegen Neon fand diesmal nicht
statt. Offen:
- Anzeige beim erneuten Öffnen gehört zur Detailansicht von Use Case 2.
- Commit und Pull Request stehen noch aus.

**Welche Konzepte wurden behandelt?**
Mehrere Rückgabewerte als Dictionary; Einheiten im Namen
(`strecke_auto_in_metern`); Runden mit `round()` in Python und `toFixed()` in
JavaScript; Speichern in der Basiseinheit und Umrechnen erst für die Anzeige;
mehrere Spalten in einem `UPDATE`; Umbenennen von Funktionen samt Aufrufen,
Tests und Doku; mit einem Mock prüfen, wie oft eine Funktion aufgerufen wurde
(`assert_called_once()`).

**Eigenleistung und KI-Unterstützung**
Fabio gab den Plan mit den Entscheiden (Meter speichern, Kilometer anzeigen,
Dictionary) frei und erlaubte die Anpassung an Linas Test. Danach wünschte er
möglichst schlanken Code, weil er jede Codestelle erklären können muss, und
wählte aus vier Vorschlägen zwei aus: `raise_for_status()` entfernen und den
eigenen Umrechnungstest in den Test der Speicherroute einbauen. Das Einbauen
der Routenabfrage in die Hauptfunktion liess er sich zuerst im Vergleich
zeigen und gab es danach frei. Er verzichtete auf ein Review durch Lina. Der Agent schrieb
Code, Tests und Doku, prüfte die Anzeige im Browser mit simulierten Antworten
und machte eine echte Abfrage beim Kartendienst.

**Persönliche Reflexion – von Fabio zu ergänzen**
Kann ich erklären, warum die Strecke in Metern gespeichert und erst im
Browser in Kilometer umgerechnet wird?

**Nächster Lernschritt**
Änderungen mit dem Skill `end-coding` committen und als Pull Request
eröffnen; danach US 30003 (Neuberechnung beim erneuten Speichern).

## 2026-10-24 – US 30006 umgesetzt: Arbeitsweg im Stellen-Formular anzeigen

**Was haben wir gemacht?**
Unter der Stellenbeschreibung gibt es einen nur lesbaren Kasten «Arbeitsweg
mit dem Auto» mit Strecke und Fahrzeit. Er ist leer, bis die Stelle
gespeichert ist. Das Formular bleibt nach dem Speichern offen. Ein zweiter
Klick auf «Speichern» meldet «… bereits gespeichert (ID: …) und kann hier
nicht bearbeitet werden.».

- Geändert: `public/index.html` (Kasten, zwei Anzeigewerte, Leeren beim
  Laden, Füllen beim Speichern) und die Meldung in
  `stellenanzeige_speichern()` in `src/app/datenbank.py`.
- Tests: ein angepasster Test von Lina in
  `tests/test_stellenanzeige_speichern.py`. 39 Tests laufen durch.
- Doku: [US 30006](../../Use_cases/Use_Case_3/30006-arbeitsweg-im-formular-anzeigen.md)
  und [Spickzettel](../../Use_cases/Use_Case_3/30006-spickzettel.md).
- Commits `f6cc126` (feat) und `c149ff2` (docs), PR #21 mit Merge-Commit in
  `master`.

**Warum haben wir das gemacht?**
Fabio fiel auf, dass im Formular keine Arbeitsweg-Daten zu sehen sind. Die
Abklärung ergab:

- Die Werte hingen nur an der Bestätigungsmeldung, und das Formular wurde
  nach dem Speichern ausgeblendet.
- Stelle 11 hatte keine Werte, weil sie gespeichert wurde, bevor der Server
  mit dem neuen Code lief.
- Eine gespeicherte Stelle lässt sich heute gar nicht bearbeiten.
  `POST /api/stellenanzeigen` legt nur neue Stellen an, und ein doppelter
  Link bricht vor der Berechnung ab.
- Das Bearbeiten ist für Use Case 2 vorgesehen (ADR 0005, Wireframe mit
  `PUT /api/stellenanzeigen/<id>`). Dazu gibt es aber noch keine
  ausgeschriebene Story.

Betrachtete Alternativen: den Button nach dem Speichern sperren oder gleich
eine `PUT`-Route bauen (Kern von US 30003). Entscheid: nur die Anzeige bauen,
den Button aktiv lassen und stattdessen die Meldung klarer machen.

**Welche Auswirkungen hat das?**
Der Arbeitsweg steht an einem festen Ort im Formular, wie ADR 0005 es
vorsieht. Backend, Berechnung und Datenbank blieben unverändert. Die Anzeige
wurde im Browser geprüft: den doppelten Link mit dem echten Backend, Erfolg
und gescheiterte Berechnung mit simulierten Antworten. Offen:

- Bearbeiten gespeicherter Stellen und Anzeige beim Öffnen (Use Case 2),
  dazu US 30003.
- Stelle 11 hat weiterhin keinen Arbeitsweg.

**Welche Konzepte wurden behandelt?**
`:value` (eine Richtung) gegenüber `v-model` (zwei Richtungen) in Vue, dazu
`readonly`; `fieldset`/`legend` für einen Kasten; Template-Strings in
JavaScript; Unterschied zwischen `POST` (neu anlegen) und `PUT` (bestehenden
Datensatz ersetzen); warum ein doppelter Link das Speichern abbricht, bevor
die Berechnung erreicht wird; Zustand im Frontend zurücksetzen, damit keine
alten Werte stehen bleiben.

**Eigenleistung und KI-Unterstützung**
Fabio bemerkte das Fehlen der Anzeige und fragte, warum ein erneutes
Speichern mit Neuberechnung ein Problem wäre. Er fasste in eigenen Worten
zusammen, dass das Bearbeiten heute nicht möglich ist, und fragte nach einer
passenden geplanten Story. Er legte die Lösung fest (Kasten unter der
Beschreibung, nur lesbar, Button aktiv, Meldung ergänzen) und sprach die
Änderung an Linas Formular mit ihr ab. Er verlangte einen eigenen Branch,
die User Story und den Spickzettel. Er verzichtete auf ein Review und liess
direkt mergen.

Der Agent untersuchte Code und Ursachen (Datenbankabfrage zu Stelle 11,
echte Testberechnung: 44 min / 44.5 km), zeigte Alternativen auf, schrieb
Code, Test, Story und Spickzettel, prüfte im Browser, committete, erstellte
den Pull Request und mergte ihn.

**Persönliche Reflexion – von Fabio zu ergänzen**
Kann ich erklären, warum ein zweiter Klick auf «Speichern» heute nichts neu
berechnet und was es dafür bräuchte?

**Nächster Lernschritt**
Im Team klären, wer Use Case 2 übernimmt. Danach US 30003 mit
`PUT /api/stellenanzeigen/<id>` umsetzen.

### 2026-10-24 – «Failed to fetch»: Absturz des lokalen Servers und Bereich Bugs

**Was haben wir gemacht?**
Beim Testen des aktuellen Stands (zuerst US 30001/30002, nach `git pull`
US 30006) erschien im Browser mehrmals «Failed to fetch», beim Laden einer
Anzeige und beim Speichern. Ablauf:

- Im Browser endeten die Anfragen an `/api/stellenanzeigen/vorschau` und
  `/api/stellenanzeigen` mit `net::ERR_EMPTY_RESPONSE`: Der Server hat gar
  nicht geantwortet.
- Ein Neustart des Servers half zuerst. Nach dem Holen der neuen Version kam
  der Fehler wieder. Im Server-Log stand jetzt die Ursache:
  `objc[…] … fork() was called … Crashing instead.`
- Notlösung: Der Server läuft seither mit
  `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` vor dem gunicorn-Befehl. Danach
  wurde nachgestellt: Codeänderung mit Neuladen, dann vier Anfragen, alle
  korrekt beantwortet.
- Als dauerhafte Lösung wurde `uv run flask --app src/app run --debug --port 5001`
  auf einem Testport geprüft (drei Neuladevorgänge, kein Absturz).
- Neuer Bereich `docs/Use_cases/Bugs/` auf Höhe der Use Cases mit
  [US 90001 – Lokalen Server auf allen Rechnern gleich und stabil starten](../../Use_cases/Bugs/90001-lokalen-server-stabil-starten.md).
  Branch `docs/bugs-lokaler-server`, Pull Request #23, gemergt in `master`.

**Warum haben wir das gemacht?**
Ohne funktionierenden lokalen Server lässt sich keine Story testen. Die
Ursache lag nicht im Code der App: gunicorn startet mit `--reload` nach jeder
Codeänderung einen neuen Worker per `fork()`, und macOS beendet diesen
Worker, sobald er über `requests` ins Internet geht. Zudem läuft gunicorn auf
Windows gar nicht, und im README steht noch der Platzhalter der Vorlage. Das
Team hat also keinen gemeinsamen Startbefehl.

Betrachtete Lösungen: die macOS-Variable dauerhaft setzen (wirkt nur auf
macOS und nur, wenn man daran denkt) oder lokal `flask run` verwenden (läuft
auf allen Betriebssystemen, Online-Version und `Dockerfile` bleiben
unverändert). Entscheid: zuerst eine Story schreiben, die Umstellung erst nach
Absprache im Team umsetzen.

**Welche Auswirkungen hat das?**
Am Code der App hat sich nichts geändert. Bugs und Infrastrukturprobleme
haben jetzt einen eigenen Ort; ihre Stories beginnen mit 9. Offen:

- Absprache mit Lina und Mirko, ob lokal `flask run` verwendet wird.
- Danach ADR 0012, Startbefehl im README und VS-Code-Aufgabe.
- Test des Starts auf einem Windows-Rechner, falls im Team vorhanden.

**Welche Konzepte wurden behandelt?**
«Failed to fetch» bedeutet, dass der Browser keine Antwort bekommen hat; die
Ursache steht meist im Server-Log, nicht im Code. gunicorn mit Master- und
Worker-Prozessen, `fork()` und `--reload`; Umgebungsvariablen vor einem
Befehl; Entwicklungsserver von Flask gegenüber einem Server für den
Online-Betrieb; warum `--debug` nur mit `127.0.0.1` und nie mit
`--host 0.0.0.0` verwendet werden darf. Bei Git: VS Code zeigt die Dateien
des Branches, auf dem der Ordner gerade steht; ein in `master` gemergter PR
erscheint erst nach `git switch master` und `git pull`; Git-Befehle
funktionieren nur im Repository-Ordner (`JobTracker`), nicht im Ordner
darüber («not a git repository»).

**Eigenleistung und KI-Unterstützung**
Fabio testete die App, meldete «Failed to fetch» und fragte, wie sich das in
Zukunft verhindern lässt. Er fragte nach, ob die Umstellung auf Windows
funktioniert und welche Nachteile sie hat. Er entschied, zuerst eine Story zu
schreiben, und legte fest, dass sie in einem eigenen Bereich auf Höhe der Use
Cases steht. Er benannte den Bereich in «Bugs» um und gab Umbenennen des
Branches, Commit, Push, Pull Request und Merge in Auftrag. Er bemerkte, dass
der neue Ordner in VS Code fehlte, und versuchte `git switch master` selbst.

Der Agent untersuchte Browser-Anfragen und Server-Log, startete den Server
neu, prüfte die Lösungen auf Testports, schrieb Bereich und Story, arbeitete
dafür in einer eigenen Arbeitskopie (git worktree), committete, erstellte und
mergte den Pull Request und wechselte den Ordner `JobTracker` auf `master`.

**Persönliche Reflexion – von Fabio zu ergänzen**
Kann ich erklären, warum «Failed to fetch» hier kein Fehler im Code war und
wo ich bei diesem Fehler zuerst nachschaue?

**Nächster Lernschritt**
Mit Lina und Mirko über `flask run` entscheiden und danach US 90001 umsetzen.
