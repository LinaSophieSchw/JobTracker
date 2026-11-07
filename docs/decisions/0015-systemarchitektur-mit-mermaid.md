# 0015 – Systemarchitektur mit Mermaid dokumentieren

Date: 2026-11-07

## Status

Accepted

## Context

Die Systemarchitektur soll im README verständlich dargestellt und gemeinsam
mit dem Code gepflegt werden. Die Übersicht zeigt das Frontend mit Vue und
Bootstrap, Flask auf Vercel, PostgreSQL bei Neon sowie jobs.ch und
OpenRouteService. Fabio soll die Darstellung vor dem Merge prüfen.

## Options Considered

* Eine separat erstellte Bilddatei einbinden: einfach anzuzeigen, Änderungen
  müssen aber zusätzlich in einer Grafikdatei gepflegt werden.
* Mermaid als Text im README einbinden: Darstellung und Änderungen bleiben
  direkt im Repository nachvollziehbar.
* Eine ausführliche Darstellung nach C4 erstellen: klarere formale Gliederung,
  für die gewünschte kompakte Übersicht jedoch umfangreicher.

## Decision

Lina verwendet ein Mermaid-Flussdiagramm im README. Das Frontend steht oben,
Vercel bildet die Hosting-Grenze für Backend und statische Dateien. Die
Verbindungen tragen Beschriftungen zu Schnittstellen und Datenformaten.
Die erste Zeile der Komponenten wird hervorgehoben; im Datenbankkasten
werden die Tabellen benutzer und stellenanzeigen genannt.

## Reasons

Die Darstellung lässt sich als Text bearbeiten und mit Git versionieren.
GitHub kann den Mermaid-Code im README als Diagramm darstellen. Es entsteht
kein zusätzlicher Build-Schritt für die Anwendung. Die kompakte Übersicht
passt zum Lernprojekt und kann bei Änderungen angepasst werden.

## Consequences

Das Diagramm muss bei Architekturänderungen mitgepflegt werden. Die genaue
Anordnung und Formatierung hängen vom Mermaid-Renderer ab. Das Diagramm ist
eine Systemübersicht und kein vollständiges C4- oder Datenbankmodell.
Die Darstellung auf GitHub und die fachliche Prüfung durch Fabio stehen
vor dem Merge noch aus. Die Laufzeitarchitektur der Webapp wird nicht verändert.
