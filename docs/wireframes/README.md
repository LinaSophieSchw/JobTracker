# Wireframes JobTracker

Stand: 2026-10-20

Die Wireframes zeigen, welche Screens es gibt, welche Felder wo stehen und wie
die Use Cases zusammenhängen. Sie sind kein Design. Grundlage für
[ADR 0010 – Minimale Oberfläche](../decisions/0010-minimale-oberflaeche.md).

| Datei | Inhalt |
|---|---|
| [wireframes.html](wireframes.html) | Die drei Screens mit Zuordnung zu den Use Cases, die nötigen Backend-Aufrufe und die Meldungen |
| [prototyp.html](prototyp.html) | Klickbarer Wegwerf-Prototyp mit Protokoll «Was im Backend passieren würde» |

Zum Ansehen die Datei im Browser öffnen (Doppelklick im Finder bzw. Explorer).
GitHub zeigt HTML-Dateien nur als Quelltext an.

## Screens

1. **Übersicht** (Startseite): Liste der Stellen, Buttons «Profil» und
   «+ Neue Stelle». Der Button ist gesperrt, bis das Profil einmal gespeichert
   wurde.
2. **Stellen-Formular** für neue und bestehende Stellen
   ([ADR 0005](../decisions/0005-ein-formular-fuer-erfassen-und-bearbeiten.md)):
   Linkfeld mit «Informationen laden» oben, Felder der Stelle, Arbeitsadresse
   und nur lesbarer Arbeitsweg.
3. **Profil:** Name und Wohnadresse.

## Was der Prototyp nicht ist

Der Prototyp ist reines HTML und JavaScript ohne Backend. Er speichert nichts
dauerhaft, jobs.ch und OpenRouteService sind simuliert, die Kilometer sind
erfunden. Er gehört nicht zur Applikation und wird nicht deployt.
