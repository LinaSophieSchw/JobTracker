# US 30001 – Fahrzeit beim erstmaligen Speichern einer Stelle sehen

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzer möchte ich beim erstmaligen Speichern einer Stelle die geschätzte Autofahrzeit von meiner Wohnadresse zum Arbeitsort sehen, damit ich den Zeitaufwand für den Arbeitsweg einschätzen kann.

## Umfang des ersten Vertical Slice

Nach dem fest hinterlegten Demo-Benutzer mit Wohnadresse ([US 30004](30004-demo-benutzer-fest-hinterlegen.md)) und dem Stellen-Formular mit Arbeitsadresse und Arbeitsweg aus Use Case 1 ([US 10002](../Use_Case_1/10002-weitere-felder-vorschauen.md) bis [US 10004](../Use_Case_1/10004-manuell-erfassen.md)) wird beim erstmaligen Speichern einer Stelle die Autofahrzeit abgefragt, gespeichert und angezeigt. Der Slice umfasst den gesamten Ablauf vom Klick bis zur gespeicherten Anzeige einschliesslich des einheitlichen Berechnungsfehlers.

Gemeinsame Festlegungen für diesen Slice:

- Wohnadresse und Arbeitsadresse bestehen jeweils aus drei Feldern: **Strasse mit Hausnummer, Postleitzahl und Ort** ([ADR 0009](../../decisions/0009-adresse-in-drei-feldern.md)). Die Wohnadresse ist beim Demo-Benutzer fest im System hinterlegt ([US 30004](30004-demo-benutzer-fest-hinterlegen.md)); die Arbeitsadresse wird über drei Textfelder erfasst.
- **Es gibt keine Maske zur Erfassung des Nutzers.** Alle Stellen gehören zum fest hinterlegten Demo-Benutzer.
- Die Felder für Arbeitsadresse und Arbeitsweg gehören zum Stellen-Formular von **Use Case 1**. Use Case 3 berechnet nur die Werte des Arbeitswegs.
- Es werden **keine Eingabevalidierungen** vorgenommen: keine Pflichtfeld-, Format-, Längen- oder Plausibilitätsprüfungen.
- **Die Umsetzung einer Funktion zum Bearbeiten gespeicherter Adressen gehört zu einem anderen Use-Case.** Bei jedem Speichern eines Inserats verwendet die Berechnung die für diesen Speichervorgang aktuellen Adressen, auch wenn diese über eine anderweitig umgesetzte Bearbeitungsfunktion geändert wurden.
- **Schweiz ist fest vorgegeben.** Es gibt keine Länderauswahl; die Adresssuche wird auf die Schweiz beschränkt.
- Berechnet werden Strecke und geschätzte Fahrzeit für den **einfachen Hinweg mit dem Auto**, ohne Live-Verkehrsdaten.
- Die Anwendung verwendet **OpenRouteService** zur Adresssuche und Routenberechnung ([ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md)).
- Berechnungen werden ausschliesslich durch den Klick auf **«Speichern» im Inseratsformular** ausgelöst. Eingaben und das Öffnen einer Stelle lösen keine Berechnung aus.
- Scheitert die Arbeitswegberechnung, verhindert dies nicht das Speichern des Inserats. Es erscheint ausschliesslich: **«Arbeitsweg konnte nicht berechnet werden.»**
- Im Studienprojekt wird für den Demo-Benutzer eine öffentliche Beispieladresse ohne Bezug zu realen Personen verwendet.

## Ablauf

1. Der Nutzer klickt bei einer neuen Stelle auf «Speichern».
2. Das Backend verwendet die fest hinterlegte Wohnadresse des Demo-Benutzers und die erstmalig erfasste Arbeitsadresse.
3. Es führt die Bestandteile je Adresse für die auf die Schweiz begrenzte Adresssuche zusammen und ermittelt die Koordinaten.
4. Es lässt die Autofahrzeit für den einfachen Hinweg berechnen.
5. Bei Erfolg wird die Fahrzeit bei der Stelle gespeichert und in Minuten angezeigt.
6. Scheitert die Berechnung, bleibt die Stelle speicherbar; die Fahrzeit bleibt leer und der allgemeine Hinweis erscheint.

## Akzeptanzkriterien

- [ ] Der Klick auf «Speichern» bei einem neuen Inserat löst die Berechnung aus.
- [ ] Die Anwendung verwendet die fest hinterlegte Wohnadresse des Demo-Benutzers und die erstmalig erfasste Arbeitsadresse.
- [ ] Die Adressbestandteile werden für die Adresssuche zusammengeführt. Beide Adressen werden mit auf die Schweiz begrenzter Suche in Koordinaten umgewandelt.
- [ ] Die Anwendung lässt die geschätzte Autofahrzeit für den einfachen Hinweg berechnen.
- [ ] Die Fahrzeit wird dauerhaft bei der Stelle in der Datenbank gespeichert und in Minuten angezeigt.
- [ ] Nach erneutem Öffnen wird die gespeicherte Fahrzeit angezeigt, ohne eine neue Berechnung auszulösen.
- [ ] Kann keine verwendbare Adresse oder Route ermittelt werden oder scheitert die Anfrage, bleibt das Inserat speicherbar. Die Fahrzeit bleibt leer und der vereinbarte allgemeine Hinweis erscheint.
- [ ] Technische Fehlerursachen werden nicht angezeigt.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die Adresssuche und Routenberechnung zunächst mit öffentlichen Beispieladressen prüfen.
2. Den Aufruf beim erstmaligen Speichern mit der Wohnadresse des Demo-Benutzers und der Arbeitsadresse des Inserats verbinden.
3. Die Fahrzeit bei der Stelle in der Datenbank speichern.
4. Gespeicherte Minuten beziehungsweise den allgemeinen Fehlerhinweis anzeigen.
5. Erfolgsfall, Berechnungsfehler und erneutes Öffnen mit simulierten API-Antworten testen.

## Noch nicht enthalten

- Anzeige und Speicherung der Streckenlänge; folgt in Story 30002.
- Neuberechnung beim Speichern bestehender Inserate; folgt in Story 30003.
- Automatische Korrektur von Adressen und Auswahl zwischen Adressvorschlägen.
- Eingabevalidierungen im Inseratsformular.
- Maske zur Erfassung des Nutzers oder zum Ändern der Wohnadresse.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Die Dokumentation bestätigt Freitext-Adresssuche, Länderfilter und Autorouting. Ein authentifizierter Test mit den vorgesehenen Schweizer Beispieladressen steht noch aus. Vor der Umsetzung API-Zugang, Ergebnisstruktur, Zeiteinheit sowie den Umgang mit ungeeigneten Adresstreffern prüfen. Ein bloss zurückgegebener Ort genügt nicht als konkrete Adresse. Der API-Schlüssel bleibt serverseitig; Netzwerkaufrufe erhalten ein Zeitlimit. Automatische Tests verwenden simulierte Antworten statt Live-Abfragen. Die Prüfung der API-Ergebnisse ist keine Eingabevalidierung der Formulare.
