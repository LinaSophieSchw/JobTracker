# PostgreSQL bei Neon statt SQLite

Datum: 2026-10-19 (nachträglich festgehalten am 2026-10-20)

## Status

Angenommen und umgesetzt. Ersetzt den Datenbank-Teil von
[ADR 0001](0001-System_architektur.md).

## Kontext

[ADR 0001](0001-System_architektur.md) wählte SQLite für den lokalen Einstieg
und hielt fest, dass die Speicherlösung vor dem Onlinebetrieb erneut geprüft
wird. Auf Vercel läuft die App als serverlose Funktion. Eine SQLite-Datei in
der Vercel-Laufzeit bietet keine verlässliche dauerhafte Speicherung über
Aufrufe und Deployments hinweg.

## Betrachtete Optionen

- **Option 1: SQLite beibehalten.** Einfach lokal, aber online gehen Daten
  verloren.
- **Option 2: Externe PostgreSQL-Datenbank bei Neon.** Die Daten liegen
  ausserhalb der Vercel-Laufzeit und bleiben erhalten. Verbindung und
  SQL-Befehle müssen angepasst werden.

## Entscheidung

Option 2: PostgreSQL bei Neon, angesprochen mit dem Treiber `psycopg`.
Entschieden und umgesetzt von Lina am 19. und 20.10.2026
(siehe [Learninglog Lina](../reflection/Lina/learninglog_lina.md)).

## Begründung

Die Applikation muss bis Ende der Prüfungssession online erreichbar sein und
gespeicherte Stellenanzeigen behalten. Das geht auf Vercel nur mit einer
Datenbank ausserhalb der Laufzeit.

## Konsequenzen

- Die Verbindungsadresse steht lokal in der ignorierten `.env` unter
  `DATABASE_URL` und online in den Vercel-Umgebungsvariablen, nie in Git.
- Die Datenbanktests verwenden simulierte Objekte und brauchen keine
  Neon-Zugangsdaten. Die echte Verbindung wurde lokal und im Vercel-Preview
  manuell geprüft.
- Die SQLite-spezifischen Hinweise im [Datenmodell](../datenmodell.md)
  (Abschnitte 7 und 8) sind noch nachzuführen.
- Jede Person braucht für die lokale Entwicklung Zugang zu einer
  Neon-Datenbank.
