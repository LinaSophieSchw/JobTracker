# Lokaler Entwicklungsserver mit flask run statt gunicorn

Datum: 2026-10-24

## Status

Angenommen. Umgesetzt mit
[US 90001](../Use_cases/Bugs/90001-lokalen-server-stabil-starten.md).

## Kontext

Lokal wurde die App bisher mit
`uv run gunicorn --pythonpath src --bind 127.0.0.1:5001 --reload app:app`
gestartet. Beim Testen von US 30006 erschien im Browser mehrmals «Failed to
fetch». Das Server-Log zeigte:

```
objc[…]: +[NSNumber initialize] may have been in progress in another thread when fork() was called. … Crashing instead.
```

gunicorn startet mit `--reload` nach jeder Codeänderung einen neuen Worker
per `fork()`. macOS beendet diesen Worker, sobald er über `requests` ins
Internet geht (jobs.ch-Vorschau, OpenRouteService). Der Code der App ist
nicht die Ursache.

Ausserdem läuft gunicorn auf Windows nicht, und im README stand nur der
Platzhalter der Projektvorlage. Das Team hatte keinen gemeinsamen
Startbefehl.

## Betrachtete Optionen

- **Option 1: gunicorn behalten und auf macOS
  `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` vor den Befehl setzen.** Behebt
  den Absturz, wirkt aber nur auf macOS und nur, wenn man daran denkt. Auf
  Windows läuft gunicorn trotzdem nicht.
- **Option 2: Lokal den Entwicklungsserver von Flask verwenden
  (`flask run`).** Läuft auf macOS und Windows mit demselben Befehl. Beim
  Neuladen startet Flask einen neuen Prozess statt `fork()`. Er ist nur für
  die Entwicklung gedacht, nicht für den Online-Betrieb.

## Entscheidung

Option 2. Lokal wird die App mit
`uv run flask --app src/app run --debug --port 5001` gestartet. Entschieden
von Fabio, Lina und Mirko am 24.10.2026.

## Begründung

Ein einziger Befehl für alle Betriebssysteme ist für ein Team aus Anfängern
am einfachsten. Der Absturz kann mit `flask run` gar nicht auftreten, statt
dass man ihn mit einer Variable umgehen muss. Im Test auf einem Testport
wurden nach drei Neuladevorgängen alle Anfragen korrekt beantwortet.

Die Online-Version ist nicht betroffen: Vercel verwendet weder gunicorn noch
`flask run`.

## Konsequenzen

- Der Startbefehl steht im README, und in VS Code gibt es die Aufgabe
  «JobTracker starten».
- `--debug` zeigt bei einem Absturz eine Fehlerseite, auf der man Python-Code
  ausführen kann. Deshalb hört der Server nur auf `127.0.0.1`. `--debug` darf
  nie zusammen mit `--host 0.0.0.0` verwendet werden.
- Port 5001, weil auf macOS Port 5000 durch die AirPlay-Funktion belegt ist.
- `gunicorn` bleibt in der `pyproject.toml`, weil das `Dockerfile` ihn für den
  Betrieb in einem Container braucht.
- Lokal läuft ein anderer Server als online. Das war schon mit gunicorn so,
  weil Vercel die App selbst ausführt.
