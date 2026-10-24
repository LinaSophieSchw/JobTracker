# Use Case 3 – Arbeitsweg berechnen und anzeigen

Stand: 2026-10-24

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
| 1 | [US 30004 – Demo-Benutzer mit Wohnadresse fest im System hinterlegen](30004-demo-benutzer-fest-hinterlegen.md) | Umgesetzt (PR #17) |
| 2 | [US 30001 – Fahrzeit beim erstmaligen Speichern sehen](30001-fahrzeit-beim-ersten-speichern.md) | Umgesetzt |
| 3 | [US 30002 – Zusätzlich die Streckenlänge sehen](30002-streckenlaenge-ergaenzen.md) | Umgesetzt |
| 4 | [US 30003 – Arbeitsweg beim erneuten Speichern neu berechnen](30003-arbeitsweg-beim-erneuten-speichern.md) | Geplant |

US 30004 kommt zuerst, weil die Berechnung eine Wohnadresse braucht.

**Reserve.** Die Felder der Arbeitsadresse im Stellen-Formular gehören zu
Use Case 1. Die folgende Story wird nur verwendet, falls Use Case 1 diesen Teil
nicht umsetzt:

| User Story | Stand |
|---|---|
| [US 30005 – Arbeitsadresse erstmalig bei einer Stelle hinterlegen](30005-arbeitsadresse-erstmalig-speichern.md) | Reserve |

## Benutzer und Wohnadresse

Version 1 erfasst keinen Nutzer. Es gibt keine Maske, über die Name oder
Wohnadresse eingegeben werden. Stattdessen ist ein Demo-Benutzer mit `id` 1
fest im System hinterlegt, dem alle erfassten Stellen zugeordnet werden
([US 30004](30004-demo-benutzer-fest-hinterlegen.md),
[ADR 0003](../../decisions/0003-benutzer-ohne-login.md)). Das gilt vorläufig,
bis im Team geklärt ist, wer das Profil anlegen übernimmt
(Teambesprechung vom 21.10.2026). Eine Maske zur Erfassung des Nutzers kann
später ergänzt werden.

## Voraussetzungen

- Der Demo-Benutzer mit Wohnadresse ist fest im System hinterlegt
  ([US 30004](30004-demo-benutzer-fest-hinterlegen.md)).
- Das Stellen-Formular aus Use Case 1 enthält die Felder für Arbeitsadresse und
  Arbeitsweg.
- Der Nutzer erfasst eine Stelle oder speichert eine bestehende Stelle erneut.
- Für eine erfolgreiche Berechnung liegt eine konkrete Arbeitsadresse vor.
- Im Studienprojekt wird für den Demo-Benutzer eine öffentliche
  Beispieladresse ohne Bezug zu realen Personen verwendet.

## Adressen und Abgrenzung

Wohnadresse und Arbeitsadresse bestehen je aus drei Feldern: Strasse mit
Hausnummer, Postleitzahl und Ort
([ADR 0009](../../decisions/0009-adresse-in-drei-feldern.md)). Es erfolgen
keine Eingabevalidierungen. Die Schweiz ist fest vorgegeben; die Adresssuche
wird auf die Schweiz beschränkt.

| Was | Wo |
|---|---|
| Felder Arbeitsadresse und Arbeitsweg im Stellen-Formular | Use Case 1 |
| Demo-Benutzer mit Wohnadresse fest hinterlegen | Use Case 3 (US 30004) |
| Maske zum Erfassen des Nutzers und seiner Wohnadresse | vorläufig keine |
| Arbeitsadresse ändern | Use Case 2 |
| Arbeitsweg berechnen, speichern und Fehler behandeln | Use Case 3 |

Beim Speichern einer Stelle verwendet dieser Use Case die dann aktuellen
Adressen, auch wenn die Arbeitsadresse vorher in Use Case 2 geändert wurde.

## Auslöser

**Der Nutzer klickt im Stellen-Formular auf «Speichern».**

Jeder Klick auf «Speichern» löst die Berechnung mit den für diesen
Speichervorgang aktuellen Adressen aus, mit und ohne Adressänderung. Das blosse
Eingeben von Angaben und das Öffnen einer Stelle lösen keine Berechnung aus.

## Normaler Ablauf

1. Der Nutzer erfasst eine Stelle oder speichert eine bestehende Stelle erneut
   über «Speichern».
2. Die Anwendung verwendet die fest hinterlegte Wohnadresse des
   Demo-Benutzers und die Arbeitsadresse der Stelle.
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
- Eingabevalidierungen im Stellen-Formular.
- Maske zum Erfassen oder Ändern des Nutzers und seiner Wohnadresse.
- Benutzeranmeldung und mehrere Benutzer.
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
