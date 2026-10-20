# US 30005 – Arbeitsweg beim erneuten Speichern neu berechnen

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzer möchte ich bei jedem erneuten Speichern eines Inserats den Arbeitsweg anhand der aktuellen Adressen neu berechnen lassen, damit die Ergebnisse zu diesen Adressen passen und eine zuvor fehlgeschlagene Berechnung erneut versucht wird.

## Umfang des ersten Vertical Slice

Nach den Stories 30003 und 30004 den vollständigen Ablauf auch beim erneuten Speichern einer bestehenden Stelle ausführen. Ein entsprechender Speichervorgang wird als vorhanden vorausgesetzt. Die Berechnung verwendet die beim Speichern aktuellen Adressen und ersetzt oder leert die gespeicherten Ergebnisse. Eine Adressbearbeitungsfunktion wird hier nicht umgesetzt; anderweitig umgesetzte Adressänderungen werden beim Speichern berücksichtigt.

Die Felder für die Arbeitsadresse und die Anzeigefelder für Strecke und Fahrzeit im Formular der Stelle gehören zu Use Case 1. Diese Story aktualisiert nur deren Werte beim Speichern.

Gemeinsame Festlegungen für diesen Slice:

- Wohnadresse und Arbeitsadresse werden jeweils über vier getrennte Textfelder erfasst: **Strasse, Hausnummer, Postleitzahl und Ort**.
- Es werden **keine Eingabevalidierungen** vorgenommen: keine Pflichtfeld-, Format-, Längen- oder Plausibilitätsprüfungen.
- **Die Umsetzung einer Funktion zum Bearbeiten gespeicherter Adressen gehört zu einem anderen Use-Case.** Bei jedem Speichern eines Inserats verwendet die Berechnung die für diesen Speichervorgang aktuellen Adressen, auch wenn diese über eine anderweitig umgesetzte Bearbeitungsfunktion geändert wurden.
- **Schweiz ist fest vorgegeben.** Es gibt keine Länderauswahl; die Adresssuche wird auf die Schweiz beschränkt.
- Berechnet werden Strecke und geschätzte Fahrzeit für den **einfachen Hinweg mit dem Auto**, ohne Live-Verkehrsdaten.
- Die Anwendung verwendet **OpenRouteService** zur Adresssuche und Routenberechnung.
- Berechnungen werden ausschliesslich durch den Klick auf **«Speichern» im Inseratsformular** ausgelöst. Eingaben, Profil-Speichern und das Öffnen einer Stelle lösen keine Berechnung aus.
- Scheitert die Arbeitswegberechnung, verhindert dies nicht das Speichern des Inserats. Es erscheint ausschliesslich: **«Arbeitsweg konnte nicht berechnet werden.»**
- Im Studienprojekt werden erfundene Nutzerprofile mit existierenden Beispieladressen ohne Bezug zu realen Personen verwendet.

## Ablauf

1. Der Nutzer öffnet eine bestehende Stelle und klickt auf «Speichern».
2. Das Backend verwendet die aktuell hinterlegte Wohnadresse und die für den Speichervorgang aktuelle Arbeitsadresse. Diese kann aus einer in einem anderen Use-Case umgesetzten Bearbeitungsfunktion stammen.
3. Es führt dieselbe Arbeitswegberechnung wie beim erstmaligen Speichern aus.
4. Bei Erfolg ersetzt es die gespeicherten Ergebniswerte und zeigt sie an.
5. Bei einem Berechnungsfehler leert es beide Ergebniswerte und zeigt den allgemeinen Hinweis; das Inserat bleibt speicherbar.
6. Ein späterer Klick auf «Speichern» startet einen weiteren Versuch.

## Akzeptanzkriterien

- [ ] Jeder Klick auf «Speichern» bei einem bestehenden Inserat löst die Berechnung erneut aus.
- [ ] Verwendet werden die beim Speichern aktuellen Adressen. Das gilt auch, wenn eine Adresse über eine in einem anderen Use-Case umgesetzte Funktion geändert wurde. Die Bearbeitungsfunktion selbst gehört nicht zu dieser Story.
- [ ] Bei erfolgreicher Berechnung ersetzen die neu ermittelten Werte die bisherigen Werte in der Datenbank und in der Anzeige. Sie können zahlenmässig unverändert bleiben.
- [ ] Scheitert die Berechnung, verhindert dies nicht das Speichern des Inserats.
- [ ] Bei einem Berechnungsfehler werden beide bisherigen Ergebniswerte geleert. Stattdessen erscheint der vereinbarte allgemeine Hinweis.
- [ ] Beim nächsten Klick auf «Speichern» wird die Berechnung erneut versucht.
- [ ] Das spätere Öffnen des Inserats zeigt den gespeicherten Zustand und löst keine Berechnung aus.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Den vorhandenen Ablauf zum erneuten Speichern prüfen.
2. Den Berechnungsbaustein aus den bisherigen Stories in diesen Ablauf einbinden.
3. Neue Ergebniswerte beziehungsweise leere Werte bei derselben Stelle speichern.
4. Die Anzeige nach dem Speichern und beim erneuten Öffnen aktualisieren.
5. Erfolg, Fehler mit zuvor vorhandenen Werten und einen weiteren Versuch nach Dienstausfall testen. Zusätzlich mit vorbereiteten geänderten Adressdaten prüfen, dass die Berechnung die aktuellen Angaben verwendet; dafür keine Bearbeitungsfunktion bauen.

## Noch nicht enthalten

- Umsetzung einer Funktion zum Ändern oder Ergänzen gespeicherter Adressen.
- Aufbau einer allgemeinen Inseratsbearbeitung.
- Automatische Wiederholung ohne erneuten Klick auf «Speichern».
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Vor der Umsetzung prüfen, ob der Ablauf zum erneuten Speichern bereits vorhanden ist und wie die Ergebnisse bei derselben Stelle aktualisiert werden. Mit simulierten Antworten prüfen, dass nach einem Berechnungsfehler keine alten Ergebniswerte weiter angezeigt werden und dass die Berechnung die beim Speichern aktuellen Adressen verwendet. Die Schnittstelle zur anderweitig umgesetzten Adressbearbeitung abstimmen. Diese Prüfung und Implementierung stehen noch aus.
