# US 30004 – Zusätzlich die Streckenlänge sehen

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzer möchte ich bei einer neu gespeicherten Stelle zusätzlich die Strecke mit dem Auto sehen, damit ich die Entfernung auf dem Arbeitsweg einschätzen kann.

## Umfang des ersten Vertical Slice

Nach Story 30003 denselben durchgängigen Ablauf um einen zweiten Ergebniswert erweitern: Die Streckenlänge wird aus derselben Routenberechnung übernommen, bei der Stelle gespeichert und zusätzlich zur Fahrzeit angezeigt.

Das Anzeigefeld für die Strecke im Formular der neuen Stelle gehört zu Use Case 1. Diese Story füllt es beim Speichern mit dem berechneten Wert.

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
2. Die Anwendung berechnet wie in Story 30003 die Autoroute.
3. Sie übernimmt Fahrzeit und Streckenlänge aus derselben Antwort.
4. Sie speichert beide Werte bei der Stelle und zeigt Minuten sowie Kilometer an.
5. Scheitert die Berechnung, bleiben beide Werte leer und der allgemeine Hinweis erscheint.

## Akzeptanzkriterien

- [ ] Beim erstmaligen Speichern einer Stelle wird zusätzlich zur Fahrzeit die Streckenlänge aus derselben Routenberechnung übernommen.
- [ ] Die Streckenlänge wird dauerhaft bei der Stelle in der Datenbank gespeichert.
- [ ] Bei der Stelle werden die Strecke in Kilometern und die Fahrzeit in Minuten angezeigt.
- [ ] Nach erneutem Öffnen sind beide gespeicherten Werte sichtbar, ohne eine neue Berechnung auszulösen.
- [ ] Scheitert die Berechnung, bleiben beide Ergebniswerte leer und der vereinbarte allgemeine Hinweis erscheint. Das Inserat bleibt speicherbar.
- [ ] Es werden keine Eingabevalidierungen und keine Funktionen zur Bearbeitung gespeicherter Adressen ergänzt.

## Schrittweise Umsetzung

1. Die Streckenlänge aus der bestehenden Routenantwort auslesen.
2. Die Speicherung bei der Stelle um die Streckenlänge erweitern.
3. Die Anzeige um Kilometer ergänzen.
4. Speichern, erneutes Laden, Einheitenumrechnung und Fehlerfall mit simulierten Antworten testen.

## Noch nicht enthalten

- Zusätzliche API-Abfrage nur für die Streckenlänge.
- Neuberechnung beim Speichern bestehender Inserate; folgt in Story 30005.
- Eingabevalidierungen in Profil- und Inseratsformularen.
- Umsetzung einer Funktion zum Ändern, Korrigieren oder nachträglichen Ergänzen gespeicherter Adressangaben; dies gehört zu einem anderen Use-Case.
- Vergleichsfunktion, Karten, Navigation, andere Verkehrsmittel, Rückweg und Live-Verkehrsdaten.
- Berechnungen während der Eingabe und regelmässige Aktualisierung im Hintergrund.

## Technische Prüfung vor der Umsetzung

Vor der Umsetzung die verwendete Einheit der Streckenlänge in der konkreten API-Antwort prüfen und die Umrechnung für die Kilometeranzeige festlegen. Eine passende Datenbankspalte mit eindeutiger Einheit abstimmen; die bisherige Dokumentation legt diese noch nicht fest. Dazu sind noch keine API-Tests oder Schemaänderungen erfolgt.
