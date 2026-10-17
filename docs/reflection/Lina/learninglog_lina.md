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
