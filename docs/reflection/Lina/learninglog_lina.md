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

## 2026-10-19 – PostgreSQL für die Speicherung beim Deployment

**Was haben wir gemacht?**
Für das Deployment auf Vercel wurde Neon PostgreSQL als künftige Datenbank
gewählt. Das Neon-Projekt und der Datenbank-Branch `Test` wurden bereits
eingerichtet. Die Umstellung des Python-Codes ist noch nicht abgeschlossen.

**Warum haben wir das gemacht?**
SQLite kann Daten dauerhaft speichern und eignet sich für die lokale
Entwicklung. Unsere lokale SQLite-Datei innerhalb der Vercel-Laufzeit bietet
jedoch keine verlässliche dauerhafte Speicherung über Aufrufe und Deployments
hinweg. Deshalb soll eine externe PostgreSQL-Datenbank die Daten halten.

**Welche Auswirkungen hat das?**
Die Datenbankverbindung und SQLite-spezifische SQL-Befehle müssen angepasst
werden. Zugangsdaten sollen über Umgebungsvariablen eingebunden werden.
Test- und Produktionsverbindungen müssen noch getrennt zugeordnet und die
Online-Speicherung anschliessend geprüft werden.

**Welche Konzepte wurden behandelt?**
Unterschied zwischen einer lokalen Datenbankdatei und einer extern betriebenen
Datenbank sowie zwischen lokaler Entwicklung und Deployment.

**Eigenleistung und KI-Unterstützung**
Lina richtete Neon anhand der besprochenen Schritte ein und möchte die
Verbindung schrittweise selbst umsetzen. Der Agent erklärte die Einschränkung
der bisherigen Lösung und ergänzte diesen Eintrag auf ihren Wunsch.

**Persönliche Reflexion – von Lina zu ergänzen**
Warum funktioniert unsere lokale Datenbanklösung nicht unverändert auf Vercel?

**Nächster Lernschritt**
Den PostgreSQL-Treiber installieren und die lokale Anwendung zuerst mit dem
Neon-Testbranch verbinden. Die erfolgreiche Verbindung ist noch nachzuweisen.

## 2026-10-20 – Connection String für die Neon-Verbindung

**Was haben wir gemacht?**
Lina öffnete in Neon die Verbindungsdetails des Branches `Test`.
Der Begriff „Connection String“ (Verbindungszeichenfolge) wurde besprochen.
Diese Adresse bündelt Datenbanktyp, Benutzer, Passwort, Server,
Datenbankname und Verbindungsoptionen.

**Warum haben wir das gemacht?**
Python benötigt diese Angaben, um die richtige PostgreSQL-Datenbank
anzusprechen. Ein allgemeines Beispiel ohne echte Zugangsdaten lautet:
`postgresql://BENUTZER:PASSWORT@SERVER/DATENBANK?sslmode=require`.

**Welche Auswirkungen hat das?**
Die echte Adresse gehört lokal in die ignorierte `.env` unter `DATABASE_URL`
und online in die passenden Vercel-Umgebungsvariablen. Sie wird nicht im
Learninglog oder Quellcode dokumentiert. Ein erfolgreicher Verbindungstest
wurde bisher noch nicht bestätigt.

**Welche Konzepte wurden behandelt?**
Connection String, Umgebungsvariablen und Trennung von Zugangsdaten und Code.
Die angezeigten Sternchen maskieren das Passwort; eine tatsächlich verwendete
Verbindungsadresse benötigt das echte Passwort.

**Eigenleistung und KI-Unterstützung**
Lina zeigte die Neon-Verbindungsansicht und bat um Dokumentation.
Der Agent ergänzte eine Erklärung mit Platzhaltern ohne echte Zugangsdaten.

**Persönliche Reflexion – von Lina zu ergänzen**
Welche Angaben stecken im Connection String, und warum bleibt er ausserhalb
des Git-Repositorys?

**Nächster Lernschritt**
Die Verbindung der lokalen Flask-App zum Neon-Testbranch über `SELECT 1`
prüfen, ohne dabei die Verbindungsadresse auszugeben.

## 2026-10-20 – PostgreSQL-Verbindung lokal und auf Vercel geprüft

**Was haben wir gemacht?**
Lina stellte die Verbindungsfunktion von SQLite auf `psycopg` um.
Die Flask-Konfiguration liest `DATABASE_URL`; lokal wird dafür die ignorierte
`.env` geladen. Die Statusroute führt weiterhin `SELECT 1` aus.
Lina bestätigte die Antwort `{"datenbank":"ok"}` lokal und anschliessend
im Vercel-Preview `job-tracker-2gsmno016-swen-hausarbeit.vercel.app`.
Elf automatische Tests bestanden; Ruff und Black meldeten zuletzt keine Fehler.

**Warum haben wir das gemacht?**
Die Anwendung benötigt für Vercel eine externe Datenbankverbindung.
Die bisherigen SQLite-Tests wurden ersetzt: Die neuen Datenbanktests prüfen
die fehlende Adresse, die Übergabe an psycopg sowie Statusabfrage und Schliessen
der Verbindung mit simulierten Objekten. Sie benötigen keine Neon-Zugangsdaten.
Die tatsächliche Verbindung wurde separat manuell geprüft.

**Welche Auswirkungen hat das?**
Die Verbindung funktioniert online, das Speichern von Bewerbungen ist in
diesem Branch noch nicht umgesetzt. Für den Prototyp wurde vorerst eine
gemeinsame Datenbank auf dem Neon-Branch `main` für Vercel vereinbart;
Production wurde zusätzlich zu Preview und Development ausgewählt.
Eine vollständige Trennung der Test- und Produktionsdaten bleibt offen.
Der zuvor erstellte Branch `Test` bleibt bestehen. Welchen Branch die lokale
`.env` aktuell verwendet, wurde nach dieser Vereinfachung nicht abschliessend
bestätigt.

Beim ersten Deployment importierte die App die alte SQLite-Funktion aus
`_vendor/app/datenbank.py`. Relative interne Imports sorgen nun dafür,
dass Module aus demselben Paket geladen werden. Ein weiterer Fehler zeigte
SQLite-Code aus `src/app/datenbank.py`: Die PostgreSQL-Version dieser Datei,
die angepassten Tests und `uv.lock` waren noch nicht im Commit enthalten.
Nach deren Commit und Push funktionierte die Online-Statusabfrage.

**Welche Konzepte wurden behandelt?**
Relative Paketimporte, lokale Arbeitskopie gegenüber Commit und Deployment,
Runtime-Logs, Umgebungsvariablen, simulierte Unittests und manuelle
Integrationstests. Ein „Ready“-Deployment beweist noch keine funktionierende
Datenbankverbindung. Die Reihenfolge der URL-Optionen `sslmode` und
`channel_binding` verändert ihre Bedeutung nicht.

In einem Fehlerprotokoll war eine vollständige Verbindungsadresse sichtbar.
Der Agent erklärte das automatisch erzeugte Datenbankpasswort und empfahl
dessen Zurücksetzen. Eine Änderung der lokalen `.env` wurde von Lina bestätigt;
eine erfolgreiche Passwortrotation samt Aktualisierung aller betroffenen
Verbindungen wurde nicht separat nachgewiesen. Zugangsdaten werden hier
nicht übernommen.

**Eigenleistung und KI-Unterstützung**
Lina übernahm die Codeänderungen selbst, führte Tests, Codeprüfungen, Commits
und Pushes aus, konfigurierte Vercel und zeigte die erfolgreichen Statusantworten.
Der Agent lieferte kommentierte Beispiele, erklärte die Fehlerprotokolle und
verglich lokale Dateien mit dem Git-Stand. Auf Wunsch ergänzt er diesen Eintrag.

**Persönliche Reflexion – von Lina zu ergänzen**
Wie erkenne ich, ob ein Fehler aus meinem lokalen Code, dem Commit oder der
Deployment-Konfiguration stammt?

**Nächster Lernschritt**
Den Pull Request prüfen lassen und nach dem Merge die Verbindung in Production
testen. Danach weitere Felder aus jobs.ch untersuchen und die Speicherung
passend zum vereinbarten Datenmodell aufbauen.
