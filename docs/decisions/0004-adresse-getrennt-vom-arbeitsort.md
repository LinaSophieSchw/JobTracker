# Adresse getrennt vom Arbeitsort

Datum: 2026-10-19

## Status

Angenommen

## Kontext

Die Fahrzeit braucht einen genauen Zielpunkt. Anzeigen nennen oft nur einen
Ort oder mehrere Orte («Bern oder Zürich»). Mit nur dem Ort rechnet ein
Routendienst zum Ortszentrum, was bei grösseren Orten ungenau ist.

## Betrachtete Optionen

- **Option 1: Ein Feld `arbeitsort` für beides.** Einfach. Fahrzeit ungenau,
  «Bern, Zürich» gar nicht berechenbar.
- **Option 2: Zwei Felder, `arbeitsort` zur Anzeige und `adresse` für die
  Fahrzeit.** Genau. Ein Feld mehr, und die Adresse muss oft von Hand ergänzt
  werden.
- **Option 3: Koordinaten speichern.** Genau, aber ein zusätzlicher Dienst zur
  Umwandlung (Geocoding) und bei Google Fristen für das Speichern.

## Entscheidung

Option 2 angenommen: zwei Felder, `arbeitsort` zur Anzeige und `adresse` für
die Fahrzeit.

## Begründung

Genauere Fahrzeit bei kleinem Mehraufwand. Beide Dienste, die für die Fahrzeit
in Frage kommen (Google Routes API und transport.opendata.ch), nehmen Adressen
direkt an. Eine eigene Umwandlung in Koordinaten entfällt.

## Konsequenzen

- Format «Strasse Nr, PLZ Ort» mit Pflicht zur PLZ, gleich für die
  Wohnadresse im Profil (Regel A1 im [Datenmodell](../datenmodell.md)).
- Der Import füllt `adresse` nur, wenn jobs.ch eine Strasse liefert. Bei
  mehreren Arbeitsorten nimmt er die erste Adresse; der Benutzer kann sie
  ändern.
- Fehlt eine Adresse, gibt es keine Fahrzeit. Das ist ein normaler Zustand:
  Das Formular zeigt «Adresse fehlt, Fahrzeit nicht berechenbar».
- Der Dienst wandelt die Adresse selbst um. Unvollständige Adressen können am
  falschen Ort landen. Gegenmassnahmen: PLZ-Pflicht und, falls Google, der
  Parameter `regionCode` = `ch`.
