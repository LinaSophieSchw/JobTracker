# Ordnerstruktur

Diese Datei erklärt, welche Ordner und Dateien es im JobTracker gibt und wozu
sie dienen. Welche Funktion in welcher Python-Datei steckt, steht im README
unter «Wo finde ich was im Code?».

## Code

 * `src/app/` enthält das Backend in Python mit Flask.
   `__init__.py` erstellt die Flask-App, die übrigen Dateien enthalten die
   Routen, den Zugriff auf die Datenbank, das Auslesen von jobs.ch und die
   Berechnung des Arbeitswegs.
 * `public/` enthält das Frontend: `index.html` mit Vue 3 und Bootstrap über
   CDN sowie das Favicon. Online liefert Vercel diesen Ordner direkt aus,
   lokal liefert ihn Flask aus.
 * `tests/` enthält die Unittests für pytest. Externe Dienste wie die
   Datenbank und OpenRouteService werden darin durch Mocks ersetzt.

## Dokumentation

 * `docs/decisions/` enthält die Architekturentscheide (ADRs), fortlaufend
   nummeriert. Neue Entscheide basieren auf `docs/decision-template.md`.
 * `docs/Use_cases/` enthält die drei Use Cases mit ihren User Stories und
   unter `Bugs/` die dokumentierten Fehler.
 * `docs/datenmodell.md` beschreibt die Tabellen in der Datenbank.
 * `docs/wireframes/` enthält die Wireframes und den Prototyp der Oberfläche.
 * `docs/reflection/` enthält pro Person einen Learninglog zur Vorbereitung
   der Reflexion.
 * `docs/agent-collaboration.md` beschreibt die Zusammenarbeit mit
   KI-Agenten.

## Werkzeuge und Konfiguration

 * `.github/workflows/ci.yml` ist die CI-Pipeline mit GitHub Actions
   (ADR 0016).
 * `.agents/skills/` enthält die Skills für KI-Agenten. `.claude/skills/`
   verweist für Claude Code auf dieselben Dateien.
 * `.vscode/` enthält Einstellungen und Tasks für VS Code, zum Beispiel
   «JobTracker starten».
 * `AGENTS.md` enthält die Anweisungen für KI-Agenten in diesem Projekt.
 * `pyproject.toml` und `uv.lock` halten die Abhängigkeiten fest. Pakete
   werden mit `uv add …` und `uv remove …` hinzugefügt oder entfernt.
 * `Dockerfile` beschreibt einen Container mit gunicorn. Für das Deployment
   auf Vercel wird es nicht gebraucht (ADR 0012).
 * `.env` enthält lokal die Datenbankadresse und den API-Schlüssel. Sie ist
   in `.gitignore` eingetragen und kommt nie ins Repository.
 * `.mailmap` fasst die Autorennamen in der Git-History pro Person zusammen.
