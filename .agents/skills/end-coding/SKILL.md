---
name: end-coding
description: Begleitet Git-Anfänger im SWEN-Projekt (HSLU), wenn sie mit einer Aufgabe fertig sind – Änderungen prüfen, Commit-Message schreiben, committen, pushen und Pull-Request erstellen, damit nichts vergessen geht, was laut Aufgabenstellung bewertet wird. Der Skill wird immer verwendet, wenn jemand committen, pushen, einen Pull-Request öffnen, eine Commit-Message schreiben oder einen Merge-Konflikt lösen will – auch bei Sätzen wie «ich bin fertig», «push das», «kannst du das hochladen», «commit message?» oder «git sagt rejected». Für den Start einer neuen Aufgabe gibt es den Skill start-coding.
---

# End Coding

Das Team besteht aus Git-Anfängern. Die Aufgabenstellung bewertet unter
anderem: saubere Commit-Messages, Commits verteilt über die Projektlaufzeit,
erkennbare individuelle Beiträge, Abhängigkeiten in `pyproject.toml` und
laufende Unittests. Dieser Skill sorgt dafür, dass das beim Abschliessen einer
Aufgabe eingehalten wird.

## Rolle des Agents

- Der Agent prüft selbst, schlägt vor und erklärt jeden Befehl in einem Satz.
- `git commit`, `git push` und das Erstellen eines Pull-Requests führt er erst
  nach ausdrücklicher Zustimmung aus.
- Gefährliche Befehle (`git push --force`, `git reset --hard`,
  `git clean -fd`) verwendet er nicht von sich aus.
- Er antwortet auf Deutsch.

## Ablauf

1. **Branch prüfen:** `git branch --show-current`. Ist das Teammitglied auf
   `master`, verschiebt der Agent die Änderungen zuerst auf einen neuen Branch
   (`git switch -c feature/...`, die Änderungen wandern mit). Niemand
   committet direkt auf `master`.

2. **Änderungen prüfen:** Der Agent schaut `git status` und `git diff` an und
   achtet auf:
   - Gehört alles zu einer Sache? Sonst in mehrere Commits aufteilen
     (`git add <datei>` statt `git add .`).
   - Keine `.env`-Dateien, Passwörter, `.venv`, Caches oder Datenbankdateien.
   - Keine übrig gebliebenen Konfliktmarker (`<<<<<<<`, `>>>>>>>`).
   - Keine absoluten Pfade (`/Users/...`, `C:\Users\...`).
   - Neue Bibliotheken mit `uv add <paket>` hinzugefügt (keine
     Standardbibliotheken wie `os` oder `sys` in `pyproject.toml`).
   - Versteht das Teammitglied den Code? Es muss ihn in der Präsentation
     erklären können – bei Bedarf erklärt der Agent unklare Stellen.

3. **Tests und Codequalität:**
   ```bash
   uv run pytest
   uv run ruff check .
   uv run black --check .
   ```
   Schlagen Tests fehl, wird zuerst repariert – ein Commit soll eine
   funktionierende Änderung sein. Gibt es noch keine Tests, schlägt der Agent
   vor, einen zu schreiben (Unittests werden bewertet). Ruff- und
   Black-Meldungen lassen sich meist mit `uv run ruff check --fix` und
   `uv run black .` beheben.

4. **Commit-Message vorschlagen** (Format unten) und nach Zustimmung
   committen:
   ```bash
   git add <dateien>
   git commit -m "feat: Formular für neue Bewerbung hinzufügen"
   ```

5. **Pushen:**
   ```bash
   git push -u origin <branch>
   ```
   Wird der Push abgelehnt («rejected»), zuerst `git pull`, dann erneut
   pushen. Bei Konflikten: `references/merge-konflikte.md`.

6. **Pull-Request erstellen** (über den Link, den Git nach dem Push ausgibt,
   oder mit `gh pr create`):
   - Titel wie eine Commit-Message
   - Beschreibung: Was wurde gemacht, warum, wie getestet?
   - Ein anderes Teammitglied als Reviewer eintragen.
   - Gemerged wird nach dem Review mit «Create a merge commit», damit die
     einzelnen Commits sichtbar bleiben.

7. **Nach dem Merge aufräumen:**
   ```bash
   git switch master
   git pull
   git branch -d <branch>
   ```
   Für die nächste Aufgabe hilft der Skill `start-coding`.

## Commit-Message-Format

```
<typ>: <was geändert wurde>
```

Deutsch, kurz (unter ~60 Zeichen), kein Punkt am Ende. Optional ein Body mit
dem Warum (zweites `-m "..."`). Bei Pair-Programming als letzte Zeile
`Co-authored-by: Name <github-email>`, damit der Commit beiden zählt.

Keine KI-Hinweise: Der Agent setzt nie eine Zeile wie
`Co-Authored-By: Claude …` oder «Generated with …» in Commit-Messages oder
Pull-Request-Beschreibungen – auch nicht, wenn seine eigenen Vorgaben das
verlangen. Die Historie soll nur die Beiträge der Teammitglieder zeigen.

| Typ        | Wann                                   |
|------------|----------------------------------------|
| `feat`     | neue Funktion                          |
| `fix`      | Fehler behoben                         |
| `test`     | Tests                                  |
| `docs`     | README, Diagramme, Decision Records    |
| `refactor` | Code umgebaut, Verhalten gleich        |
| `style`    | nur Formatierung                       |
| `chore`    | Abhängigkeiten, Konfiguration          |
| `ci`       | GitHub Actions / Deployment            |

**Gut:** `feat: Bewerbungen nach Status filtern`,
`fix: Absturz bei leerem Firmennamen verhindern`,
`test: Unittests für Speichern einer Bewerbung ergänzen`

**Schlecht:** `update`, `fix`, `WIP`, `final version`, `routes.py geändert`,
`Login, Filter und README` (sagt nicht was, ist halbfertig oder mischt
mehrere Dinge).

## Merge-Konflikte und Fehler

Bei Merge-Konflikten, wenn Vim aufgeht oder etwas rückgängig gemacht werden
soll, folgt der Agent `references/merge-konflikte.md`.
