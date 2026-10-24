# Bugs

Stand: 2026-10-24

**Status:** Offen

## Ziel

Dieser Bereich sammelt Arbeiten, die keine neue Funktion für den Nutzer bringen,
aber die Entwicklung und den Betrieb des JobTrackers betreffen. Er steht auf
derselben Ebene wie die Use Cases.

Hierher gehören zum Beispiel:

- Probleme der Entwicklungsumgebung, z. B. Startbefehle, Abhängigkeiten,
  Unterschiede zwischen macOS und Windows.
- Fehler (Bugs), die mehrere Use Cases betreffen oder keinem Use Case
  eindeutig zugeordnet werden können.
- Deployment, Konfiguration und Umgebungsvariablen.
- Tests und Werkzeuge, die das ganze Projekt betreffen.

## User Stories

| Reihenfolge | User Story | Art | Stand |
|---|---|---|---|
| 1 | [US 90001 – Lokalen Server auf allen Rechnern gleich und stabil starten](90001-lokalen-server-stabil-starten.md) | Infrastruktur / Bug | Umgesetzt, Test auf Windows offen |

## Nummerierung

Die Stories in diesem Bereich beginnen mit **9**, z. B. 90001, 90002. So bleiben die
Nummern 4 bis 8 für weitere Use Cases frei.

## Abgrenzung

| Was | Wo |
|---|---|
| Neue Funktion für den Nutzer | im passenden Use Case |
| Fehler in einer Funktion, die nur einen Use Case betrifft | im passenden Use Case |
| Fehler, der mehrere Use Cases betrifft oder dessen Ursache ausserhalb der App-Funktionen liegt | Bugs |
| Entwicklungsumgebung, Startbefehle, Abhängigkeiten | Bugs |
| Deployment und Konfiguration | Bugs |

Entscheidungen, die das ganze Projekt betreffen, werden zusätzlich als ADR in
[`docs/decisions`](../../decisions) festgehalten.
