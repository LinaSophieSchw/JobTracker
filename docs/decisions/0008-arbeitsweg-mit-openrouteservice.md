# Arbeitsweg mit OpenRouteService berechnen und speichern

Datum: 2026-10-20

## Status

Angenommen. Ersetzt [ADR 0002](0002-externe-web-api.md). Die Adresssuche
wird durch [ADR 0011](0011-strukturierte-adresssuche.md) präzisiert.

## Kontext

Use Case 3 zeigt zu einer Stelle die Strecke und die geschätzte Fahrzeit von
der Wohnadresse zur Arbeitsadresse. [ADR 0002](0002-externe-web-api.md) hatte
dafür die Google Maps Routes API gewählt und den genauen Ablauf offen gelassen.
Das [Datenmodell](../datenmodell.md) überliess der Person, die Use Case 3
bearbeitet, die Wahl des Verkehrsmittels und ob die Fahrzeit gespeichert wird.

## Betrachtete Optionen

- **Option 1: Google Maps Routes API** (ADR 0002). Braucht ein
  Google-Cloud-Projekt mit eingerichteter Abrechnung.
- **Option 2: OpenRouteService.** Bietet laut Dokumentation eine
  Freitext-Adresssuche mit Länderfilter und eine Routenberechnung für das Auto.

## Entscheidung

Option 2: OpenRouteService. Entschieden von Fabio für Use Case 3.

Festgelegter Ablauf:

- Verkehrsmittel Auto, einfacher Hinweg, ohne Live-Verkehrsdaten.
- Die Adresssuche ist auf die Schweiz beschränkt.
- Jeder Klick auf «Speichern» im Stellen-Formular löst die Berechnung aus,
  bei neuen und bei bestehenden Stellen. Eingaben, das Speichern des Profils
  und das Öffnen einer Stelle lösen keine Berechnung aus.
- Strecke und Fahrzeit werden bei der Stelle gespeichert. Eine erfolgreiche
  Berechnung ersetzt alte Werte.
- Scheitert die Berechnung, wird die Stelle trotzdem gespeichert. Strecke und
  Fahrzeit werden geleert und es erscheint nur «Arbeitsweg konnte nicht
  berechnet werden.».

## Begründung

Die Adresssuche mit Länderfilter und die Autoroute decken den Bedarf von
Use Case 3 ab. Gespeicherte Werte stehen beim Öffnen der Stelle ohne neue
Anfrage zur Verfügung und bleiben für spätere Vergleiche erhalten.
*Weitere Gründe gegenüber Google, z. B. Kosten oder Zugang: von Fabio zu
ergänzen.*

## Konsequenzen

- Neue Spalten in `stellenanzeigen`: `fahrzeit_auto_in_minuten` und
  `strecke_auto_in_metern` (siehe [Datenmodell](../datenmodell.md)). Die
  Oberfläche zeigt Minuten und Kilometer.
- Laut Dokumentation liefert die Route die Strecke in Metern und die Dauer in
  Sekunden. Mit einer echten Antwort bestätigt am 22.10.2026 (Bern–Zug:
  5682 Sekunden, 138 268 Meter).
- Der API-Schlüssel bleibt serverseitig in einer Umgebungsvariable, nie in Git.
  Netzwerkaufrufe erhalten ein Zeitlimit.
- Automatische Tests verwenden simulierte Antworten statt Live-Abfragen.
- Die Felder für Arbeitsadresse und Arbeitsweg gehören zum Formular von
  Use Case 1. Use Case 3 liefert nur die Berechnung.
- Ein API-Zugang bei OpenRouteService ist einzurichten; das Kontingent des
  Gratis-Zugangs ist vor dem Deployment zu prüfen.
