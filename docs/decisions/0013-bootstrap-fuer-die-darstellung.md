# Bootstrap für die Darstellung der Oberfläche

Datum: 2026-11-07

## Status

Angenommen. Von Lina für die weitere Gestaltung entschieden;
die Einbindung ist noch nicht umgesetzt.

## Kontext

JobTracker verwendet HTML und Vue 3 über CDN. Stellenübersicht und
Stellenformular funktionieren, ihre Darstellung verwendet bislang vorwiegend
die Standardgestaltung des Browsers. Die Oberfläche soll übersichtlicher,
einheitlicher und etwas moderner werden. Der einfache Aufbau ohne
Frontend-Build-Schritt soll erhalten bleiben.

Das Studienprojekt legt Wert auf nachvollziehbaren Code und einen
überschaubaren Aufwand. Für die vorhandenen Formulare und Tabellen ist
keine individuelle Gestaltung erforderlich.

## Betrachtete Optionen

- **Eigenes CSS:** Frei gestaltbar und ohne zusätzliche Bibliothek, aber
  Abstände, Formularstile und responsive Anordnung müssen selbst umgesetzt
  und gepflegt werden.
- **Bootstrap über CDN:** Vorgefertigte Klassen für Layout, Formulare,
  Buttons und Tabellen. Schnelle, einheitliche Gestaltung; dafür wird eine
  zusätzliche CSS-Bibliothek geladen und das Aussehen orientiert sich an
  deren Vorgaben.
- **Bootstrap mit zusätzlichem eigenem CSS:** Mehr Gestaltungsfreiheit,
  aber zusätzliche Regeln und mögliche Überschreibungen. Für den aktuellen
  Umfang nicht erforderlich.

## Entscheidung

Lina entscheidet sich für Bootstrap als CSS-Bibliothek über CDN.
Die vorhandenen Bootstrap-Klassen reichen zunächst aus; eine zusätzliche
eigene CSS-Datei ist nicht vorgesehen.

Vue bleibt für Datenbindung, Anzeigezustände und Benutzerinteraktionen
zuständig. Bootstrap-JavaScript wird für die geplante Gestaltung nicht
eingebunden. Backend, Datenbank und fachliche Abläufe bleiben unverändert.

## Begründung

Bootstrap passt zur einfachen Oberfläche des Projekts. Die vorhandenen
Bausteine ermöglichen mit wenig Aufwand gut lesbare Formulare, konsistente
Buttons, klare Abstände und eine übersichtliche Stellenliste. Das Team kann
sich auf die Funktionen konzentrieren und muss kein eigenes Designsystem
entwickeln. Die Einbindung per CDN benötigt keine Build-Werkzeuge und
entspricht dem bisherigen Vorgehen mit Vue.

## Konsequenzen

- Die Gestaltung wird schrittweise über Klassen im bestehenden HTML ergänzt.
- Die bisherigen Funktionen und Vue-Bindungen müssen weiterhin funktionieren.
  Insbesondere werden weder zusätzliche Pflichtfelder noch neue fachliche
  Validierungsregeln durch Styling eingeführt.
- Die Darstellung auf schmalen und breiten Bildschirmen sowie die Bedienung
  von Formular und Übersicht werden nach der Umstellung geprüft.
- Die Anwendung hängt für die Darstellung zusätzlich von der Verfügbarkeit
  des Bootstrap-CDN ab. Bei der Umsetzung wird eine konkrete Version fixiert
  und der vom Anbieter veröffentlichte Integritätswert übernommen.
- Ein individuelles Erscheinungsbild wird zugunsten einer einfachen,
  einheitlichen Darstellung zurückgestellt.

## Referenzen

- [Bootstrap: Einstieg und CDN-Einbindung](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap: Formulare](https://getbootstrap.com/docs/5.3/forms/overview/)
- [ADR 0010: Minimale Oberfläche](0010-minimale-oberflaeche.md)
