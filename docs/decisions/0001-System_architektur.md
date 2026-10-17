# Grundarchitektur und Hosting für JobTracker

Datum: 2026-10-17

## Status

Angenommen für die weitere Entwicklung: SQLite wird zunächst lokal verwendet;
Vercel bleibt das vorgesehene Hostingziel. Die Kombination ist noch nicht für
den dauerhaften Onlinebetrieb mit gespeicherten Anwendungsdaten freigegeben.

## Kontext

JobTracker wird im Master-Modul SWEN als Webapplikation entwickelt. Das Team
möchte eine überschaubare Architektur, die sich mit den vorhandenen Kenntnissen
umsetzen und erklären lässt. Am heutigen Tag wurden Hosting und Datenbankwahl
besprochen. Frontend mit Vue über CDN und Backend mit Flask bleiben bestehen.
Die Abstimmung erfolgte im Kontext der Rücksprache mit den Dozenten.

Der gesonderte Entscheid zur externen Web-API steht in
[0002-externe-web-api.md](0002-externe-web-api.md).

## Betrachtete Optionen

### Hosting: Azure Web Apps und Vercel

- **Azure Web Apps (Azure App Service):** Als Hosting-Option betrachtet,
  aber im heutigen Vergleich nicht ausgewählt.
- **Vercel:** Ausgewählt, weil das Team darin eine einfache Möglichkeit sieht,
  die Webapplikation bereitzustellen. Dies ist die Einschätzung des Teams,
  keine Behauptung, dass Vercel grundsätzlich für jede Architektur einfacher ist.

### Datenbank: MySQL und SQLite

- **MySQL:** Relationale Datenbank mit einem separaten Datenbankserver.
- **SQLite:** Ebenfalls relational; speichert die Daten in einer Datei und
  benötigt keinen separaten Datenbankserver. Dies erleichtert den lokalen Einstieg.

Der Wunsch nach einer relationalen Datenbank gilt für beide Optionen und ist
allein kein Unterscheidungsmerkmal. Das Team hat SQLite ausgewählt; die einfache
lokale Einrichtung spricht zusätzlich dafür.

## Entscheidung

Das Projektteam entscheidet sich für:

- **Frontend:** Vue über CDN für Formulare, Listen und Dashboard.
- **Backend:** Flask mit Python für Validierung und Scoring.
- **Datenbank:** SQLite für Bewerbungen und Profildaten.
- **Hosting:** Vercel.

Die Entwicklung wird vorerst auf dieser Grundlage fortgesetzt. Ein Wechsel
des Hostinganbieters oder der Datenbank wird jetzt nicht vorgenommen. Vor dem
Deployment mit echten Anwendungsdaten wird die Speicherlösung erneut geprüft.

## Begründung

Vue über CDN ermöglicht interaktive Oberflächen ohne zusätzlichen
Frontend-Build-Prozess. Flask hält das Backend vollständig in Python und passt
zum überschaubaren Projektumfang. SQLite erfüllt den Wunsch nach relationaler
Datenspeicherung und vereinfacht zunächst die lokale Einrichtung.

Vercel wurde gegenüber Azure Web Apps gewählt, weil das Team dort einen
einfachen Weg zur Bereitstellung erwartet.

## Konsequenzen

- Frontend, Backend und Datenbank werden als getrennte Teile einer gemeinsam
  funktionierenden Anwendung umgesetzt.
- Flask kann auf Vercel betrieben werden; die lokale SQLite-Datei kann dort
  jedoch nicht als dauerhaft beschreibbare Anwendungsdatenbank eingeplant werden.
- **Bekanntes Speicherrisiko:** Online gespeicherte Bewerbungen oder Profildaten
  könnten bei Verwendung ungeeigneten lokalen oder temporären Speichers verloren
  gehen. Eine lokal funktionierende SQLite-Datenbank beweist deshalb nicht,
  dass die Speicherung auf Vercel dauerhaft funktioniert.
- Vor dem Deployment muss eine dauerhafte Speicherlösung festgelegt und geprüft
  werden. Falls sie nicht zur gewählten Architektur passt, muss die Datenbank-
  oder Hostingentscheidung erneut betrachtet und dokumentiert werden.
- Bei dieser Prüfung muss ein gespeicherter Eintrag auch nach einem Neustart
  und einem erneuten Deployment erhalten bleiben. Falls das mit der geplanten
  Lösung nicht gewährleistet werden kann, wird ein anderer Hostinganbieter oder
  eine geeignete extern betriebene Datenbank gewählt.
- Die Auswahl von Vercel und SQLite ist damit dokumentiert, ihre gemeinsame
  Einsatzfähigkeit im Deployment ist noch nicht nachgewiesen.
- Scoring-Regeln, Datenmodell und automatisches Deployment sind noch umzusetzen.
- Dieses Dokument verändert keinen Anwendungscode und richtet keine Dienste ein.

Technische Quellen, geprüft am 2026-10-17:

- [Flask auf Vercel](https://vercel.com/docs/frameworks/backend/flask)
- [SQLite auf Vercel und Grenzen der Speicherung](https://vercel.com/kb/guide/is-sqlite-supported-in-vercel)
