# Minimale Oberfläche

Datum: 2026-10-20

## Status

Vorgeschlagen.

Geändert am 21.10.2026 (Teambesprechung): In Version 1 gibt es keinen
Profil-Screen. Ein Demo-Benutzer mit Wohnadresse ist fest im System
hinterlegt, «+ Neue Stelle» ist deshalb nie gesperrt
([US 30004](../Use_cases/Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md)).
Die betroffenen Punkte unten sind angepasst.

## Kontext

Die Use Cases standen bisher einzeln nebeneinander. Um zu sehen, welche
Funktionen es braucht und wie sie zusammenhängen, hat Fabio am 20.10.2026
Wireframes und einen klickbaren Prototyp erstellt
([docs/wireframes](../wireframes/README.md)). Das Frontend wird in der
Aufgabenstellung nicht bewertet; es muss die Applikation nur bedienbar machen.

## Betrachtete Optionen

- **Option 1: Ausgebaute Oberfläche** mit Dashboard, Filtern, Hinweisen und
  Bestätigungen. Mehr Komfort, aber mehr Code und mehr Abstimmung.
- **Option 2: Minimale Oberfläche.** Nur was es braucht, um die Funktionen zu
  bedienen.

## Entscheidung

Option 2, vorgeschlagen von Fabio:

- **Zwei Screens in Version 1:** Übersicht (Startseite) und Stellen-Formular
  für neue und bestehende Stellen
  ([ADR 0005](0005-ein-formular-fuer-erfassen-und-bearbeiten.md)). Ein
  Profil-Screen kann später ergänzt werden.
- **Übersicht:** reine Liste mit Titel, Firma, Arbeitsort, Status und
  Arbeitsweg. Kein Filter, keine Suche. Ein Klick auf eine Zeile öffnet die
  Stelle.
- **Linkfeld** mit «Informationen laden» sitzt oben im Stellen-Formular, kein
  eigener Screen.
- **Ein Benutzer** ([ADR 0003](0003-benutzer-ohne-login.md)), keine
  Benutzerübersicht.
- **Der Benutzer ist fest hinterlegt.** Name und Wohnadresse des
  Demo-Benutzers stehen im Code und werden beim Anlegen der Tabellen
  eingefügt. «+ Neue Stelle» ist immer aktiv.
- **Keine Hinweis- oder Erfolgsmeldungen.** Nach dem Speichern erscheint
  einfach die Übersicht.
- **Fehlermeldungen nur, wo Use Case 1 und das Datenmodell sie verlangen**, je
  ein kurzer Satz. Den Wortlaut legt die Person fest, die Use Case 1 umsetzt.
  Fest vorgegeben ist nur die Meldung aus Use Case 3.

  | Fall | Grundlage | Wortlaut |
  |---|---|---|
  | Ungültiger oder nicht unterstützter Link | US 10001, Regel S1 | legt Use Case 1 fest |
  | Titel oder Firma fehlt beim Speichern einer Stelle | US 10003/10004, Datenmodell | legt Use Case 1 fest |
  | Stelle ist schon erfasst | Regel S2, US 10003 | legt Use Case 1 fest |
  | Arbeitsweg nicht berechenbar | [ADR 0008](0008-arbeitsweg-mit-openrouteservice.md) | «Arbeitsweg konnte nicht berechnet werden.» |

  Vor dem Löschen einer Stelle fragt die Oberfläche nach.

## Begründung

Das Team will die Applikation so einfach wie möglich halten. Jede Meldung und
jeder zusätzliche Zustand muss gebaut, getestet und in der Präsentation erklärt
werden. Der Aufwand gehört in Backend, Datenbank und externen Dienst.

## Konsequenzen

- Der Datensatz in `benutzer` entsteht automatisch beim Anlegen der Tabellen
  (Regel B2 im [Datenmodell](../datenmodell.md)). Die Übersicht braucht keine
  Abfrage, ob ein Profil existiert.
- Die Stories US 10002 und US 10003 sehen noch eine Bestätigung nach dem
  Speichern und ausführlichere Meldungen vor. Sie passt die Person an, die
  Use Case 1 bearbeitet.
- Der fest hinterlegte Demo-Benutzer gehört zu Use Case 3 (US 30004). Wer
  einen Profil-Screen übernimmt, ist noch offen; bis dahin gibt es keinen.
- Die Wireframes in [docs/wireframes](../wireframes/README.md) zeigen noch den
  Stand vor dem 21.10.2026 mit Profil-Screen und gesperrtem «+ Neue Stelle».
