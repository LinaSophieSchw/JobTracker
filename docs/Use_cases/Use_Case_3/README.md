# Use Case 3 – Arbeitsweg berechnen und anzeigen

Stand: 2026-10-20

**Status:** Inhaltlich abgestimmt

## Ziel

Der Nutzer sieht zu einer erfassten Stelle die Streckenlänge und die geschätzte
Fahrzeit mit dem Auto von seiner Wohnadresse zum Arbeitsort. Die gespeicherten
Angaben helfen ihm, den Arbeitsweg einzuschätzen.

Die gespeicherten Werte stehen für spätere Vergleiche zur Verfügung. Die
Umsetzung einer Vergleichsfunktion gehört nicht zu diesem Use Case.

## User Stories

| Reihenfolge | User Story | Stand |
|---|---|---|
| 1 | [US 30001 – Fahrzeit beim erstmaligen Speichern sehen](30001-fahrzeit-beim-ersten-speichern.md) | Geplant |
| 2 | [US 30002 – Zusätzlich die Streckenlänge sehen](30002-streckenlaenge-ergaenzen.md) | Geplant |
| 3 | [US 30003 – Arbeitsweg beim erneuten Speichern neu berechnen](30003-arbeitsweg-beim-erneuten-speichern.md) | Geplant |

**Reserve.** Das Profil mit Wohnadresse und die Felder der Arbeitsadresse im
Stellen-Formular gehören zu Use Case 1. Die beiden folgenden Stories werden nur
verwendet, falls Use Case 1 diese Teile nicht umsetzt:

| User Story | Stand |
|---|---|
| [US 30004 – Wohnadresse erstmalig im Profil hinterlegen](30004-wohnadresse-erstmalig-speichern.md) | Reserve |
| [US 30005 – Arbeitsadresse erstmalig bei einer Stelle hinterlegen](30005-arbeitsadresse-erstmalig-speichern.md) | Reserve |

## Voraussetzungen

- Das Profil mit Wohnadresse aus Use Case 1 ist vorhanden.
- Das Stellen-Formular aus Use Case 1 enthält die Felder für Arbeitsadresse und
  Arbeitsweg.
- Der Nutzer erfasst eine Stelle oder speichert eine bestehende Stelle erneut.
- Für eine erfolgreiche Berechnung liegt eine konkrete Arbeitsadresse vor.
- Im Studienprojekt werden erfundene Nutzerprofile mit existierenden
  Beispieladressen ohne Bezug zu realen Personen verwendet.

## Adressen und Abgrenzung

Wohnadresse und Arbeitsadresse bestehen je aus drei Feldern: Strasse mit
Hausnummer, Postleitzahl und Ort
([ADR 0009](../../decisions/0009-adresse-in-drei-feldern.md)). Es erfolgen
keine Eingabevalidierungen. Die Schweiz ist fest vorgegeben; die Adresssuche
wird auf die Schweiz beschränkt.

| Was | Wo |
|---|---|
| Felder Arbeitsadresse und Arbeitsweg im Stellen-Formular | Use Case 1 |
| Profil mit Wohnadresse erstmalig erfassen | Use Case 1 |
| Arbeitsadresse und Wohnadresse ändern | Use Case 2 |
| Arbeitsweg berechnen, speichern und Fehler behandeln | Use Case 3 |

Beim Speichern einer Stelle verwendet dieser Use Case die dann aktuellen
Adressen, auch wenn sie vorher in Use Case 2 geändert wurden.

## Auslöser

**Der Nutzer klickt im Stellen-Formular auf «Speichern».**

Jeder Klick auf «Speichern» löst die Berechnung mit den für diesen
Speichervorgang aktuellen Adressen aus, mit und ohne Adressänderung. Das blosse
Eingeben von Angaben, das Speichern des Profils und das Öffnen einer Stelle
lösen keine Berechnung aus.

## Normaler Ablauf

1. Der Nutzer erfasst eine Stelle oder speichert eine bestehende Stelle erneut
   über «Speichern».
2. Die Anwendung verwendet die Wohnadresse aus dem Profil und die
   Arbeitsadresse der Stelle.
3. Sie wandelt die Adressen über OpenRouteService in geografische Koordinaten
   um und lässt den einfachen Hinweg mit dem Auto berechnen
   ([ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md)).
4. Sie speichert die Stelle sowie Strecke und Fahrzeit.
5. Sie zeigt die Strecke in Kilometern und die geschätzte Fahrzeit in Minuten
   bei der Stelle an.

Eine erfolgreiche Neuberechnung ersetzt zuvor gespeicherte Ergebnisse. Beim
späteren Öffnen der Stelle werden die gespeicherten Werte angezeigt; dadurch
wird keine neue Berechnung ausgelöst.

## Fehlgeschlagene Berechnung

Scheitert die Arbeitswegberechnung, verhindert dies nicht das Speichern der
Stelle. Kann der Arbeitsweg aus irgendeinem Grund nicht berechnet werden:

- Bleiben Strecke und Fahrzeit leer; allfällige alte Ergebnisse werden entfernt.
- Erscheint nur der Hinweis **«Arbeitsweg konnte nicht berechnet werden.»**
- Werden keine technischen Details oder unterschiedlichen Fehlerursachen
  angezeigt.
- Wird erst beim nächsten Klick auf «Speichern» erneut gerechnet.

## Ausserhalb des Umfangs

- Felder im Stellen-Formular (Use Case 1) und das Ändern von Adressen
  (Use Case 2).
- Eingabevalidierungen in Profil- und Stellen-Formular.
- Benutzeranmeldung.
- Stellensuche, Inseratsimport und Ermitteln der Arbeitsadresse aus dem
  Stellenlink.
- Verwalten des Bewerbungsstatus.
- Eine eigene Vergleichsansicht, Sortierung oder Bewertung von Stellen.
- Live-Verkehrsdaten und verkehrsabhängige Fahrzeitprognosen.
- Andere Verkehrsmittel, Rückweg und alternative Routen.
- Interaktive Karten und Navigation.
- Berechnungen während der Eingabe, automatische Wiederholungsversuche und
  regelmässige Aktualisierungen im Hintergrund.

Die angezeigte Fahrzeit ist eine Schätzung ohne Berücksichtigung der aktuellen
Verkehrslage.
