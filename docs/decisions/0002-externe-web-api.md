# Externe Web-API: Google Maps Routes API statt LinkedIn

Datum: 2026-10-17

## Status

Angenommen: Google Maps Routes API wurde als externe Web-API ausgewählt.
Der genaue fachliche Ablauf der Integration wird noch festgelegt.

## Kontext

Im Rahmen der Rücksprache mit den Dozenten wurde geklärt, dass JobTracker
eine externe Web-API verwenden muss. Die API-Auswahl wurde daraufhin überprüft
und die Planung des Projekts angepasst.

Ursprünglich war eine Anbindung an LinkedIn vorgesehen. Nach Recherche kam das
Team zum Ergebnis, dass die für das Vorhaben benötigten API-Zugriffe nicht
hinreichend frei zugänglich sind. LinkedIn bietet zwar bestimmte offene
Berechtigungen an; weitergehende Zugriffe können jedoch eine Freigabe oder
Partnerzulassung voraussetzen. Der konkrete gewünschte Endpunkt wurde in diesem
Entscheid noch nicht benannt. Die Aussage bezieht sich deshalb auf die
Einschätzung der geplanten Integration, nicht auf sämtliche LinkedIn-APIs.

## Betrachtete Optionen

- **LinkedIn-API:** Ursprünglich vorgesehen, nach der Recherche wegen der
  Zugangsbeschränkungen für das geplante Vorhaben verworfen.
- **Google Maps Routes API:** Als Alternative zur Integration einer externen
  Web-API ausgewählt. Ermöglicht Routenberechnungen zwischen Orten.

## Entscheidung

Das Projektteam entscheidet sich nach Anpassung der Projektplanung für die
Google Maps Routes API anstelle der ursprünglich vorgesehenen LinkedIn-Anbindung.
Die Integration soll über das Flask-Backend erfolgen.

## Begründung

Die LinkedIn-Anbindung wird wegen der recherchierten Zugangsbeschränkungen
nicht weiterverfolgt. Mit der Routes API soll stattdessen eine externe
Webdienstfunktion in JobTracker integriert werden.

Eine mögliche Anwendung ist die Berechnung von Fahrtzeit oder Entfernung zu
einem Arbeitsort. Dieser konkrete Anwendungsfall ist noch abzustimmen und
wird hier nicht als bereits beschlossene Funktion dargestellt.

## Konsequenzen

- Die ursprüngliche Planung einer LinkedIn-Integration wird ersetzt. Betroffene
  User Stories und Anforderungen sind bei ihrer weiteren Bearbeitung anzupassen.
- Vor der Umsetzung sind Start und Ziel, Verkehrsmittel und gewünschte
  Ergebnisse festzulegen. Eine interaktive Karte ist nicht automatisch enthalten.
- Für die Nutzung sind die API im Google-Cloud-Projekt, Authentifizierung und
  Abrechnung einzurichten; Kosten und Anfragekontingente sind vorab zu prüfen.
- Zugangsdaten werden serverseitig verwaltet und nicht im Repository gespeichert.
- Fehler und Ausfälle des externen Dienstes müssen abgefangen werden. Automatische
  Tests sollen keine kostenpflichtigen Live-Aufrufe voraussetzen.
- Dieser Entscheid dokumentiert die Auswahl; eine Integration ist damit noch
  nicht implementiert.

Quellen, geprüft am 2026-10-17:

- [LinkedIn: API-Zugang und Berechtigungen](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [Google Maps Routes API: Routenberechnung](https://developers.google.com/maps/documentation/routes/compute-route-over)
- [Google Maps Routes API: Nutzung und Abrechnung](https://developers.google.com/maps/documentation/routes/usage-and-billing)
