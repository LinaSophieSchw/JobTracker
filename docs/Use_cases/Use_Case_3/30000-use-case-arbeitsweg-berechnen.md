# Use-Case 3: Arbeitsweg berechnen und anzeigen

**Status:** Inhaltlich abgestimmt

## Ziel

Der Nutzer sieht zu einer erfassten Stelle die Streckenlänge und die geschätzte Fahrzeit mit dem Auto von seiner Wohnadresse zum Arbeitsort. Die gespeicherten Angaben helfen ihm, den Arbeitsweg einzuschätzen.

Die gespeicherten Werte stehen für spätere Vergleiche zur Verfügung. Die Umsetzung einer Vergleichsfunktion gehört nicht zu diesem Use-Case.

## Voraussetzungen

- Die grundlegende Profil- und Inseratserfassung ist vorhanden.
- Die Wohnadresse wird vor der ersten Arbeitswegberechnung im Profil hinterlegt.
- Der Nutzer erfasst ein Inserat oder speichert ein bestehendes Inserat erneut.
- Für eine erfolgreiche Berechnung liegt eine konkrete Arbeitsadresse vor.
- Im Studienprojekt werden erfundene Nutzerprofile mit existierenden Beispieladressen ohne Bezug zu realen Personen verwendet.

## Adresserfassung und Abgrenzung

Die ergänzenden Adress-Stories umfassen die erstmalige Erfassung und Speicherung der Wohnadresse und der Arbeitsadresse. Beide Adressen werden jeweils über vier getrennte Textfelder erfasst: Strasse, Hausnummer, Postleitzahl und Ort.

Es erfolgen keine Eingabevalidierungen: keine Pflichtfeld-, Format-, Längen- oder Plausibilitätsprüfungen. Schweiz ist fest vorgegeben; die Adresssuche wird auf die Schweiz beschränkt.

**Die Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressen gehört zu einem anderen Use-Case – sowohl im Profil als auch beim Inserat. Dies schliesst die Verwendung anderweitig geänderter Adressangaben für die Berechnung nicht aus.**

Was das Speichern einer Profiländerung unmittelbar auslöst, gehört zu einem anderen Use-Case. Beim nächsten Speichern eines Inserats verwendet dieser Use-Case jedoch die dann aktuellen Adressen.

## Auslöser

**Der Nutzer klickt im Inseratsformular auf «Speichern».**

Jeder Klick auf «Speichern» im Inseratsformular löst die Berechnung mit den für diesen Speichervorgang aktuellen Adressen aus. Das gilt mit und ohne Adressänderung. Eine Bearbeitungsfunktion kann aus einem anderen Use-Case stammen und wird hier nicht umgesetzt. Das blosse Eingeben von Angaben löst keine Berechnung aus.

## Normaler Ablauf

1. Der Nutzer erfasst das Inserat oder speichert ein bestehendes Inserat erneut über «Speichern».
2. Die Anwendung verwendet die aktuell hinterlegte Wohnadresse aus dem Profil und die für diesen Speichervorgang aktuelle Arbeitsadresse. Auch Änderungen aus einer in einem anderen Use-Case umgesetzten Bearbeitungsfunktion werden dabei berücksichtigt.
3. Sie wandelt die Adressen über OpenRouteService in geografische Koordinaten um und lässt den einfachen Hinweg mit dem Auto berechnen.
4. Sie speichert das Inserat sowie die berechnete Strecke und Fahrzeit bei der zugehörigen Stelle.
5. Sie zeigt die Strecke in Kilometern und die geschätzte Fahrzeit in Minuten bei der Stelle an.

Eine erfolgreiche Neuberechnung ersetzt zuvor gespeicherte Ergebnisse. Beim späteren Öffnen der Stelle werden die gespeicherten Werte angezeigt; dadurch wird keine neue Berechnung ausgelöst.

## Fehlgeschlagene Berechnung

Scheitert die Arbeitswegberechnung, verhindert dies nicht das Speichern des Inserats.

Kann der Arbeitsweg aus irgendeinem Grund nicht berechnet werden:

- Bleiben Strecke und Fahrzeit leer; allfällige alte Ergebnisse werden entfernt.
- Erscheint der Hinweis **«Arbeitsweg konnte nicht berechnet werden.»**
- Werden keine technischen Details oder unterschiedlichen Fehlerursachen angezeigt.
- Wird erst beim nächsten Klick auf «Speichern» erneut gerechnet.

## Ergebnis

Das Inserat ist gespeichert. Bei erfolgreicher Berechnung sind Strecke und geschätzte Fahrzeit dauerhaft bei der Stelle hinterlegt und sichtbar. Andernfalls erscheint der einheitliche Hinweis.

## Gehört zum Umfang

- Wohn- und Arbeitsadresse erstmalig über vier getrennte Textfelder erfassen, speichern und anschliessend anzeigen.
- Vorhandene Wohn- und Arbeitsadresse verwenden.
- Adressen in Koordinaten umwandeln und den Arbeitsweg mit OpenRouteService berechnen.
- Strecke und Fahrzeit speichern und anzeigen.
- Die Berechnung mit jedem Klick auf «Speichern» auslösen.
- Fehlgeschlagene Berechnungen einheitlich behandeln.

## Ausserhalb des Umfangs

- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Wohn- und Arbeitsadressen. Die Neuberechnung beim Speichern eines Inserats bleibt Bestandteil dieses Use-Cases.
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Aufbau der gesamten Profilverwaltung und Benutzeranmeldung.
- Stellensuche, Inseratsimport und Ermitteln der Arbeitsadresse aus dem Stellenlink.
- Verwalten des Bewerbungsstatus.
- Eine eigene Vergleichsansicht, Sortierung oder Bewertung von Stellen.
- Live-Verkehrsdaten und verkehrsabhängige Fahrzeitprognosen.
- Andere Verkehrsmittel, Rückweg und alternative Routen.
- Interaktive Karten und Navigation.
- Berechnungen während der Eingabe, automatische Wiederholungsversuche und regelmässige Aktualisierungen im Hintergrund.

Die angezeigte Fahrzeit ist eine Schätzung ohne Berücksichtigung der aktuellen Verkehrslage.
