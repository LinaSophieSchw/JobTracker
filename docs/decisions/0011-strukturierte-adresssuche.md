# Strukturierte Adresssuche statt Freitext

Datum: 2026-10-24

## Status

Angenommen. Präzisiert die Adresssuche aus
[ADR 0008](0008-arbeitsweg-mit-openrouteservice.md).

## Kontext

ADR 0008 und [US 30001](../Use_cases/Use_Case_3/30001-fahrzeit-beim-ersten-speichern.md)
sahen vor, die drei Adressfelder aus
[ADR 0009](0009-adresse-in-drei-feldern.md) zu einem Text zusammenzuführen und
mit der Freitext-Suche von OpenRouteService in Koordinaten umzuwandeln. Die
Story verlangt ausserdem: Ein bloss zurückgegebener Ort genügt nicht als
konkrete Adresse.

Die technische Prüfung vom 22.10.2026 mit öffentlichen Beispieladressen
zeigte:

| Eingabe | Freitext-Suche | Strukturierte Suche |
|---|---|---|
| Bundesplatz 3, 3005 Bern | Adresse gefunden | Adresse gefunden |
| Gibtsnichtweg 999, 9999 Nirgendwo | «Böschenstrasse 999, Chur», als Adresse | nur «Schweiz» |
| Luzern (ohne Strasse) | nur Ort | nur Ort |
| Bundesplatz 3000, 3005 Bern | nur Strasse | nur Strasse |

Jeder Treffer enthält im Feld `layer`, was gefunden wurde: `address` (Adresse
mit Hausnummer), `street`, `postalcode`, `locality` oder `country`.

## Betrachtete Optionen

- **Option 1: Freitext-Suche** wie in ADR 0008. Die erfundene Adresse wurde
  mit `layer` `address` in Chur gefunden. Eine Prüfung auf `address` reicht
  dann nicht; es entstünde eine falsche Fahrzeit.
- **Option 2: Strukturierte Suche.** Strasse, Postleitzahl und Ort gehen
  getrennt an den Dienst (`address`, `postalcode`, `locality`), dazu
  `country=CH`. Alle geprüften Fälle wurden richtig eingeordnet.

## Entscheidung

Option 2, entschieden von Fabio für Use Case 3. Nur ein Treffer mit `layer`
`address` wird für die Berechnung verwendet; alles andere gilt als
gescheiterte Berechnung.

## Begründung

Die strukturierte Suche passt zu den drei Adressfeldern aus ADR 0009: Die
Felder müssen nicht zusammengeführt werden, und der Dienst muss nicht raten,
welcher Teil die Postleitzahl ist. Zusammen mit der Prüfung auf `address` ist
sie die einfachste Lösung, die in der technischen Prüfung keine falsche
Adresse geliefert hat.

## Konsequenzen

- Umgesetzt in `koordinaten_suchen()` in `src/app/arbeitsweg.py`.
- Adressen ohne Hausnummer, z. B. «Rega-Center», ergeben keine Fahrzeit. Das
  entspricht der Story: Es erscheint «Arbeitsweg konnte nicht berechnet
  werden.».
- Die Prüfung des Treffers ist keine Eingabevalidierung des Formulars; geprüft
  wird die Antwort des Dienstes.
- Die Story US 30001 und ADR 0008 verweisen auf diesen Entscheid.
