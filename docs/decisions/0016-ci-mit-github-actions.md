# Automatische Prüfung mit GitHub Actions (CI)

Datum: 2026-11-14

## Status

Vorgeschlagen von Mirko. Angenommen, sobald der Pull Request mit
`.github/workflows/ci.yml` nach dem Review gemergt ist.

## Kontext

Vor jedem Commit sollen die Unittests grün sein und der Code den Stilregeln
entsprechen (Skill `end-coding`: `uv run pytest`, `uv run ruff check .`,
`uv run black --check .`). Bisher macht das jede Person von Hand auf dem
eigenen Rechner. Ob es passiert ist, sieht beim Review niemand.

Die Online-Version wird von Vercel aus GitHub gebaut und ausgeliefert
(Continuous Deployment). Eine automatische Prüfung der Tests vor dem Merge
(Continuous Integration) gab es nicht. Der Ordner `.github/workflows/`
enthielt nur den Platzhalter der Projektvorlage.

Die Tests ersetzen Datenbank, jobs.ch und OpenRouteService durch Mocks. Sie
laufen darum ohne Zugangsdaten.

## Betrachtete Optionen

- **Option 1: Weiterhin nur von Hand prüfen.** Kein Aufwand, aber
  vergessene Prüfungen fallen erst auf, wenn etwas auf `master` kaputt ist.
- **Option 2: GitHub Actions.** Eine YAML-Datei im Repository. GitHub führt
  bei jedem Push und Pull Request dieselben Befehle aus und zeigt das
  Ergebnis im Pull Request. Für öffentliche Repositories kostenlos.
- **Option 3: Prüfung bei Vercel.** Vercel baut die App nur, es führt unsere
  Unittests nicht aus.
- **Option 4: Andere CI-Dienste (GitLab CI, Jenkins).** Passen nicht, weil
  unser Code auf GitHub liegt; Jenkins bräuchte einen eigenen Server.

## Entscheidung

Option 2. Die Datei `.github/workflows/ci.yml` führt bei jedem Push und Pull
Request aus:

1. `uv sync --locked --all-groups`
2. `uv run pytest`
3. `uv run ruff check .`
4. `uv run black --check .`

Vorgeschlagen und umgesetzt von Mirko am 14.11.2026.

## Begründung

Es sind genau die Befehle, die das Team schon von Hand verwendet. Wer die
Pipeline liest, erkennt sie wieder. Die Datei ist kurz und braucht weder
neue Abhängigkeiten noch Secrets. `--locked` prüft zusätzlich, ob `uv.lock`
zur `pyproject.toml` passt, und deckt so vergessene `uv add`-Schritte auf.

## Konsequenzen

- Jeder Pull Request zeigt ein grünes Häkchen oder ein rotes Kreuz. Gemergt
  wird nur, wenn es grün ist.
- Wer committet, sollte die Befehle trotzdem lokal ausführen; die Pipeline
  meldet Fehler erst einige Minuten nach dem Push.
- Neue Tests dürfen keine echte Datenbank und keine echten Webdienste
  verwenden, sonst scheitern sie in der Pipeline ohne Zugangsdaten.
- Die Pipeline prüft nur. Das Ausliefern übernimmt weiterhin Vercel.
- Offen: GitHub kann so eingestellt werden, dass ein Merge ohne grünes
  Häkchen gar nicht möglich ist («Branch protection»). Das kann nur die
  Besitzerin des Repositories (Lina) einschalten.
