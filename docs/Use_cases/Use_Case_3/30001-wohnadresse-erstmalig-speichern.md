# US 30001 – Wohnadresse erstmalig im Profil hinterlegen

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzer möchte ich meine Wohnadresse einmalig in getrennten Feldern erfassen und speichern können, damit sie als Ausgangspunkt für die Arbeitswegberechnung zur Verfügung steht.

## Umfang des ersten Vertical Slice

Die bestehende Profilerfassung um vier Adressfelder erweitern. Der Ablauf führt vom erstmaligen Eingeben über das Backend und die Datenbank bis zur erneuten Anzeige der gespeicherten Wohnadresse. Die grundlegende Profilerfassung wird als vorhanden vorausgesetzt.

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

1. Der Nutzer öffnet die erstmalige Adresserfassung im Profil.
2. Er gibt Strasse, Hausnummer, Postleitzahl und Ort in getrennten Textfeldern ein.
3. Er klickt im Profil auf «Speichern».
4. Das Backend speichert die Angaben ohne Eingabevalidierung beim Profil.
5. Beim erneuten Öffnen wird die Adresse angezeigt; eine Bearbeitungsfunktion ist nicht enthalten.

## Akzeptanzkriterien

- [ ] Bei der erstmaligen Erfassung enthält das Profil die Textfelder Strasse, Hausnummer, Postleitzahl und Ort.
- [ ] Die Angaben werden ohne Eingabevalidierung übernommen.
- [ ] Beim Klick auf «Speichern» im Profil werden die Angaben dauerhaft dem Profil in der Datenbank zugeordnet.
- [ ] Beim erneuten Öffnen wird die gespeicherte Adresse angezeigt. Eine Bearbeitungsfunktion für diese Angaben ist nicht enthalten.
- [ ] Die gespeicherten Angaben stehen der späteren Arbeitswegberechnung zur Verfügung.
- [ ] Das Speichern des Profils löst keine Arbeitswegberechnung aus.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die vorhandene Profilerfassung und ihre Speicherung prüfen.
2. Vier Textfelder mit dem bestehenden Speichervorgang verbinden.
3. Die vier Bestandteile über das Backend in der Datenbank speichern und wieder laden.
4. Die gespeicherte Adresse im Profil anzeigen.
5. Den vollständigen Ablauf sowie leere Angaben ohne Validierung prüfen.

## Noch nicht enthalten

- Gesamte Profilverwaltung und Anmeldung.
- Spätere Bearbeitung oder Ergänzung der gespeicherten Wohnadresse.
- Arbeitswegberechnung und Folgen einer Wohnadressänderung.
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Vor der Umsetzung prüfen, ob Profilerfassung, Speichern und erneutes Laden bereits vorhanden sind und wer sie im Team betreut. Das bisher gelesene Datenmodell sieht ein zusammenhängendes Wohnadressfeld vor. Die Speicherung muss so abgestimmt werden, dass die vier Bestandteile erhalten bleiben; eine Änderung am Datenmodell wird mit dem Team dokumentiert. Die Vorprüfung und Implementierung sind noch nicht erfolgt.
