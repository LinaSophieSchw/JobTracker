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
