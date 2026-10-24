# US 30002 – Zusätzlich die Streckenlänge sehen

Status: Umgesetzt (Branch `feature/30002-streckenlaenge`)

Datum: 2026-10-20, umgesetzt 2026-10-24

Spickzettel zur Umsetzung: [30002-spickzettel.md](30002-spickzettel.md)

## User Story

Als Nutzer möchte ich bei einer neu gespeicherten Stelle zusätzlich die Strecke mit dem Auto sehen, damit ich die Entfernung auf dem Arbeitsweg einschätzen kann.

## Umfang des ersten Vertical Slice

Nach Story 30001 denselben durchgängigen Ablauf um einen zweiten Ergebniswert erweitern: Die Streckenlänge wird aus derselben Routenberechnung übernommen, bei der Stelle gespeichert und zusätzlich zur Fahrzeit angezeigt.

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
2. Die Anwendung berechnet wie in Story 30001 die Autoroute.
3. Sie übernimmt Fahrzeit und Streckenlänge aus derselben Antwort.
4. Sie speichert beide Werte bei der Stelle und zeigt Minuten sowie Kilometer an.
5. Scheitert die Berechnung, bleiben beide Werte leer und der allgemeine Hinweis erscheint.

## Akzeptanzkriterien

- [x] Beim erstmaligen Speichern einer Stelle wird zusätzlich zur Fahrzeit die Streckenlänge aus derselben Routenberechnung übernommen.
- [x] Die Streckenlänge wird dauerhaft bei der Stelle in der Datenbank gespeichert.
- [x] Bei der Stelle werden die Strecke in Kilometern und die Fahrzeit in Minuten angezeigt.
- [ ] Nach erneutem Öffnen sind beide gespeicherten Werte sichtbar, ohne eine neue Berechnung auszulösen. *Teilweise:* Beide Werte stehen dauerhaft in `fahrzeit_auto_in_minuten` und `strecke_auto_in_metern`. Eine Ansicht zum Öffnen einer Stelle gibt es noch nicht; sie gehört zur Detailansicht von Use Case 2, die diese Spalten nur mitlesen muss.
- [x] Scheitert die Berechnung, bleiben beide Ergebniswerte leer und der vereinbarte allgemeine Hinweis erscheint. Das Inserat bleibt speicherbar.
- [x] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die Streckenlänge aus der bestehenden Routenantwort auslesen.
2. Die Speicherung bei der Stelle um die Streckenlänge erweitern.
3. Die Anzeige um Kilometer ergänzen.
4. Speichern, erneutes Laden, Einheitenumrechnung und Fehlerfall mit simulierten Antworten testen.

## Noch nicht enthalten

- Zusätzliche API-Abfrage nur für die Streckenlänge.
- Neuberechnung beim Speichern bestehender Inserate; folgt in Story 30003.
- Eingabevalidierungen im Inseratsformular.
- Maske zur Erfassung des Nutzers oder zum Ändern der Wohnadresse.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Vor der Umsetzung die verwendete Einheit der Streckenlänge in der konkreten API-Antwort prüfen und die Umrechnung für die Kilometeranzeige festlegen. Vorgesehen ist die Spalte `strecke_auto_in_metern` ([ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md)).

### Befund vom 24.10.2026

| Frage | Befund |
|---|---|
| Einheit | `distance` in `routes[0].summary` ist in Metern. Bestätigt schon in der Prüfung zu [US 30001](30001-fahrzeit-beim-ersten-speichern.md) am 22.10.2026 (Bern–Zug: 138267.6). |
| Zusätzliche Abfrage | Nicht nötig. `distance` steht in derselben Antwort wie `duration`. |
| Schema | Keine Änderung nötig. Die Spalte `strecke_auto_in_metern INTEGER` gibt es schon. |
| Umrechnung | Gespeichert werden ganze Meter (`round()`, 138267.6 → 138268). Das Frontend zeigt Kilometer mit einer Nachkommastelle (138268 / 1000 → «138.3 km»). |
| Echte Abfrage | Am 24.10.2026 mit `arbeitsweg_berechnen()` geprüft: Bern–Zug ergibt 95 Minuten und 138268 Meter, «Luzern» ohne Strasse ergibt beide Werte leer. |
