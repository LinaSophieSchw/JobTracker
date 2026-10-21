# Minimale Oberfläche mit drei Screens

Datum: 2026-10-20

## Status

Vorgeschlagen.

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

- **Drei Screens:** Übersicht (Startseite), Stellen-Formular für neue und
  bestehende Stellen ([ADR 0005](0005-ein-formular-fuer-erfassen-und-bearbeiten.md))
  und Profil.
- **Übersicht:** reine Liste mit Titel, Firma, Arbeitsort, Status und
  Arbeitsweg. Kein Filter, keine Suche. Ein Klick auf eine Zeile öffnet die
  Stelle.
- **Linkfeld** mit «Informationen laden» sitzt oben im Stellen-Formular, kein
  eigener Screen.
- **Ein Benutzer** ([ADR 0003](0003-benutzer-ohne-login.md)), keine
  Benutzerübersicht.
- **Eine Stelle kann erst erfasst werden, wenn ein Profil existiert.** In der
  Oberfläche ist «+ Neue Stelle» gesperrt, bis das Profil einmal gespeichert
  wurde. Das Profil gilt als erfasst, auch wenn die Adressfelder leer sind.
- **Keine Hinweis- oder Erfolgsmeldungen.** Ein gesperrter Button braucht
  keine Erklärung; nach dem Speichern erscheint einfach die Übersicht.
- **Fehlermeldungen nur, wo Use Case 1 und das Datenmodell sie verlangen**, je
  ein kurzer Satz. Den Wortlaut legt die Person fest, die Use Case 1 umsetzt.
  Fest vorgegeben ist nur die Meldung aus Use Case 3.

  | Fall | Grundlage | Wortlaut |
  |---|---|---|
  | Ungültiger oder nicht unterstützter Link | US 10001, Regel S1 | legt Use Case 1 fest |
  | Titel oder Firma fehlt beim Speichern einer Stelle | US 10003/10004, Datenmodell | legt Use Case 1 fest |
  | Name fehlt beim Speichern des Profils | Datenmodell | legt Use Case 1 fest |
  | Stelle ist schon erfasst | Regel S2, US 10003 | legt Use Case 1 fest |
  | Arbeitsweg nicht berechenbar | [ADR 0008](0008-arbeitsweg-mit-openrouteservice.md) | «Arbeitsweg konnte nicht berechnet werden.» |

  Vor dem Löschen einer Stelle fragt die Oberfläche nach.

## Begründung

Das Team will die Applikation so einfach wie möglich halten. Jede Meldung und
jeder zusätzliche Zustand muss gebaut, getestet und in der Präsentation erklärt
werden. Der Aufwand gehört in Backend, Datenbank und externen Dienst.

## Konsequenzen

- Damit der Button gesperrt werden kann, braucht die Übersicht eine Abfrage, ob
  das Profil existiert. Der Datensatz in `benutzer` entsteht deshalb erst beim
  ersten Speichern des Profils, nicht automatisch beim Anlegen der Tabellen
  (siehe [Datenmodell](../datenmodell.md)).
- Der gesperrte Button ist nur Komfort. Das Backend lehnt das Speichern einer
  Stelle ab, solange kein Profil existiert (Regel B2 im
  [Datenmodell](../datenmodell.md)); der Fremdschlüssel `benutzer_id` sichert
  das zusätzlich in der Datenbank ab.
- Die Stories US 10002 und US 10003 sehen noch eine Bestätigung nach dem
  Speichern und ausführlichere Meldungen vor. Sie passt die Person an, die
  Use Case 1 bearbeitet.
- Das Profil gehört zu Use Case 1: Screen, Name, Wohnadresse in drei Feldern,
  erstes Speichern und die Sperre von «+ Neue Stelle». Das Ändern des Profils
  gehört zu Use Case 2.
- Die Wireframes in [docs/wireframes](../wireframes/README.md) zeigen den
  Stand dieses Entscheids.
