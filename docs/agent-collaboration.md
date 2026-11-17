# Zusammenarbeit mit KI-Agenten

Wir haben den JobTracker mit Coding-Agenten wie Codex und Claude Code
entwickelt. Diese Datei beschreibt, wie wir sie eingesetzt haben und welche
Regeln dabei galten.

## Grundlage: AGENTS.md

[AGENTS.md](../AGENTS.md) ist die Anleitung, die jeder Agent zuerst liest.
Sie legt fest:

 * Einfache Lösungen zuerst, zum Beispiel Flask statt Django und ein Frontend
   über CDN ohne Build-Schritt.
 * Wichtige Entscheide werden als ADR in [decisions](decisions/) festgehalten,
   auf der Grundlage von [decision-template.md](decision-template.md).
 * Wo Backend, Frontend und Dokumentation liegen (siehe
   [directories.md](directories.md)).

## Skills für den Arbeitsablauf

Die Skills liegen in `.agents/skills/`. Für Claude Code sind `start-coding`,
`learn-coding`, `end-coding` und `learninglog` zusätzlich in `.claude/skills/`
eingetragen. Diese Einträge verweisen nur auf dieselben Dateien.

| Skill | Wann | Was der Agent tut |
|---|---|---|
| `start-coding` | Vor einer neuen Aufgabe | Neuesten Stand von GitHub holen, Abhängigkeiten aktualisieren, Feature-Branch anlegen |
| `learn-coding` | Beim Programmieren | Die User Story als Vertical Slice (Frontend → Backend → Datenbank) in kleinen, lauffähigen Schritten umsetzen und jeden Schritt einfach auf Deutsch erklären |
| `end-coding` | Wenn die Aufgabe fertig ist | Änderungen prüfen, deutsche Commit-Message schreiben, committen, pushen und Pull Request öffnen |
| `challenge-development-decisions` | Bei Technologie- und Architekturfragen | Annahmen hinterfragen und Alternativen zeigen, bevor gebaut wird, und den Entscheid als ADR festhalten |
| `learninglog` | Nach wichtigen Schritten und Entscheiden | Arbeitsschritte, Entscheide und die Unterstützung durch die KI im Learninglog der Person festhalten |

## Regeln

 * **Der Agent schlägt vor, das Team entscheidet.** Neue Bibliotheken und
   Technologien gibt es erst nach Rückfrage.
 * **Wir müssen den Code erklären können.** Darum baut der Agent in kleinen
   Schritten und erklärt jeden Schritt, statt ganze Dateien auf einmal zu
   schreiben.
 * **Entscheide werden dokumentiert.** Was wir mit dem Agenten entschieden
   haben, steht als ADR in [decisions](decisions/).
 * **Der Beitrag der KI bleibt sichtbar.** Jede Person führt einen eigenen
   Learninglog in [reflection](reflection/). Darin steht, was die KI
   beigetragen hat. Persönliche Reflexionen schreibt die Person selbst; der
   Agent erfindet sie nicht.
