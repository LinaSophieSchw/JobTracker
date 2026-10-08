---
name: start-coding
description: Bereitet im SWEN-Projekt alles vor, bevor ein Teammitglied mit Programmieren beginnt – neusten Stand von GitHub holen, Abhängigkeiten aktualisieren und einen passenden Feature-Branch eröffnen. Der Skill wird immer verwendet, wenn jemand mit einer neuen Aufgabe anfangen will, z. B. «ich will das Login bauen», «lass uns starten», «neues Feature», «ich fange jetzt an mit …» oder «bring mich auf den neusten Stand». Für das Abschliessen (committen, pushen, Pull-Request) gibt es den Skill end-coding.
---

# Start Coding

Das Team besteht aus Git-Anfängern. Dieser Skill sorgt dafür, dass jede neue
Aufgabe auf dem neusten Stand und auf einem eigenen Branch beginnt. Das
verhindert Merge-Konflikte und hält die Beiträge pro Person in der Historie
sichtbar.

Der Agent führt die Schritte selbst aus (sie verändern nichts Gefährliches)
und erklärt jeden Befehl in einem Satz. Er antwortet auf Deutsch.

## Ablauf

1. **Offene Änderungen prüfen:** `git status`. Gibt es noch nicht committete
   Änderungen, hält der Agent an und fragt das Teammitglied, ob diese zuerst
   abgeschlossen werden sollen (Skill `end-coding`) oder vorerst mit
   `git stash` beiseitegelegt werden sollen.
2. **Identität prüfen:** `git config user.name` und `git config user.email`.
   Fehlt etwas, erklärt der Agent, wie es gesetzt wird. Die E-Mail muss zum
   GitHub-Account passen, sonst werden die Commits niemandem zugeordnet.
3. **Neusten Stand holen:**
   ```bash
   git switch master
   git pull
   ```
4. **Abhängigkeiten aktualisieren** (falls jemand neue Pakete hinzugefügt
   hat):
   ```bash
   uv sync --all-groups
   ```
5. **Branch eröffnen:** Aus der Beschreibung des Teammitglieds leitet der
   Agent einen kurzen Namen ab, z. B. «Ich will das Login bauen» →
   ```bash
   git switch -c feature/login
   ```
   Präfixe: `feature/` (Neues), `fix/` (Fehler), `docs/` (Dokumentation),
   `test/` (Tests). Kleinbuchstaben, Bindestriche, keine Umlaute. Hat das
   Teammitglied nichts beschrieben, fragt der Agent kurz, woran es arbeiten
   will.
6. **Kurz zusammenfassen:** Auf welchem Branch das Teammitglied jetzt ist und
   dass beim Fertigwerden der Skill `end-coding` hilft. Dazu der Hinweis:
   lieber mehrmals zwischendurch committen als einmal am Schluss.

Meldet `git pull` einen Konflikt, folgt der Agent
`.agents/skills/end-coding/references/merge-konflikte.md`.
