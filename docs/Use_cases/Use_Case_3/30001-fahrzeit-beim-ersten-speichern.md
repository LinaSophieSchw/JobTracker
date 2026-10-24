# US 30001 – Fahrzeit beim erstmaligen Speichern einer Stelle sehen

Status: Umgesetzt (Branch `feature/30001-fahrzeit`)

Datum: 2026-10-20, umgesetzt 2026-10-24

Spickzettel zur Umsetzung: [30001-spickzettel.md](30001-spickzettel.md)

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
3. Es übergibt die drei Bestandteile je Adresse getrennt an die auf die Schweiz begrenzte Adresssuche und ermittelt die Koordinaten ([ADR 0011](../../decisions/0011-strukturierte-adresssuche.md)).
4. Es lässt die Autofahrzeit für den einfachen Hinweg berechnen.
5. Bei Erfolg wird die Fahrzeit bei der Stelle gespeichert und in Minuten angezeigt.
6. Scheitert die Berechnung, bleibt die Stelle speicherbar; die Fahrzeit bleibt leer und der allgemeine Hinweis erscheint.

## Akzeptanzkriterien

- [x] Der Klick auf «Speichern» bei einem neuen Inserat löst die Berechnung aus.
- [x] Die Anwendung verwendet die fest hinterlegte Wohnadresse des Demo-Benutzers und die erstmalig erfasste Arbeitsadresse.
- [x] Die Adressbestandteile werden getrennt an die strukturierte Adresssuche übergeben ([ADR 0011](../../decisions/0011-strukturierte-adresssuche.md)). Beide Adressen werden mit auf die Schweiz begrenzter Suche in Koordinaten umgewandelt.
- [x] Die Anwendung lässt die geschätzte Autofahrzeit für den einfachen Hinweg berechnen.
- [x] Die Fahrzeit wird dauerhaft bei der Stelle in der Datenbank gespeichert und in Minuten angezeigt.
- [ ] Nach erneutem Öffnen wird die gespeicherte Fahrzeit angezeigt, ohne eine neue Berechnung auszulösen. *Teilweise:* Die Fahrzeit steht dauerhaft in `fahrzeit_auto_in_minuten`. Eine Ansicht zum Öffnen einer Stelle gibt es noch nicht; sie gehört zur Detailansicht von Use Case 2, die diese Spalte nur mitlesen muss.
- [x] Kann keine verwendbare Adresse oder Route ermittelt werden oder scheitert die Anfrage, bleibt das Inserat speicherbar. Die Fahrzeit bleibt leer und der vereinbarte allgemeine Hinweis erscheint.
- [x] Technische Fehlerursachen werden nicht angezeigt.
- [x] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

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

Die Dokumentation bestätigt Freitext-Adresssuche, Länderfilter und Autorouting. Vor der Umsetzung API-Zugang, Ergebnisstruktur, Zeiteinheit sowie den Umgang mit ungeeigneten Adresstreffern prüfen. Ein bloss zurückgegebener Ort genügt nicht als konkrete Adresse. Der API-Schlüssel bleibt serverseitig; Netzwerkaufrufe erhalten ein Zeitlimit. Automatische Tests verwenden simulierte Antworten statt Live-Abfragen. Die Prüfung der API-Ergebnisse ist keine Eingabevalidierung der Formulare.

### Befund vom 22.10.2026

Geprüft mit öffentlichen Beispieladressen (Bundesplatz 3 Bern, Bahnhofstrasse 12 Zug, Suurstoffi 1 Rotkreuz):

| Frage | Befund |
|---|---|
| API-Zugang | Funktioniert. Der Schlüssel geht im Header `Authorization` mit, nicht in der URL. Ein falscher Schlüssel ergibt Statuscode 403. |
| Ergebnisstruktur Adresssuche | GeoJSON: `features[0].geometry.coordinates` = `[Längengrad, Breitengrad]`, `features[0].properties.layer` = Art des Treffers. |
| Ergebnisstruktur Route | `routes[0].summary` mit `duration` und `distance`, z. B. Bern–Zug `{'distance': 138267.6, 'duration': 5682.0}`. |
| Zeiteinheit | `duration` in Sekunden (5682 s ≈ 95 Min.), `distance` in Metern. |
| Ungeeignete Treffer | «Luzern» allein ergibt `layer` `locality`. Nur `address` ist eine konkrete Adresse. Die Freitext-Suche fand für die erfundene Adresse «Gibtsnichtweg 999, 9999 Nirgendwo» eine Adresse in Chur; deshalb strukturierte Suche ([ADR 0011](../../decisions/0011-strukturierte-adresssuche.md)). |
| Punkt ohne Strasse | Route antwortet mit Statuscode 404 (Code 2010). |
| Gleiche Start- und Zieladresse | `duration` 0.0, also 0 Minuten, kein Fehler. |
