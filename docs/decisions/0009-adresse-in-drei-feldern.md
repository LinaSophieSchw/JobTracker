# Adressen in drei Feldern ohne Prüfung

Datum: 2026-10-21

## Status

Vorgeschlagen. Ändert das Adressformat aus
[ADR 0004](0004-adresse-getrennt-vom-arbeitsort.md) und ersetzt Regel A1 im
[Datenmodell](../datenmodell.md). Die Trennung von Arbeitsort und Adresse aus
ADR 0004 bleibt bestehen.

## Kontext

ADR 0004 und Regel A1 legen eine Adresse als ein Textfeld im Format
«Strasse Nr, PLZ Ort» fest, mit Pflicht zur vierstelligen PLZ und einem
Prüfmuster. Die Stories zu Use Case 3 sahen zuerst vier getrennte Felder vor
(Strasse, Hausnummer, Postleitzahl, Ort).

Eine Prüfung von zwei jobs.ch-Anzeigen am 21.10.2026 zeigte: jobs.ch liefert
Strasse und Hausnummer zusammen in einem Feld (`street`, z.B.
«Bahnhofstrasse 12»), dazu `postalCode` und `city`. Manche Ortsangaben haben
gar keine Hausnummer (z.B. «Rega-Center»).

## Betrachtete Optionen

- **Option 1: Ein Feld mit Prüfung** (heutiger Stand). Das Backend muss das
  Format prüfen und eine Fehlermeldung liefern.
- **Option 2: Vier Felder ohne Prüfung.** Der Import müsste `street` in
  Strasse und Hausnummer aufteilen und braucht eine Regel für Angaben ohne
  Hausnummer.
- **Option 3: Drei Felder ohne Prüfung.** Strasse mit Hausnummer,
  Postleitzahl und Ort, gleich aufgebaut wie bei jobs.ch.

## Entscheidung

Option 3, vorgeschlagen von Fabio: drei Felder ohne Pflicht-, Format-, Längen-
oder Plausibilitätsprüfung. Die Schweiz ist fest vorgegeben, es gibt keine
Länderauswahl. Gilt für die Wohnadresse und die Arbeitsadresse.

## Begründung

Die App übernimmt den Aufbau von jobs.ch, dadurch muss beim Import nichts
zerlegt werden. Ohne Prüfung braucht es keine zusätzlichen Fehlermeldungen
([ADR 0010](0010-minimale-oberflaeche.md)). Ob eine Adresse brauchbar ist,
zeigt sich bei der Berechnung des Arbeitswegs
([ADR 0008](0008-arbeitsweg-mit-openrouteservice.md)).

## Konsequenzen

- Spalten `wohnadresse_strasse`, `wohnadresse_postleitzahl`,
  `wohnadresse_ort` in `benutzer` und `inseratadresse_strasse`,
  `inseratadresse_postleitzahl`, `inseratadresse_ort` in `stellenanzeigen`
  statt `wohnadresse` und `adresse`. Das Feld Strasse enthält die Hausnummer.
  Der Präfix `inseratadresse_` grenzt die Adresse aus dem Inserat klar von
  `wohnadresse_` und von `arbeitsort` ab.
- Der Import schreibt `street` unverändert in `inseratadresse_strasse`,
  `postalCode` in `inseratadresse_postleitzahl` und `city` in
  `inseratadresse_ort`.
- Unvollständige oder falsche Adressen werden gespeichert. Die Berechnung des
  Arbeitswegs scheitert dann und zeigt die Meldung aus ADR 0008. Die Meldung
  «Adresse fehlt, Fahrzeit nicht berechenbar» aus ADR 0004 entfällt.
- Die Stories US 10002 und US 10003 verwenden noch das alte Format. Sie passt
  die Person an, die Use Case 1 bearbeitet.
- Die Person, die das Datenmodell betreut, bestätigt den Vorschlag.
