# US 30002 – Arbeitsadresse erstmalig bei einer Stelle hinterlegen

Status: Abhängig von Use Case 1 – nur umsetzen, falls dort nicht vorhanden

Datum: 2026-10-20

> **Hinweis:** Die Felder für die Arbeitsadresse gehören zum Formular der neuen Stelle in Use Case 1. Wer dieses Formular umsetzt, nimmt sie mit auf. Diese Story beschreibt die Felder nur als Rückfallebene für den Fall, dass sie in Use Case 1 nicht umgesetzt werden.

## User Story

Als Nutzer möchte ich bei der Erfassung einer Stelle ihre Arbeitsadresse einmalig in getrennten Feldern erfassen und speichern können, damit sie als Ziel für die Arbeitswegberechnung zur Verfügung steht.

## Umfang des ersten Vertical Slice

Die bestehende Stellenerfassung um vier Adressfelder erweitern. Der Ablauf führt von der erstmaligen Eingabe über das Backend und die Datenbank bis zur Anzeige der gespeicherten Arbeitsadresse. Die grundlegende Stellenerfassung wird als vorhanden vorausgesetzt.

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

1. Der Nutzer erfasst eine neue Stelle.
2. Er gibt Strasse, Hausnummer, Postleitzahl und Ort in getrennten Textfeldern ein.
3. Er klickt im Inseratsformular auf «Speichern».
4. Das Backend speichert die Angaben ohne Eingabevalidierung bei der Stelle.
5. Beim erneuten Öffnen wird die Arbeitsadresse angezeigt; eine Bearbeitungsfunktion ist nicht enthalten.

## Akzeptanzkriterien

- [ ] Bei der erstmaligen Erfassung enthält das Inseratsformular die Textfelder Strasse, Hausnummer, Postleitzahl und Ort.
- [ ] Die konkrete Arbeitsadresse ist von der allgemeinen Ortsangabe der Stelle getrennt.
- [ ] Die Angaben werden ohne Eingabevalidierung übernommen. Auch leere Felder verhindern das Speichern nicht.
- [ ] Erst der Klick auf «Speichern» speichert die Angaben dauerhaft bei der zugehörigen Stelle in der Datenbank.
- [ ] Beim erneuten Öffnen wird die gespeicherte Arbeitsadresse angezeigt. Eine Bearbeitungsfunktion für diese Angaben ist nicht enthalten.
- [ ] Diese Story ergänzt keine Bearbeitungsfunktion für gespeicherte Arbeitsadressen. Wird eine solche Funktion in einem anderen Use-Case umgesetzt, können die Berechnungsstories dessen aktuelle Adressangaben verwenden.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die vorhandene Stellenerfassung und ihre Speicherung prüfen.
2. Vier Textfelder ergänzen und mit dem Speichervorgang verbinden.
3. Die Bestandteile bei der richtigen Stelle in der Datenbank speichern und wieder laden.
4. Die gespeicherte Adresse bei der Stelle anzeigen.
5. Den vollständigen Ablauf und das Speichern leerer Angaben prüfen.

## Noch nicht enthalten

- Spätere Bearbeitung oder Ergänzung der gespeicherten Arbeitsadresse.
- Automatischer Adressimport aus dem Stellenlink.
- Routenberechnung.
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Vor der Umsetzung prüfen, welche Formularfelder und Speicherfunktionen bereits vorhanden sind und wer sie betreut. Das bisher gelesene Datenmodell unterscheidet die allgemeine Ortsangabe von einem zusammenhängenden Adressfeld. Die Speicherung der vier Adressbestandteile muss mit dem Team abgestimmt und eine nötige Modelländerung dokumentiert werden. Die Vorprüfung und Implementierung sind noch nicht erfolgt.
