# US 30003 – Fahrzeit beim erstmaligen Speichern einer Stelle sehen

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzer möchte ich beim erstmaligen Speichern einer Stelle die geschätzte Autofahrzeit von meiner Wohnadresse zum Arbeitsort sehen, damit ich den Zeitaufwand für den Arbeitsweg einschätzen kann.

## Umfang des ersten Vertical Slice

Nach Umsetzung der Stories 30001 und 30002 und der grundlegenden Stellenerfassung wird beim erstmaligen Speichern einer Stelle die Autofahrzeit abgefragt, gespeichert und angezeigt. Der Slice umfasst den gesamten Ablauf vom Klick bis zur gespeicherten Anzeige einschliesslich des einheitlichen Berechnungsfehlers.

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

1. Der Nutzer klickt bei einer neuen Stelle auf «Speichern».
2. Das Backend verwendet die gespeicherte Wohnadresse und die erstmalig erfasste Arbeitsadresse.
3. Es führt die Bestandteile je Adresse für die auf die Schweiz begrenzte Adresssuche zusammen und ermittelt die Koordinaten.
4. Es lässt die Autofahrzeit für den einfachen Hinweg berechnen.
5. Bei Erfolg wird die Fahrzeit bei der Stelle gespeichert und in Minuten angezeigt.
6. Scheitert die Berechnung, bleibt die Stelle speicherbar; die Fahrzeit bleibt leer und der allgemeine Hinweis erscheint.

## Akzeptanzkriterien

- [ ] Der Klick auf «Speichern» bei einem neuen Inserat löst die Berechnung aus.
- [ ] Die Anwendung verwendet die gespeicherte Wohnadresse aus dem Profil und die erstmalig erfasste Arbeitsadresse.
- [ ] Die Adressbestandteile werden für die Adresssuche zusammengeführt. Beide Adressen werden mit auf die Schweiz begrenzter Suche in Koordinaten umgewandelt.
- [ ] Die Anwendung lässt die geschätzte Autofahrzeit für den einfachen Hinweg berechnen.
- [ ] Die Fahrzeit wird dauerhaft bei der Stelle in der Datenbank gespeichert und in Minuten angezeigt.
- [ ] Nach erneutem Öffnen wird die gespeicherte Fahrzeit angezeigt, ohne eine neue Berechnung auszulösen.
- [ ] Kann keine verwendbare Adresse oder Route ermittelt werden oder scheitert die Anfrage, bleibt das Inserat speicherbar. Die Fahrzeit bleibt leer und der vereinbarte allgemeine Hinweis erscheint.
- [ ] Technische Fehlerursachen werden nicht angezeigt.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die Adresssuche und Routenberechnung zunächst mit öffentlichen Beispieladressen prüfen.
2. Den Aufruf beim erstmaligen Speichern mit den Adressen aus Profil und Inserat verbinden.
3. Die Fahrzeit bei der Stelle in der Datenbank speichern.
4. Gespeicherte Minuten beziehungsweise den allgemeinen Fehlerhinweis anzeigen.
5. Erfolgsfall, Berechnungsfehler und erneutes Öffnen mit simulierten API-Antworten testen.

## Noch nicht enthalten

- Anzeige und Speicherung der Streckenlänge; folgt in Story 30004.
- Neuberechnung beim Speichern bestehender Inserate; folgt in Story 30005.
- Automatische Korrektur von Adressen und Auswahl zwischen Adressvorschlägen.
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Die Dokumentation bestätigt Freitext-Adresssuche, Länderfilter und Autorouting. Ein authentifizierter Test mit den vorgesehenen Schweizer Beispieladressen steht noch aus. Vor der Umsetzung API-Zugang, Ergebnisstruktur, Zeiteinheit sowie den Umgang mit ungeeigneten Adresstreffern prüfen. Ein bloss zurückgegebener Ort genügt nicht als konkrete Adresse. Der API-Schlüssel bleibt serverseitig; Netzwerkaufrufe erhalten ein Zeitlimit. Automatische Tests verwenden simulierte Antworten statt Live-Abfragen. Die Prüfung der API-Ergebnisse ist keine Eingabevalidierung der Formulare.
