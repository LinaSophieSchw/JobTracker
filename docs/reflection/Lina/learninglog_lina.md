# Learninglog – Lina

## 2026-10-17 – Architekturentscheid dokumentieren

**Was haben wir gemacht?**
Die Architekturfolie und die neu mitgeteilte Web-API-Vorgabe wurden in
`docs/decisions/0001-architektur-und-web-api.md` in deutscher Sprache dokumentiert.

**Warum haben wir das gemacht?**
Technische Entscheidungen und offene Fragen sollen für das Team und die spätere
Reflexion nachvollziehbar bleiben.

**Welche Auswirkungen hat das?**
Vue über CDN, Flask, SQLite und Google Maps Routes API sind als Arbeitsstand
festgehalten. Hosting, API-Anwendungsfall und endgültige Teambestätigung bleiben
offen. Die Anwendung wurde dadurch nicht verändert.

**Welche Konzepte wurden behandelt?**
Markdown als Dokumentformat, Entscheidungsprotokolle, Trennung von Frontend,
Backend und Datenbank sowie die Anbindung eines externen Webdienstes.

**Eigenleistung und KI-Unterstützung**
Lina lieferte die Architekturfolie, die Information zur zusätzlichen Vorgabe und
die API-Auswahl und beauftragte die Dokumentation. Der Agent formulierte den
Entscheid, stellte Alternativen gegenüber und hielt Unsicherheiten fest.
Weitere Teambeiträge sind in diesem Chat nicht belegt.

**Persönliche Reflexion – von Lina zu ergänzen**
Warum hilft es, einen Architekturvorschlag von einer bestätigten Entscheidung
zu unterscheiden?

**Nächster Lernschritt**
Den dokumentierten Arbeitsstand im Team prüfen und den konkreten Nutzen der
Routenberechnung sowie die Hosting-Anforderungen klären.

### Ergänzung: Entscheidungen präzisiert und API separat dokumentiert

Die heutige Darstellung wurde anhand der Rückmeldung berichtigt: Vercel wurde
gegenüber Azure Web Apps gewählt, SQLite gegenüber MySQL. Beide Datenbanken
sind relational. Der Entscheid zur externen API liegt jetzt separat unter
`docs/decisions/0002-externe-web-api.md`: Die geplante LinkedIn-Integration wurde
nach Recherche wegen der Zugriffsbedingungen verworfen und durch Google Maps
Routes API ersetzt. Die Rücksprache mit den Dozenten wird als Kontext benannt.

Der Agent überarbeitete die Dokumente und prüfte Herstellerdokumentation.
Dabei wurde als offener technischer Punkt festgehalten, dass eine lokale
SQLite-Datei auf Vercel keine dauerhafte beschreibbare Datenspeicherung bietet.
Die Entscheidungen wurden dokumentiert, nicht technisch umgesetzt.

Persönliche Reflexionsfrage: Wie beeinflussen Zugangsbedingungen eines externen
Dienstes und Hosting-Einschränkungen unsere ursprünglich geplante Lösung?
Persönliche Antwort noch offen.

### Ergänzung: Mit SQLite weiterarbeiten, Hostingfrage bewusst offenhalten

Lina entschied, die Entwicklung zunächst mit SQLite und Vercel als Hostingziel
fortzusetzen und das Speicherrisiko ausdrücklich dokumentieren zu lassen. Der
Agent ergänzte den Architekturentscheid: Lokal kann SQLite weiterverwendet
werden; vor dem Onlinebetrieb muss dauerhafte Speicherung auch über Neustarts
und erneute Deployments hinweg gewährleistet sein. Andernfalls ist ein Wechsel
des Hostings oder der Datenbank nötig. Ein technischer Wechsel wurde nicht
vorgenommen. Persönliche Erkenntnisse dazu wurden noch nicht formuliert.

## 2026-10-18 – SQLite lokal einrichten und testen

**Was haben wir gemacht?**
Auf dem Branch `SQLite` wurde die lokale Datenbankanbindung vorbereitet:
`/instance/` in `.gitignore` ausgeschlossen, der Datenbankpfad in
`src/app/__init__.py` konfiguriert und die Funktion `verbindung_oeffnen()`
in `src/app/datenbank.py` ergänzt. Die Route `/api/datenbank/status`
prüft die Verbindung mit `SELECT 1` und liefert `{"datenbank":"ok"}`.
Lina bestätigte das Ergebnis durch einen Screenshot im Browser.

In `tests/test_datenbank.py` wurden zwei automatische Tests ergänzt:
einer für die Verbindungsfunktion und einer für die Flask-Statusroute.
Lina bestätigte zunächst den erfolgreichen Lauf der Datenbanktests und danach
auch den Gesamttest mit den erwarteten vier erfolgreichen Tests. Die vollständige
Terminalausgabe des Gesamttests wurde im Chat nicht übermittelt.

**Warum haben wir das gemacht?**
Die Bewerbungserfassung braucht später eine Datenbank. SQLite ermöglicht
den lokalen Einstieg ohne separaten Datenbankserver. Automatische Tests
sollen Änderungen an Verbindung und Statusroute überprüfbar machen.

**Welche Auswirkungen hat das?**
Die SQLite-Datei wird bei Bedarf lokal unter `instance/jobtracker.db` erstellt.
Sie enthält noch keine Bewerbungstabelle und wird nicht über Git geteilt.
Die Verbindung wird mit `closing` nach jeder Prüfung geschlossen.
Die dauerhafte Datenspeicherung auf Vercel bleibt weiterhin ungeklärt.

**Welche Konzepte wurden behandelt?**
SQL als Abfragesprache und SQLite als Datenbanksystem; Trennung von Code und
lokalen Daten; Pfadberechnung mit `Path` und `parents[2]`; Python-Standardbibliothek
gegenüber zusätzlich installierten Paketen; Flask-Routen und Serverneustart.
Beim Testen wurden pytest, `assert`, temporäre Ordner mit `tmp_path` und die
vorübergehende Konfigurationsänderung mit `monkeypatch` besprochen.
Die Tests prüfen echte SQLite-Zugriffe; der Routentest prüft zusätzlich das
Zusammenspiel mit Flask. Sie belegen noch keine Speicherung von Bewerbungen
über Neustarts oder Deployments hinweg.

**Eigenleistung und KI-Unterstützung**
Lina erstellte den Branch selbst, übernahm die Codevorschläge, ergänzte
Kommentare, startete den Server und führte die Prüfungen aus. Sie fragte
unter anderem nach Ordnernamen, Pfadberechnung, Imports und pytest.
Der Agent lieferte Code und Testvorschläge, erklärte die Schritte und half bei
der zunächst auftretenden 404-Meldung. Der spätere erfolgreiche Aufruf ist
belegt; die genaue Ursache der vorherigen 404-Meldung wurde nicht abschliessend
nachgewiesen.

**Persönliche Reflexion – von Lina zu ergänzen**
Was kann ich durch die Browserprüfung nachweisen, und was prüfen die
automatischen Tests zusätzlich? Welche Teile kann ich bereits selbst erklären?

**Nächster Lernschritt**
Codequalität und Formatierung prüfen und das SQLite-Grundgerüst als
Zwischenstand sichern. Danach das Datenmodell für die Erfassung eines
Stellenlinks festlegen.

## 2026-10-18 – Dokumentation nach ihrem Zweck einordnen

**Was haben wir gemacht?**
Die Ablage der Projektdokumentation wurde anhand dieser Übersicht erklärt:

- **`docs/user-stories/`**: Was soll die Anwendung können?
- **`docs/decisions/`**: Warum haben wir eine bestimmte Lösung gewählt?
- **`docs/reflection/`**: Was haben wir dabei gemacht und gelernt?

**Warum haben wir das gemacht?**
Anforderungen, Entscheidungsbegründungen und persönliche Lernerfahrungen sollen
klar unterscheidbar und für das Team auffindbar sein. User Stories können
als Markdown-Dateien im Repository geführt werden; GitHub Issues sind dafür
nicht erforderlich.

**Welche Auswirkungen hat das?**
Die erste User Story liegt unter
`docs/user-stories/00001-stellenlink-erfassen.md`. Sie beschreibt den gewünschten
Ablauf und die Akzeptanzkriterien, ohne eine technische Umsetzung zu behaupten.
Architekturentscheidungen und Learninglogs bleiben in ihren eigenen Ordnern.

**Welche Konzepte wurden behandelt?**
Unterscheidung zwischen Anforderung (User Story), begründetem Entscheid
(Decision Record) und Dokumentation des Lernprozesses (Learninglog).

**Eigenleistung und KI-Unterstützung**
Lina wünschte eine Dokumentation unter `docs` statt in GitHub Issues und bat
um die Aufnahme der Übersicht ins Learninglog. Der Agent schlug die Aufteilung
vor und erstellte die erste User-Story-Datei.

**Persönliche Reflexion – von Lina zu ergänzen**
Woran erkenne ich, ob eine Information in eine User Story, einen Entscheid
oder mein Learninglog gehört?

**Nächster Lernschritt**
Den Abruf des Stellentitels für die erste User Story technisch prüfen.

## 2026-10-18 – Stellenlink laden und Titelvorschau anzeigen

**Was haben wir gemacht?**
Auf dem Branch `Bewerbung_erfassen_per_Link` wurde die erste Titelvorschau
umgesetzt. Requests lädt eine jobs.ch-Anzeige, Beautiful Soup liest ihre
Hauptüberschrift. Direkte Links und Suchlinks mit jobid werden geprüft und
auf einen direkten Anzeigenlink vereinheitlicht. Ein Flask-Blueprint stellt
`POST /api/stellenanzeigen/vorschau` bereit. Das Vue-Formular zeigt den Titel
bearbeitbar an. Lina bestätigte den Abruf zuerst in der Python-Konsole und
danach im Browser auf Port 8081.

**Warum haben wir das gemacht?**
Der erste Vertical Slice beginnt mit Link und Titel. Download, Auslesen und
Verarbeitung der Browseranfrage liegen in getrennten Funktionen und Dateien,
so dass sie nachvollziehbar und einzeln prüfbar bleiben.

**Welche Auswirkungen hat das?**
Die Titelvorschau funktioniert für die ausprobierte Anzeige. Es wird noch
keine Stelle gespeichert; Speichern und Übersicht sind die nächsten Schritte.
Zunächst kam HTML statt JSON zurück: Die laufende Anwendung auf Port 8080
antwortete mit HTTP 405, obwohl ein frisch geladenes Flask die POST-Route
auflistete. Auf Port 8081 funktionierte der aktuelle Stand. Dies spricht für
einen älteren Serverprozess auf 8080; dessen Identität wurde nicht abschliessend
geprüft. Die bisherige SQLite-Anbindung bleibt lokal.

**Welche Konzepte wurden behandelt?**
Python-Pakete und pyproject.toml; Requests und Beautiful Soup; HTML-Überschriften;
Linkprüfung und UUID; Flask-Routen, POST und JSON; Blueprints als Sammlung
zusammengehöriger Routen; Vue data, methods, v-model, fetch und async/await.
Die User Story liegt tatsächlich unter `docs/user_stories/00001-stellenlink-erfassen.md`;
dies präzisiert den zuvor im Log genannten Ordnernamen mit Bindestrich.

**Eigenleistung und KI-Unterstützung**
Lina legte Dateien an, übernahm und kommentierte die Codevorschläge, ergänzte das
Formular und probierte Konsole und Browser aus. Der Agent lieferte die Bausteine,
erklärte ihre Aufgaben, prüfte die Fehlerantwort und ergänzte automatisierte
Tests für Titelerkennung, Linkprüfung und Vorschau-Route ohne Live-Abrufe.

**Persönliche Reflexion – Lina**
Lina möchte Flask später noch besser verstehen. Routen und Blueprints wurden
besprochen; vollständiges Verständnis wird nicht vorausgesetzt.
Offene Frage: Wie gelangt der Formularlink über die Route zur Auslesefunktion
und als Titel zurück ins Frontend?

**Nächster Lernschritt**
Nach der Pause Link und bestätigten Titel in SQLite speichern und gespeicherte
Einträge anzeigen. Die User Story ist noch nicht abgeschlossen.

## 2026-10-18 – Stellenanzeige in SQLite speichern

**Was haben wir gemacht?**
Auf dem Branch `stellenanzeige_speichern` wurden in `src/app/datenbank.py`
die Funktionen `tabellen_erstellen()` und `stellenanzeige_speichern()` ergänzt.
Die Tabelle `stellenanzeigen` enthält ID, URL und Titel. Lina erstellte die
Tabelle in der Python-Konsole, prüfte die Spalten mit `PRAGMA table_info`,
speicherte einen Testeintrag und bestätigte das Zurücklesen über eine neue
Verbindung.

In `src/app/stellenanzeigen_routes.py` wurde `POST /api/stellenanzeigen`
ergänzt. Die Route prüft Link und Titel, legt die Tabelle bei Bedarf an und
liefert nach dem Speichern die ID mit HTTP 201 zurück. Das Vue-Frontend in
`public/index.html` erhielt einen Speicherbutton, eine Speicherfunktion sowie
Lade- und Erfolgsmeldungen. Der Browser bestätigte einen Eintrag mit ID 2.

**Warum haben wir das gemacht?**
Die Titelvorschau soll erst nach ausdrücklicher Bestätigung gespeichert werden.
Parametrisierte SQL-Abfragen trennen Nutzereingaben vom SQL-Befehl. `commit()`
bestätigt die Änderung; `closing` schliesst die Verbindung anschliessend.

**Welche Auswirkungen hat das?**
Link und Titel können nun lokal über die Webseite gespeichert werden. Die
Übersicht auf der Webseite fehlt noch. Ein erneuter Abruf der Daten über eine
neue Verbindung wurde bestätigt; ein gezielter Nachweis nach Serverneustart
und automatische Tests der neuen Speicherfunktion stehen noch aus.
Die früheren zehn erfolgreichen Tests beziehen sich auf den Vorschau-Zwischenstand,
nicht auf die neu hinzugefügte Speicherung. Das Vercel-Speicherthema bleibt offen.

Beim ersten Browserversuch kam erneut HTML statt JSON zurück. Beide Routen
wurden mit dem Flask-Befehl zur Routenauflistung nachgewiesen. Nach der
Anleitung zum Stoppen älterer Server und Neustarten eines einzelnen Servers
auf Port 8081 bestätigte Lina die erfolgreiche Speicherung. Die genaue
Prozessursache wurde nicht abschliessend nachgewiesen.

**Welche Konzepte wurden behandelt?**
Tabellenstruktur, Primärschlüssel, NOT NULL, CREATE TABLE IF NOT EXISTS,
INSERT mit Platzhaltern, SELECT, commit, lastrowid und current_app.
Eine SQLite-Datei ist binär und benötigt zur tabellarischen Ansicht ein
geeignetes Werkzeug. Lokal ist `qwtel.sqlite-viewer` (Version 26.9.1)
installiert; die optionale Erweiterung und ihre Verwendung wurden in der
README dokumentiert. Die tatsächliche Tabellenansicht in der Erweiterung
wurde im Chat noch nicht bestätigt.

**Eigenleistung und KI-Unterstützung**
Lina übernahm die erklärten Codebausteine selbst, führte die Konsolenprüfungen
aus und testete den Formularablauf. Der Agent lieferte und erklärte die
Bausteine, unterstützte die Fehlersuche und ergänzte auf Wunsch README und
Learninglog. Neue automatische Speichertests wurden nicht ungefragt erstellt.

**Persönliche Reflexion – von Lina zu ergänzen**
Woran erkenne ich den Unterschied zwischen einer angezeigten Vorschau und
einem tatsächlich gespeicherten Datensatz? Flask bleibt ein offener
Vertiefungspunkt aus dem vorherigen Eintrag.

**Nächster Lernschritt**
Gespeicherte Einträge auf der Webseite anzeigen, Speicherung nach Neustart
prüfen und gemeinsam automatische Speichertests ergänzen. Danach Codeprüfung,
Formatprüfung sowie manueller Commit und Push.
