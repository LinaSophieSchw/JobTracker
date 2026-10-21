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

## 2026-10-20 – US 10002: Weitere Importfelder und bearbeitbare Vorschau

**Was haben wir gemacht?**

Auf dem Branch `10002_weitere-importfelder-anzeigen-und-bearbeiten` wurde
die Titelvorschau um Firma, Arbeitsort, Adresse, Pensum und Stellenbeschreibung
erweitert. Grundlage sind US 10002 und Mirkos Datenmodell. Die Vorschau zeigt
alle sechs fachlichen Importfelder bearbeitbar an; die normalisierte URL ist
als Link sichtbar. Es wird noch nichts gespeichert (separate US 10003).

### Vorgehen: erst verstehen, dann Backend und Frontend verbinden

1. **Anzeigeninhalt untersuchen:** Lina rief die Rega-Anzeige mit `requests`
   in der Python-Konsole ab (HTTP 200). BeautifulSoup fand zwei JSON-LD-Blöcke:
   Navigation als `BreadcrumbList` und Stellenangaben als `JobPosting`.
   Mit `json.loads()` wurden die Daten in Python-Werte umgewandelt. Statt die
   lange Beschreibung auszugeben, wurden Feldnamen und relevante Werte geprüft.
2. **Quellen den eigenen Feldern zuordnen:** Firma stammt aus
   `hiringOrganization.name`; Beschreibung aus `description`.
   Die konkrete Anzeige enthält `streetAddress`, `postalCode`,
   `addressCountry` und den Ort in `addressRegion`. Andere Anzeigen können
   `addressLocality` verwenden. Dieser Befund ergänzt Mirkos frühere Beobachtung,
   in der keine standardisierte Strassenangabe gefunden worden war.
   `employmentType` und Wochenstunden wurden nicht als Prozentpensum interpretiert.
3. **Kleine Logikfunktionen ergänzen:** In
   `src/app/stellenanzeige_erfassen.py` wurden Datenblockauswahl und Feldlesen
   getrennt. Jede Hilfsfunktion wurde zunächst mit überschaubaren Beispieldaten
   in der Konsole ausprobiert. Fehlende optionale Angaben bleiben leer.
4. **Pensum gezielt untersuchen:** Eine Suche nach Prozentzeichen fand auch Titel
   und fremde Stellenempfehlungen. Allgemeine CSS-Klassen führten zunächst zum
   Veröffentlichungsdatum. Die Untersuchung des umgebenden Listeneintrags ergab
   `li[data-cy="info-workload"]` als gezielte Fundstelle. Der Selektor wurde an
   zwei Anzeigen manuell ausprobiert und bleibt abhängig vom jobs.ch-Seitenaufbau.
5. **Hauptfunktion ergänzen:** `stellenanzeige_auslesen(url)` normalisiert den
   Link, lädt die Detailseite einmal, wählt den Datenblock zur Stellen-ID und
   verbindet die Hilfsfunktionen. Zurück kommt ein Dictionary mit `url`,
   `titel`, `firma`, `arbeitsort`, `adresse`, `pensum` und
   `stellenbeschreibung`. Der vollständige Abruf wurde in der Konsole bestätigt.
6. **Flask-Route anpassen:** `stellenanzeigen_routes.py` ruft statt der alten
   reinen Titelfunktion die neue Hauptfunktion auf. Die Route prüft weiterhin die
   Eingabe und liefert das gesamte Dictionary als JSON an den Browser.
7. **Frontend erweitern:** In `public/index.html` wurden Vue-Werte in `data()`
   ergänzt. Die Lademethode übernimmt jedes Antwortfeld mit einem leeren Text
   als Ersatz für fehlende Werte. Ein tabellarisch angeordnetes Formular zeigt
   links Labels und rechts Eingabefelder; die Beschreibung verwendet ein
   mehrzeiliges `textarea`. `v-model` verbindet Eingabe und Vue-Wert.
   „Abbrechen“ blendet die Vorschau aus; es ist kein Datenbankspeichern.
8. **Code lesbar strukturieren:** Lina ergänzte Abschnittskommentare für HTML
   und JavaScript sowie innerhalb des Scripts für Vue-Vorbereitung, Daten,
   Methoden und Seitenstart. Besprochen wurden `<!-- -->` in HTML,
   `//` in JavaScript und `#` in Python. Die Datei wurde noch nicht aufgeteilt.

### Funktionen und ihre Verantwortung

| Funktion | Aufgabe |
|---|---|
| `anzeigenlink_bestimmen()` | Link prüfen und auf direkte Anzeigenadresse normalisieren |
| `stellenanzeige_daten_finden()` | Passenden JobPosting-Block auswählen |
| `stellentitel_aus_html_lesen()` | Titel aus der Hauptüberschrift lesen |
| `firma_aus_daten_lesen()` | Firmennamen lesen und äussere Leerzeichen entfernen |
| `ort_und_adresse_aus_daten_lesen()` | Orte sammeln und erste vollständige Schweizer Adresse getrennt liefern |
| `beschreibung_aus_daten_lesen()` | HTML in Text mit Absatzumbrüchen umwandeln; Skript- und Style-Inhalte entfernen |
| `pensum_aus_html_lesen()` | Gekennzeichnetes Pensum lesen, ohne beliebige Prozentwerte zu übernehmen |
| `stellenanzeige_auslesen()` | Abruf und Hilfsfunktionen verbinden; alle Vorschaufelder zurückgeben |

### Gelöste Probleme

- **ImportError in der Konsole:** Nach Ergänzen einer Funktion war in der offenen
  Python-Konsole noch die alte Modulversion geladen. Neustarten der Konsole
  ermöglichte den Import.
- **Neue Formularfelder blieben leer:** Zunächst fehlten Vue-Werte und
  Zuweisungen aus der JSON-Antwort. Diese wurden ergänzt. Anschliessend zeigte
  die Oberfläche noch eine alte Backend-Antwort mit nur Titel und Suchlink.
  Nach einem Waitress-Neustart kamen alle Felder an. Waitress lädt geänderten
  Python-Code nicht automatisch neu; aktualisiertes HTML kann dennoch schon
  sichtbar sein.
- **Zweite Anzeige ohne Kennung:** Ein JobPosting der Helikoptermechaniker-Anzeige
  enthielt weder `identifier` noch `url`. Die kanonische Adresse passte zur
  angefragten ID, und es gab genau einen JobPosting-Block. Ein kontrollierter
  Ersatzweg akzeptiert diese Kombination. Eine fremde Kennung oder mehrere
  kennungslose Anzeigen werden nicht übergangen.
- **Alter Routentest:** Der Test ersetzte noch `stellentitel_auslesen`, während
  die Route nun `stellenanzeige_auslesen` aufruft. Er wurde auf die neue Funktion
  und die vollständige JSON-Antwort umgestellt.
- **Einrückung im Test:** Beim Einfügen entstand ein IndentationError.
  Nach Korrektur der Einrückung konnte pytest die Tests wieder sammeln.
- **Importreihenfolge:** Ruff meldete zwei unsortierte Importblöcke. Die
  automatische Korrektur und Formatierung wurden angeleitet.

**Warum haben wir das gemacht?**

Importierte Angaben sollen vor dem Speichern geprüft und korrigiert werden.
HTML und strukturierte Daten wurden zuerst untersucht, statt Fundstellen zu
erraten. Kleine Funktionen trennen Datenzuordnung, Feldlesen und Netzwerkabruf.
Die Entwicklung erfolgte auf Linas Wunsch zuerst gemeinsam für alle
Backend-Felder und danach für das Frontend, jeweils in erklärten Einzelschritten.

**Welche Auswirkungen hat das?**

Der lokale Ablauf Link → Abruf → vollständige Vorschau → manuelle Bearbeitung
→ Abbrechen wurde von Lina bestätigt. Die bisher ausprobierten Anzeigen
funktionierten nach dem Ersatzweg ebenfalls. Das beweist keine Unterstützung
aller jobs.ch-Anzeigen. Ein neuer Online-Test dieser Story steht noch aus.
Die Eingabefelder sind noch schmal; Textwerte werden dadurch nur optisch
verdeckt, nicht automatisch gekürzt. Der Button heisst im zuletzt gezeigten
Screenshot weiterhin „Informationen laden“; „Link bearbeiten“ war gewünscht.

### Testing: Vorgehen und Ergebnis

Die Konsolenversuche waren zunächst manuelle Funktionstests mit erfundenen
Beispielwerten, später zusätzlich mit echten Anzeigen. Die Browserprüfung
bestätigte den zusammenhängenden Ablauf und die Bearbeitbarkeit.
Automatische Tests verwenden dagegen vorbereitete Daten und simulierte
Verbindungen beziehungsweise Funktionsantworten, keine Live-Aufrufe von
jobs.ch oder Neon.

Der berichtete Teststand entwickelte sich von 11 über 13 und 15 auf
**22 bestandene Tests**. Der letzte ausdrücklich gezeigte vollständige Lauf
meldete `22 passed in 0.92s`. Die damals gezeigte Ruff-Ausgabe enthielt noch
zwei Importfehler. Lina bestätigte danach allgemein den Erfolg; eine separate
vollständige Ausgabe der abschliessenden Ruff-/Black-Prüfung liegt hier nicht vor.
Eine aktuelle Gesamtabdeckung wird deshalb nicht behauptet.

### Übersicht aller 22 automatischen Testfälle

Die Namen entsprechen den am 20.10.2026 gelesenen Testdateien.

| Nr. | Datei | Testfunktion | Geprüftes Verhalten |
|---|---|---|---|
| 1 | test_app.py | `test_status_route_antwortet_mit_ok` | Backendstatus liefert HTTP 200 und Status ok |
| 2 | test_app.py | `test_startseite_wird_ausgeliefert` | Startseite wird ausgeliefert und enthält JobTracker |
| 3 | test_datenbank.py | `test_verbindung_ohne_adresse` | Fehlende DATABASE_URL löst verständlichen Fehler aus |
| 4 | test_datenbank.py | `test_verbindung_uebergibt_adresse` | Adresse und 15-Sekunden-Verbindungstimeout werden an psycopg übergeben |
| 5 | test_datenbank.py | `test_datenbank_status_antwortet_mit_ok` | Simulierte Statusabfrage liefert ok, führt SELECT 1 aus und schliesst Verbindung |
| 6 | test_stellenanzeige.py | `test_titel_wird_aus_hauptueberschrift_gelesen` | Titeltext wird aus h1 mit entfernten äusseren Leerzeichen gelesen |
| 7 | test_stellenanzeige.py | `test_fehlender_titel_wird_gemeldet` | Fehlendes h1 löst ValueError aus |
| 8 | test_stellenanzeige.py | `test_suchlink_wird_in_anzeigenlink_umgewandelt` | jobid aus Suchlink wird zur direkten Detailadresse |
| 9 | test_stellenanzeige.py | `test_fremder_anbieter_wird_abgelehnt` | Nicht unterstützter Anbieter wird abgelehnt |
| 10 | test_stellenanzeige.py | `test_route_liefert_alle_vorschaufelder` | Route liefert HTTP 200 und alle simulierten Vorschauwerte |
| 11 | test_stellenanzeige.py | `test_route_lehnt_leeren_link_ab` | Leerer Link liefert HTTP 400 und Meldung |
| 12 | test_stellenanzeige.py | `test_passende_stellen_id_wird_ausgewaehlt` | Passende Kennung wird trotz vorheriger fremder Anzeige gewählt |
| 13 | test_stellenanzeige.py | `test_anzeige_ohne_kennung_mit_passender_seitenadresse` | Einzelner kennungsloser Block mit passender canonical-URL wird akzeptiert |
| 14 | test_stellenanzeige.py | `test_fremde_stellen_id_wird_abgelehnt` | Fremde Kennung wird auch bei passender canonical-URL nicht ignoriert |
| 15 | test_stellenanzeige.py | `test_mehrere_anzeigen_ohne_kennung_werden_abgelehnt` | Mehrere kennungslose Anzeigen werden als uneindeutig abgelehnt |
| 16 | test_stellenanzeige.py | `test_firma_wird_gelesen` | Firmenname wird gelesen und getrimmt |
| 17 | test_stellenanzeige.py | `test_fehlende_firma_bleibt_leer` | Fehlende Firma wird nicht erfunden |
| 18 | test_stellenanzeige.py | `test_arbeitsort_und_adresse_werden_getrennt` | Samedan und vollständige Schweizer Adresse werden getrennt geliefert |
| 19 | test_stellenanzeige.py | `test_adresse_ohne_strasse_bleibt_leer` | Ort bleibt verfügbar, unvollständige Adresse bleibt leer |
| 20 | test_stellenanzeige.py | `test_beschreibung_enthaelt_text_und_absatzumbrueche` | HTML wird entfernt und Absätze bleiben getrennt |
| 21 | test_stellenanzeige.py | `test_pensum_ignoriert_prozentangaben_anderer_stellen` | info-workload hat Vorrang vor fremden Prozentangaben |
| 22 | test_stellenanzeige.py | `test_fehlendes_pensum_bleibt_leer` | Ohne gekennzeichnetes Feld wird kein fremder Prozentwert übernommen |

### Manuelle Testfälle und Grenzen

| Fall | Ergebnis laut Zusammenarbeit |
|---|---|
| Firma mit Beispieldaten auslesen | Bestätigt |
| Arbeitsort und vollständige Adresse mit Beispieldaten lesen | Bestätigt |
| HTML-Beschreibung in zwei Textabsätze umwandeln | Bestätigt |
| Pensum aus zwei echten Anzeigen lesen | Bestätigt |
| Alle Felder der Rega-Anzeige gemeinsam abrufen | Vollständige Ausgabe bestätigt |
| Andere Datenstruktur ohne identifier verarbeiten | Nach Anpassung als erfolgreich bestätigt |
| Alle sechs Felder im lokalen Browser anzeigen | Screenshot und Bestätigung vorhanden |
| Formularwerte manuell ändern | Von Lina bestätigt |
| Abbrechen blendet Formular aus | Von Lina bestätigt |
| Speicherung und erneutes Lesen in PostgreSQL | Nicht Bestandteil dieser Story; noch offen |
| Erweiterte Vorschau auf Vercel | Noch offen |

Die automatischen Tests decken nicht alle Varianten externer Daten ab.
Unter anderem sind ein kompletter simulierter Netzwerkabruf der Hauptfunktion,
mehrere Arbeitsorte, weitere ungültige Datenformen sowie Browserinteraktionen
noch nicht automatisiert geprüft. Der Routentest simuliert die Hauptfunktion
und beweist daher nicht deren tatsächliche Ausleselogik.

**Welche Konzepte wurden behandelt?**

JSON-LD, Schema.org JobPosting, Dictionaries und Listen, Typprüfungen,
Hilfs- und Hauptfunktionen, gezielte CSS-Selektoren, HTML-Textaufbereitung,
Flask als Backend, Routen als Zuordnung von Adresse und Funktion,
JSON-Antworten, Vue data/methods/mounted, v-model, async/await,
try/catch/finally, getrennte manuelle und automatisierte Prüfungen.
„Hauptfunktion“ bezeichnet hier die zusammenführende Funktion und ist
kein besonderes Python-Schlüsselwort.

**Eigenleistung und KI-Unterstützung**

Lina fügte die erklärten Codebausteine selbst ein, führte Konsolenversuche,
Browserprüfungen und pytest aus, korrigierte Einrückungen und gestaltete
die Abschnittskommentare mit. Sie beschrieb das gewünschte Formular und
brachte Schema.org als Informationsquelle ein. Der Agent untersuchte mit
ihr die Ausgaben, lieferte kommentierte Code- und Testbeispiele und erklärte
die Schichten sowie die Fehlersuche. Er las die aktuellen Dateien zur
Diagnose und erstellte diesen Eintrag auf Wunsch.
Die Aufgabenverteilung bedeutet keinen Nachweis vollständigen selbstständigen
Verständnisses aller verwendeten Konzepte.

**Persönliche Reflexion – von Lina zu ergänzen**

Wie kann ich den Ablauf vom Link über Flask und die Auslesefunktionen bis zum
bearbeitbaren Vue-Feld erklären? Was hat mir beim Unterschied zwischen HTML,
JavaScript und Python geholfen?

**Nächster Lernschritt**

Codequalität abschliessend nachweisen, neue Vorschau auf Vercel prüfen und
den Stand reviewen lassen. Datenmodell/Importdokumentation um die tatsächlich
beobachteten Datenvarianten ergänzen. Danach US 10003 separat umsetzen.

## 2026-10-20 – US 10003: Formularangaben in PostgreSQL speichern

**Was haben wir gemacht?**

Auf dem Branch `10003_stellenanzeige-speichern` wurde die Speicherung der
bereits importierten und manuell bearbeitbaren Angaben ergänzt.
Grundlage blieb das aktuelle `docs/datenmodell.md` mit zwei Tabellen und
je einem zusammenhängenden Feld für Wohn- und Arbeitsadresse. Fabios
noch nicht integrierte Entwürfe wurden auf Linas Wunsch nicht übernommen;
Fahrzeit und Strecke wurden noch nicht als zusätzliche Spalten angelegt.

### Vorgehen vom Tabellenaufbau bis zum Browser

1. **Bestehende Datenbank prüfen:** Eine lesende Abfrage auf
   `information_schema.tables` lieferte für das Schema `public` zunächst
   eine leere Liste. So wurde vor dem Anlegen geprüft, ob Tabellen existieren.
2. **Tabellenstruktur ergänzen:** `tabellen_erstellen()` in
   `src/app/datenbank.py` legt `benutzer` und `stellenanzeigen` an.
   Primärschlüssel, Fremdschlüssel, Pflichtfelder, Maximallängen,
   zulässige Statuswerte und Eindeutigkeit pro Benutzer und URL werden
   durch Datenbankregeln abgesichert. Zeitstempel verwenden `TIMESTAMPTZ`.
   `CREATE TABLE IF NOT EXISTS` verändert keine bereits vorhandene Tabelle.
3. **Demo-Benutzer anlegen:** Der Datensatz mit ID 1, Name „Demo-Benutzer“
   und öffentlicher Beispieladresse wurde eingefügt. Ein erneuter Aufruf
   überschreibt ihn nicht. Lina führte die Funktion in der Python-Konsole
   aus und bestätigte beide Tabellen im Data Editor. Eine zunächst scheinbar
   fehlende Tabelle war nach Prüfung der Tabellenauswahl sichtbar.
4. **Benutzerzuordnung festlegen:** `aktuelle_benutzer_id()` liefert in Version 1
   die ID 1. Die Zuordnung bestimmt das Backend; eine im Formular gesendete
   andere Benutzer-ID wird nicht übernommen. Ohne Login bleibt die Anwendung
   eine gemeinsame Demo, keine getrennte Umgebung für verschiedene Besucher.
5. **Formularwerte prüfen:** `textfeld_pruefen()` entfernt äussere Leerzeichen,
   prüft Texttyp, Pflichtangaben und Maximallänge. Leere optionale Werte werden
   `None` und beim Speichern SQL-NULL. `stellenanzeige_eingaben_pruefen()`
   prüft die sieben übertragenen Felder, normalisiert den jobs.ch-Link und
   prüft bei vorhandener Adresse das vereinbarte Schweizer Adressmuster.
   Das Muster beweist nicht die tatsächliche Existenz einer Adresse.
6. **Speicherfunktion ergänzen:** `stellenanzeige_speichern()` prüft erneut,
   setzt die Benutzer-ID und übergibt Werte über `%s`-Platzhalter getrennt
   vom SQL-Befehl. `RETURNING id` liefert die neue ID. Die Transaktion wird
   beim erfolgreichen Verlassen des Verbindungsblocks bestätigt, bei Fehlern
   zurückgenommen; anschliessend wird die Verbindung geschlossen.
   `ON CONFLICT (benutzer_id, url) DO NOTHING` verhindert doppelte Einträge.
   Bei einem Duplikat wird die bestehende ID abgefragt und verständlich gemeldet.
7. **Speichern unabhängig vom Browser prüfen:** Ein Testeintrag erhielt ID 1.
   Über eine neue Verbindung wurden ID, Benutzerzuordnung, Titel, Firma,
   Arbeitsort und der Standardstatus `gespeichert` erfolgreich zurückgelesen.
   Das bestätigt eine abgeschlossene Transaktion, noch keinen gezielten
   Wiederholungstest nach Serverneustart oder Deployment.
8. **Flask-Route ergänzen:** `POST /api/stellenanzeigen` nimmt JSON entgegen,
   verwendet die Datenbankadresse aus `current_app` und ruft die Speicherfunktion
   auf. Erfolg liefert HTTP 201 und die ID; Eingabefehler und Duplikate HTTP 400.
   Ein `psycopg.Error` wird mit einer allgemeinen Meldung und HTTP 503 beantwortet,
   ohne technische Details an den Browser weiterzugeben.
9. **Vue-Frontend verbinden:** In `public/index.html` kamen `speichert` und
   `erfolgsmeldung` hinzu. Die neue Methode sendet die aktuellen Formularwerte,
   einschliesslich manueller Korrekturen. Erfolg zeigt die ID und blendet die
   Vorschau aus; bei Fehlern bleiben Eingaben sichtbar. Die Buttons werden
   während des Speicherns entsprechend gesperrt. Eine alte Erfolgsmeldung
   wird beim nächsten Abruf entfernt.
10. **Bedienoberfläche prüfen:** Ein zunächst doppelter Abbrechen-Button wurde
    besprochen und die Entfernung des zusätzlichen Blocks angeleitet.
    Der bestehende Rega-Link wurde mit Hinweis auf ID 1 als Duplikat erkannt.
    Ein weiterer Eintrag aus dem Browser war anschliessend mit ID 4 im
    Data Editor sichtbar; Lina bestätigte die Werte. Lücken in IDs sind bei
    abgelehnten Einfügeversuchen normal und bedeuten keinen Datenverlust.

Zusätzlich ergänzte Lina Versionshistorien und Abschnittskommentare.
Die Herkunft des ersten Frontend-Grundgerüsts wurde von ihr als MG angegeben.
HTML-Kommentare blenden die Backendstatus-Anzeige aus, ohne die Prüfung in
JavaScript zu entfernen. Kommentare erscheinen nicht in der gerenderten
Oberfläche, bleiben aber im Seitenquelltext sichtbar.

**Warum haben wir das gemacht?**

Die Vorschau allein hält keine Daten dauerhaft fest. Erst die bewusste
Bestätigung soll einen Datensatz erzeugen. Gemeinsame Prüfungen im Backend
schützen auch bei Anfragen ausserhalb der vorgesehenen Oberfläche.
Die Datenbank ergänzt dies durch eigene Regeln. Eine Übersicht gespeicherter
Stellen wurde mit Blick auf Mirkos Use Case 2 vorerst nicht zusätzlich gebaut.

**Welche Auswirkungen hat das?**

Titel, Firma, Arbeitsort, Adresse, Pensum und Beschreibung können jetzt mit
normalisiertem Link in der verbundenen Neon-Datenbank gespeichert werden.
Status und Zeitstempel erhalten Standardwerte. Lohn, Bewerbungsdatum und
Notizen bleiben ohne weitere Eingaben leer. Die initiale Tabellenerstellung
wurde bewusst manuell ausgeführt; sie ist keine automatische Schema-Migration.
Die Tabellenanlage bedeutet nicht, dass jede zukünftig konfigurierte Neon-Branch
dieselbe Struktur schon besitzt.

### Tests und Prüfungen

Die separate Datei `tests/test_stellenanzeige_speichern.py` enthält elf neue
Tests. Die bisherigen Verbindungstests bleiben in `test_datenbank.py`.
Automatisierte Speichertests simulieren die Datenbank; sie schreiben keine
echten Neon-Datensätze und prüfen nicht die tatsächliche SQL-Ausführung oder
alle Constraints. Die echte Speicherung wurde separat manuell nachgewiesen.

| Testfunktion | Geprüftes Verhalten |
|---|---|
| `test_textfeld_entfernt_aeussere_leerzeichen` | Randabstände werden entfernt |
| `test_optionales_leeres_textfeld_wird_none` | Leere optionale Angaben werden None |
| `test_leeres_pflichtfeld_wird_abgelehnt` | Pflichtfelder dürfen nicht leer sein |
| `test_zu_langes_textfeld_wird_abgelehnt` | Maximallänge wird geprüft |
| `test_formularwerte_werden_bereinigt` | Link normalisiert, Werte bereinigt und fremde Benutzer-ID ignoriert |
| `test_unvollstaendige_adresse_wird_abgelehnt` | Angegebene Adresse muss das vereinbarte Muster erfüllen |
| `test_speicherroute_bestaetigt_neuen_eintrag` | Route übergibt Daten und liefert HTTP 201 mit ID |
| `test_speicherroute_meldet_eingabefehler` | ValueError führt zu HTTP 400 und verständlicher Meldung |
| `test_speichern_liefert_id_und_verwendet_demo_benutzer` | Speicherfunktion liefert ID und verwendet bereinigte Parameter mit Benutzer 1 |
| `test_speichern_meldet_bestehenden_eintrag` | Duplikat enthält bestehende ID; Suche bleibt auf Benutzer begrenzt |
| `test_speicherroute_meldet_datenbankausfall` | Simulierter Ausfall liefert HTTP 503 ohne interne Fehlerdetails |

Die Tests wurden schrittweise von 22 auf 28, 30, 32 und schliesslich
**33 bestandene Tests** erweitert. Fehlende Imports von `Mock` und `app`
führten zwischenzeitlich zu NameError und wurden ergänzt. `MagicMock`
simuliert das Verhalten einer Verbindung im `with`-Block.
Ruff meldete lange Versionszeilen, unsortierte und doppelte Imports;
die Texte wurden umgebrochen und die Imports korrigiert. Bei Black fehlte
zunächst der Zielpfad: Erst `uv run black .` bezieht den Projektordner ein.
Lina bestätigte abschliessend erfolgreiche Tests sowie Ruff und Black.

### Noch offene Nachweise

- Speicherung mit dem neuen Code im Vercel-Preview prüfen; bisher erfolgte
  der Browseraufruf lokal, die Datenbank selbst liegt bei Neon.
- Daten nach einem gezielten Serverneustart beziehungsweise neuen Deployment
  erneut lesen; die neue Verbindung allein ersetzt diesen Nachweis nicht.
- Datenmodell-/README-Hinweise zu SQLite und Schemaänderungen auf den aktuellen
  PostgreSQL-Stand abstimmen.
- Commit, Push und Pull Request für diesen Zwischenstand stehen noch aus.

**Welche Konzepte wurden behandelt?**

DDL mit CREATE TABLE, Primär- und Fremdschlüssel, UNIQUE, CHECK, NULL,
parametrisierte SQL-Abfragen, Transaktionen, RETURNING, Standardwerte,
Zeitstempel, Benutzerzuordnung, Flask-Konfiguration, HTTP 201/400/503,
Vue-Methoden und Anzeigezustände, Mock und MagicMock sowie die Unterschiede
zwischen simuliertem Test und echter Datenbankprüfung.

**Eigenleistung und KI-Unterstützung**

Lina fügte die kommentierten Bausteine selbst ein, korrigierte Klammern,
Einrückungen und Imports, führte die Tabellenanlage und Konsolenprüfungen
aus und testete die Speicherung im Browser. Sie kontrollierte die Daten im
Vercel Data Editor und führte pytest, Ruff und Black aus.
Der Agent lieferte und erklärte die Bausteine und Tests, unterstützte die
Fehlersuche und ergänzte auf Wunsch diesen Learninglog. Er führte in diesem
Schritt keine Tests gegen Neon und keine Commits oder Pushes aus.

**Persönliche Reflexion – von Lina zu ergänzen**

Wie unterscheiden sich Vorschau, Eingabeprüfung, INSERT und bestätigte
Transaktion? Warum bestimmt das Backend die Benutzer-ID und warum reicht
ein erfolgreicher Mock-Test allein nicht zum Nachweis echter Speicherung?

**Nächster Lernschritt**

Den dokumentierten Stand auf dem Feature-Branch sichern, im Vercel-Preview
prüfen und nach Review nach master übernehmen. Die Tabellenübersicht für
Benutzer bleibt mit Use Case 2 abzustimmen; manuelle Neuerfassung folgt
separat mit US 10004.

## 2026-10-21 – Nachtrag zu US 10004: Manuelle Erfassung

Nachträglich dokumentiert am 21.10.2026; die Umsetzung wurde in der
vorherigen Arbeitssitzung am 20.10.2026 besprochen.

**Was haben wir gemacht?**

Auf dem Branch `10004_manuelle-erfassung` wurde in `public/index.html`
der Einstieg „Von Hand erfassen“ ergänzt. Die bestehende Vorschau und
Speicherung werden wiederverwendet; eine zweite Backend-Speicherfunktion
oder eine neue Tabelle waren nicht erforderlich.

1. Der Vue-Wert `manuelle_erfassung` unterscheidet Import und manuellen Modus.
2. `stellenanzeige_manuell_erfassen()` leert die fachlichen Eingabefelder,
   entfernt alte Meldungen und übernimmt einen bereits eingegebenen Link.
   Die Methode blendet das Formular ein, ohne jobs.ch abzurufen.
3. Im manuellen Modus erscheint ein über `v-model` bearbeitbares Linkfeld.
   Nach erfolgreichem Import bleibt der normalisierte Link nur lesbar.
4. Ein neuer Import setzt den manuellen Modus zurück.
5. Der vorhandene Speicherbutton sendet die manuell eingegebenen Werte
   über dieselbe Route und Eingabeprüfung an PostgreSQL.

**Warum haben wir das gemacht?**

Manuelle Bearbeitung nach einem erfolgreichen Import war bereits möglich.
US 10004 ergänzt den davon verschiedenen Einstieg ohne erfolgreichen Import,
beispielsweise wenn ein Inserat nicht ausgelesen werden kann. Dieser Ersatzweg
ist in ADR 0005 vorgesehen. Nach Prüfung von Mirkos Projektunterlagen blieb
die bisherige Vereinbarung bestehen: Auch manuell sind ein unterstützter
jobs.ch-Link, Titel und Firma erforderlich. Erfassung ohne Link wurde als
mögliche Erweiterung diskutiert, aber nicht umgesetzt.

**Welche Auswirkungen hat das?**

Importierte und manuell erfasste Anzeigen verwenden dasselbe Formular,
dieselbe Datenstruktur und dieselben Backend-Regeln. Die Herkunft der
Angaben verändert die Speicherlogik nicht. Die Datenbankstruktur wurde
für diesen Schritt nicht geändert.

**Prüfung und Stand**

Lina bestätigte das Einfügen der Änderungen. Der aktuelle Code enthält
Button, Moduswert, Umschaltmethode und bedingte Linkanzeige. Der Branch ist
lokal mit seinem Remote-Branch verbunden und war vor diesem Nachtrag sauber.
Ein erfolgreicher manueller Speicherversuch speziell über den neuen Einstieg
wurde im Chat nicht ausdrücklich nachgewiesen. Ebenso liegen hier keine
neuen Testausgaben oder ein bestätigter Vercel-Preview-Test für US 10004 vor.
Die vorherigen 33 Tests beziehen sich auf den Stand der Speicher-Story und
beweisen nicht automatisch die neue Browserinteraktion.

**Welche Konzepte wurden behandelt?**

Wiederverwendung eines Formulars, Vue-Anzeigezustand, bedingtes Rendern mit
`v-if` und `v-else`, Datenbindung mit `v-model` sowie `type="button"`, damit
der manuelle Einstieg nicht versehentlich das Importformular abschickt.
Manuelle Erfassung und manuelle Korrektur sind unterschiedliche Abläufe.

**Eigenleistung und KI-Unterstützung**

Lina übernahm die erklärten Frontend-Bausteine selbst und wollte den Stand
manuell über VS Code committen und veröffentlichen. Der Agent lieferte
kommentierte Beispiele, erklärte die Abgrenzung zum Import und entwarf eine
Pull-Request-Beschreibung. Auf Linas Wunsch ergänzt er diesen Nachtrag.
Persönliche Lernerfahrungen werden nicht stellvertretend behauptet.

**Persönliche Reflexion – von Lina zu ergänzen**

Wie ermöglicht ein zusätzlicher Formularmodus einen neuen Ablauf, ohne die
Speicherfunktion zu duplizieren? Warum bleibt der Link bei uns Pflicht?

**Nächster Lernschritt**

Manuellen Einstieg mit Pflichtfeldfehler, erfolgreicher Speicherung,
Abbrechen und anschliessendem Import prüfen; Tests und Codequalität bestätigen.
Den Ablauf ebenfalls im Vercel-Preview testen und mit Mirko für die
Wiederverwendung des Formulars in Use Case 2 abstimmen.

## 2026-10-21 – US 10003a: Adressfelder und Arbeitswegspalten

**Was haben wir gemacht?**

Lina holte den aktuellen Master und eröffnete manuell den Branch
`10003a_erweiterung-der-db`. Grundlage waren das aktualisierte Datenmodell
und Fabios ADR 0008 und 0009. Die Umsetzung erfolgte gemeinsam in kleinen
Schritten; Lina fügte die erklärten Codeblöcke selbst ein.

1. In `src/app/datenbank.py` wurde die Tabellendefinition erweitert.
   `benutzer` erhält `wohnadresse_strasse`, `wohnadresse_postleitzahl` und
   `wohnadresse_ort`. `stellenanzeigen` erhält entsprechend
   `inseratadresse_strasse`, `inseratadresse_postleitzahl` und
   `inseratadresse_ort`. Strasse enthält jeweils auch die Hausnummer.
2. Für den Arbeitsweg wurden die optionalen INTEGER-Spalten
   `fahrzeit_auto_in_minuten` und `strecke_auto_in_metern` ergänzt.
   CHECK-Bedingungen erlauben keine negativen Ergebnisse. NULL bleibt
   möglich, solange keine erfolgreiche Berechnung vorliegt. Die spätere
   Oberfläche rechnet Meter in Kilometer um.
3. Die bestehenden Tabellen wurden zunächst mit `ALTER TABLE ...
   ADD COLUMN IF NOT EXISTS` erweitert. Besprochen wurde, dass
   `CREATE TABLE IF NOT EXISTS` bestehende Tabellen nicht verändert und
   neue Spalten bei ALTER TABLE hinten angehängt werden.
4. In `src/app/stellenanzeige_erfassen.py` liefert
   `ort_und_adresse_aus_daten_lesen()` jetzt Arbeitsort und drei getrennte
   Adressbestandteile. Sie stammen vom ersten Standort mit Strassenangabe.
   Der Arbeitsort bleibt separat; Angaben verschiedener Standorte werden
   nicht zu einer Adresse vermischt. `stellenanzeige_auslesen()` gibt die
   neuen Feldnamen als JSON zurück.
5. Eingabeprüfung und INSERT wurden auf die drei Felder umgestellt.
   Das alte Adress-Prüfmuster wurde entfernt. Texttyp, Bereinigung und
   Maximallängen bleiben gemäss Datenmodell bestehen; die Adresse ist
   optional und wird nicht auf Format oder tatsächliche Existenz geprüft.
   Das INSERT übergibt nun zehn Werte über getrennte SQL-Parameter.
6. In `public/index.html` ersetzen drei Eingabefelder das bisherige
   Adressfeld. Vue-Daten, Leeren bei manueller Erfassung, Übernahme der
   Importvorschau und JSON-Speicheranfrage verwenden dieselben Namen.
7. Nach der Codeumstellung wurden die alten Spalten `adresse` und
   `wohnadresse` aus der Tabellendefinition entfernt. Der Demo-Benutzer
   wird vorläufig weiterhin automatisch angelegt, jetzt mit drei
   Adressbestandteilen. Die Profilerfassung übernimmt Fabio separat.
8. Weil ausschliesslich entbehrliche Testdaten vorhanden waren, löschte
   Lina die Tabellen und legte sie mit der fertigen Definition neu an:
   zuerst `stellenanzeigen`, dann `benutzer` löschen, anschliessend
   `tabellen_erstellen()` aufrufen. Die bisherigen Testeinträge gingen
   dabei bewusst verloren. Das ist kein Vorgehen für erhaltenswerte Daten.

**Gelöste Probleme und Prüfung**

- Ein vom Agenten vorgeschlagener Python-Kommentar mit `#` innerhalb eines
  SQL-Texts verursachte beim Neuanlegen einen PostgreSQL-Syntaxfehler.
  Kommentare innerhalb von SQL verwenden `--`; Lina entfernte die
  betroffenen Kommentare. Die Löschung war bereits bestätigt, während
  der fehlgeschlagene Aufbau zurückgerollt wurde. Nach der Korrektur und
  einem Neustart der Python-Sitzung genügte ein erneutes Anlegen ohne DROP.
- Im Vercel-Dateneditor waren zunächst noch alte Spalten sichtbar.
  Eine Abfrage auf `information_schema.columns`, sortiert nach
  `ordinal_position`, bestätigte die korrekte Struktur. Nach Neuladen
  zeigte auch der Dateneditor die neue Struktur und Reihenfolge.
- Eine falsche Einrückung im Speichertest verhinderte zunächst das
  Einsammeln der Tests. Der assert-Block wurde korrekt eingerückt.
- Die Importtests erwarten vier Rückgabewerte statt einer zusammengesetzten
  Adresse. Der Test ohne Strasse erwartet einen erhaltenen Arbeitsort und
  drei leere Adresswerte. Der bisherige Ablehnungstest wurde durch einen
  Test ersetzt, der unvollständige Adressen erlaubt. Der Speichertest
  prüft die zehn übergebenen SQL-Parameter.
- Lina bestätigte Import und Speicherung über die lokale Webapp sowie
  die getrennten Adresswerte in der Datenbank.
- Abschliessend meldete Linas Terminal: **33 Tests bestanden**, Ruff
  **All checks passed**, Black **8 files would be left unchanged**.
  Diese Tests beweisen noch keine Routenberechnung; diese ist nicht
  implementiert. Ein Deployment dieses Branches ist noch nicht bestätigt.

**Warum haben wir das gemacht?**

Die Datenstruktur soll zu Fabios Arbeitswegberechnung passen. Getrennte
Adressbestandteile vermeiden ein nachträgliches Zerlegen zusammengesetzter
Adressen. Fahrzeit und Strecke erhalten eindeutige Einheiten im Spaltennamen.
Die bisherige einzelne Adresse wurde schrittweise ersetzt, statt sie vor
Anpassung ihrer Aufrufer zu entfernen.

**Welche Auswirkungen hat das?**

Import, Formular und Speicherung verwenden jetzt dieselben drei Adressfelder.
Die Datenbank ist für Fahrzeit und Strecke vorbereitet. Routenaufruf,
Ergebnisanzeige und Profilerfassung bleiben offen und werden mit Fabio
abgestimmt. Alte Anwendungen, die noch `adresse` verwenden, sind mit dem
neuen Schema nicht kompatibel; der neue Code muss deshalb zeitnah über
Review auf Master und anschliessend ins Deployment gelangen.

**Welche Konzepte wurden behandelt?**

Tabellendefinition und Schemaänderung, CREATE TABLE gegenüber ALTER TABLE,
Fremdschlüssel und Löschreihenfolge, Transaktionen und Rollback, NULL gegenüber
0, Einheiten, SQL-Platzhalter, JSON-Feldnamen, Vue-Datenbindung, Python-
Einrückung, Neustart einer Python-Sitzung und zwischengespeicherte Browseransichten.

**Eigenleistung und KI-Unterstützung**

Lina führte Git-Schritte, Codeänderungen, Datenbankbefehle und Tests manuell
aus und bestätigte den Browserablauf. Der Agent las relevante Dateien,
lieferte vollständige kommentierte Codebeispiele, erklärte die Änderungen
und unterstützte bei Fehlersuche und Testanpassungen. Der Agent verursachte
mit einem ungeeigneten SQL-Kommentar selbst einen Fehler und korrigierte
seine Anleitung. Die abschliessenden erfolgreichen Testergebnisse stammen
aus Linas Terminalausgabe.

**Persönliche Reflexion – von Lina zu ergänzen**

Warum verändert CREATE TABLE IF NOT EXISTS keine vorhandene Tabelle?
Wann ist Neuanlegen vertretbar und wann braucht es eine Migration mit
Erhalt bestehender Daten?

**Nächster Lernschritt**

Änderungen samt Lernlog committen, Branch veröffentlichen und nach Review
auf Master übernehmen. Fabio die neuen Feldnamen und den vorläufigen
Demo-Benutzer mitteilen. Nach dem Deployment den Online-Ablauf prüfen.
