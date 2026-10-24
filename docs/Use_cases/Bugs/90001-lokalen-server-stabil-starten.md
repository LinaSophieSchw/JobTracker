# US 90001 – Lokalen Server auf allen Rechnern gleich und stabil starten

Status: Geplant (Absprache mit Lina und Mirko offen)

Datum: 2026-10-24

Art: Infrastruktur / Bug

## User Story

Als Entwickler im Team möchte ich die App lokal mit einem einzigen, im README beschriebenen Befehl starten, der auf macOS und Windows gleich funktioniert und nach Codeänderungen nicht abstürzt, damit ich neue Versionen zuverlässig testen kann.

## Ausgangslage

Beim Testen von US 30006 erschien im Browser mehrmals **«Failed to fetch»**, beim Laden einer Anzeige und beim Speichern. Ursache war nicht der Code der App, sondern der lokale Server:

- Lokal wurde mit `uv run gunicorn --pythonpath src --bind 127.0.0.1:5001 --reload app:app` gestartet.
- Bei jeder Codeänderung startet gunicorn mit `--reload` einen neuen Worker per `fork()`.
- macOS beendet diesen Worker sofort, sobald er über `requests` ins Internet geht (jobs.ch-Vorschau, OpenRouteService). Der Browser bekommt dann gar keine Antwort.
- gunicorn läuft auf Windows grundsätzlich nicht. Im README steht dafür nur der Platzhalter der Projektvorlage (`uv run gunicorn app:app` bzw. `uv run waitress-serve app:app`), und dort fehlt `--pythonpath src`. Es gibt also keinen gemeinsamen Startbefehl im Team.

## Umfang des ersten Vertical Slice

Für die lokale Entwicklung wird der eingebaute Entwicklungsserver von Flask verwendet:

```bash
uv run flask --app src/app run --debug --port 5001
```

Gemeinsame Festlegungen für diesen Slice:

- **Nur die lokale Entwicklung ändert sich.** Die Online-Version auf Vercel und das `Dockerfile` mit gunicorn bleiben unverändert. `gunicorn` bleibt in der `pyproject.toml`.
- **Ein Befehl für alle Betriebssysteme.** Der Befehl ist auf macOS und in der Windows-PowerShell gleich.
- **Port 5001**, weil auf macOS Port 5000 durch die AirPlay-Funktion belegt ist.
- **`--debug` nur lokal.** Der Server hört nur auf `127.0.0.1`. `--debug` darf nie zusammen mit `--host 0.0.0.0` verwendet werden, weil man über die Fehlerseite dann aus dem Netzwerk Python-Code ausführen könnte.
- **Der Code in `src/` bleibt unverändert.**
- Der Entscheid wird als ADR festgehalten, weil er die Werkzeuge des ganzen Teams betrifft.

## Ablauf

1. Ein Teammitglied holt den neusten Stand und führt `uv sync --all-groups` aus.
2. Es startet den Server mit dem Befehl aus dem README oder in VS Code über die Aufgabe «JobTracker starten».
3. Es öffnet http://localhost:5001 im Browser.
4. Es ändert Code. Der Server lädt neu, und Vorschau sowie Speichern funktionieren weiterhin.
5. Erscheint trotzdem «Failed to fetch», schaut es zuerst ins Terminal, in dem der Server läuft. Dort steht die Ursache.
6. Mit `Ctrl+C` beendet es den Server.

## Akzeptanzkriterien

- [ ] Der Abschnitt «Get started» im README nennt den Befehl `uv sync --all-groups` und den Startbefehl. Der Platzhaltertext in diesem Abschnitt ist ersetzt.
- [ ] Das README erklärt in einem Satz, warum lokal `flask run` statt gunicorn verwendet wird.
- [ ] Das README warnt, `--debug` nicht mit `--host 0.0.0.0` zu verwenden.
- [ ] Das README erklärt, dass man bei «Failed to fetch» zuerst ins Server-Terminal schaut.
- [ ] In VS Code gibt es eine Aufgabe «JobTracker starten», die den Server mit demselben Befehl startet.
- [ ] Nach einer Codeänderung lädt der Server neu, und eine Vorschau sowie das Speichern liefern weiterhin eine Antwort statt «Failed to fetch».
- [ ] Der Start ist auf macOS geprüft und, falls im Team vorhanden, auf einem Windows-Rechner.
- [ ] `src/`, `Dockerfile`, `pyproject.toml` und die Vercel-Konfiguration bleiben unverändert.
- [ ] Ein ADR zum lokalen Entwicklungsserver liegt in `docs/decisions`.

## Schrittweise Umsetzung

1. Im Team entscheiden: lokal `flask run` statt gunicorn. Ergebnis als ADR 0012 festhalten.
2. README: Abschnitt «Get started» mit Startbefehl, Begründung, Warnung zu `--debug` und Hinweis zu «Failed to fetch» schreiben.
3. `.vscode/tasks.json`: Aufgabe «JobTracker starten» ergänzen.
4. Auf macOS prüfen: Server starten, Codeänderung auslösen, Vorschau und Speichern testen.
5. Ein Teammitglied mit Windows prüft den Start, falls vorhanden.

## Noch nicht enthalten

- Die übrigen Platzhalter im README (Projektbeschreibung, «Understanding the sources»).
- Lokales Testen mit Docker.
- Änderungen am Deployment auf Vercel.
- Automatische Tests auf GitHub (CI).
- Aufräumen von `MANUAL.md` und Vorlagencode wie `src/app/static/`.

## Technische Prüfung vor der Umsetzung

### Befund vom 24.10.2026

| Frage | Befund |
|---|---|
| Was zeigt der Browser? | `POST /api/stellenanzeigen/vorschau` und `POST /api/stellenanzeigen` enden mit `net::ERR_EMPTY_RESPONSE`. Der Server antwortet gar nicht. |
| Was zeigt das Server-Log? | `objc[…]: +[NSNumber initialize] may have been in progress in another thread when fork() was called. … Crashing instead.` Danach: `Worker (pid: …) was sent SIGKILL!` |
| Wann tritt es auf? | Nach einem `Worker reloading` wegen einer Codeänderung, z. B. nach `git pull`. Ein frisch gestarteter Server funktioniert zuerst. |
| Liegt es am Code? | Nein. Derselbe Code funktioniert mit einem neu gestarteten Server und mit `flask run`. |
| Notlösung auf macOS | `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` vor den gunicorn-Befehl setzen. Funktioniert, aber nur auf macOS und nur, wenn man daran denkt. |
| Test mit `flask run` | Auf Testport 5098: drei Codeänderungen mit Neuladen ausgelöst, danach jede Vorschau-Anfrage korrekt beantwortet, kein Absturz. Flask startet beim Neuladen einen neuen Prozess statt `fork()`. |
| Windows | gunicorn läuft auf Windows nicht. `flask run` läuft auf allen Betriebssystemen. Auf Windows noch nicht praktisch getestet. |
