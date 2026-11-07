# Öffentliche Domain und JobTracker-Logo

Datum: 2026-11-07

## Status

Angenommen. Lina bestätigte die Domainänderung und prüfte das Logo lokal.
Die endgültige Domain und ihre Weiterleitung sind noch separat zu prüfen;
das Online-Deployment der Logoänderung steht noch aus.

## Kontext

Die öffentliche Webapp war unter
`https://job-tracker-omega-virid.vercel.app` erreichbar. Der automatisch
vergebene Name ist schwer zu merken und enthält keinen Kursbezug.
Ausserdem fehlte ein eigenes Symbol im Browser-Tab und neben dem Seitentitel.

Die Gestaltung soll zum einfachen Studienprojekt und zur blauen
Bootstrap-Hauptfarbe passen, ohne zusätzliche Bibliotheken einzuführen.

## Betrachtete Optionen

- **Bisherige Adresse und kein eigenes Logo:** Kein zusätzlicher Aufwand,
  aber weniger Wiedererkennung und ein schwer teilbarer Name.
- **Verständliche vercel.app-Adresse und ein gemeinsames PNG-Symbol:**
  Kleine Änderung an Hosting-Einstellungen und HTML. Ein Bild wird an
  beiden Anzeigeorten wiederverwendet.
- **Eigene registrierte Domain und umfangreicher Markenauftritt:** Mehr
  Gestaltungsfreiheit, aber zusätzlicher Beschaffungs- und Pflegeaufwand,
  der für das Studienprojekt nicht erforderlich ist.

## Entscheidung

Lina entscheidet sich für eine verständliche Adresse unter `vercel.app`
mit Projekt- und Kursbezug. Im zuletzt gezeigten Bestätigungsdialog war
`https://jobtracker-swen.vercel.app` eingetragen. Die Variante
`jobtracker-swen26.vercel.app` wurde ebenfalls diskutiert; ein anschliessender
Wechsel auf diesen Namen ist nicht belegt. Vor dem Aktualisieren zentraler
Projektlinks ist der tatsächlich gespeicherte Name in Vercel zu bestätigen.

Die bisherige Domain soll auf die neue weiterleiten. Dafür war im
Vercel-Dialog «Redirect old domain to new» ausgewählt.

Als Logo wird ein mit KI-Bildgenerierung erstelltes blaues Aktenkoffer-Symbol
mit weissem Häkchen verwendet. Die Datei liegt unter `public/favicon.png`.
Sie wird im HTML-Kopf als Favicon und zusätzlich als 40 × 40 Pixel grosses
Bild neben «JobTracker» eingebunden. Bootstrap-Klassen richten Bild und
Überschrift aus. Das dekorative Bild neben dem bereits vorhandenen Namen
erhält einen leeren Alternativtext.

## Begründung

Eine kurze Adresse ist für Team, Präsentation und Weitergabe verständlicher.
Die Weiterleitung soll bestehende Links erhalten. Die vorhandene
vercel.app-Domain genügt; eine separat registrierte Domain ist nicht nötig.

Das einfache Symbol verbindet Stellensuche und erledigte Aufgaben. Blau
passt zur bestehenden Oberfläche. Die Wiederverwendung derselben Datei als
Favicon und Seitenlogo hält die Einbindung und Pflege überschaubar.

## Konsequenzen

- Die Domain wird in Vercel verwaltet, nicht im HTML. Backend, Datenbank
  und fachliche Abläufe werden durch die Umbenennung nicht geändert.
- Die tatsächlich aktive neue Adresse und die Weiterleitung werden im
  Browser geprüft. Danach werden Verweise in README und Präsentation
  auf den bestätigten Namen aktualisiert.
- Das PNG wird gemeinsam mit dem HTML versioniert und veröffentlicht.
  Ein Browser kann das bisherige Favicon zwischenspeichern; die Anzeige
  ist nach dem Deployment gegebenenfalls in einem neuen Tab zu prüfen.
- Die lokale Anzeige neben der Überschrift ist per Screenshot bestätigt.
  Ein erfolgreicher Online-Test des neuen Logos wird erst nach dem
  Deployment dokumentiert.
- Das Logo ist eine einfache PNG-Datei, kein eigenständiges Designsystem.
  Eine zusätzliche Bild- oder Icon-Bibliothek ist nicht erforderlich.

## Referenzen

- [ADR 0013: Bootstrap für die Darstellung](0013-bootstrap-fuer-die-darstellung.md)
- [Frontend](../../public/index.html)
- [Logo und Favicon](../../public/favicon.png)
- [Linas Lernlog](../reflection/Lina/learninglog_lina.md)
