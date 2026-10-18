!! Change this document for your own project by removing the placeholder text, adding your own text, adding helpful sections etc. etc. !!

# <Project Title>

In a few sentences describe what your project is trying to solve.

You can use [GitHub markdown
notation](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
or [GitLab markdown notation](https://docs.gitlab.com/ee/user/markdown.html) in
case you are using one of these platforms. This will give a nicely formatted
documentation when looking at your project online.

## Get started

Explain what the user has to type to get started with your solution. Which one
is the main Python file? In the simplest case, this could look something like
this:

```bash
    uv run gunicorn app:app
```

or on a Windows host

```powershell
    uv run waitress-serve app:app
```

In other cases the user might have to install some project dependencies first
and has to run something like this (a pyproject.toml file is also included in
the project template):

``
    uv sync
``

## Local deployment

If you have installed Docker locally, you can test your application in a local
deployment using the `Dockerfile`. For this you first have to build the entire
application into a Docker image:

```bash
    docker build . -t webapp
```

Now you can run this Docker image and check if your server is really starting
correctly. Use the following command. Notice that the part `webapp` needs to
match with whatever you chose when creating the image in the previous step:

```bash
    docker run -p 8000:8000 webapp
```

You should now be able to open your web browser under the URL 
http://localhost:8000 and you should be greeted with a very simple page.

## Lokale SQLite-Datenbank

Für die lokale Entwicklung verwenden wir SQLite. Das Python-Modul `sqlite3`
ist bereits in Python enthalten; ein separater Datenbankserver ist nicht nötig.

- Speicherort: `instance/jobtracker.db`, relativ zum Projekt-Hauptordner.
- Tabelle: `stellenanzeigen` mit `id`, `url` und `titel`.
- Beim Speichern über `POST /api/stellenanzeigen` wird die Tabelle bei Bedarf
  angelegt und der Link mit dem bestätigten Titel gespeichert.
- Die reine Titelvorschau speichert noch keinen Eintrag.
- Die Datei bleibt lokal und wird über `/instance/` in `.gitignore` von Git
  ausgeschlossen. Jedes Teammitglied hat seine eigene Datenbank.
- Die Daten bleiben erhalten, solange diese Datei erhalten bleibt. Dies löst
  nicht die weiterhin offene dauerhafte Datenspeicherung auf Vercel.

### Einträge in VS Code ansehen

Lokal wurde die Erweiterung **SQLite Viewer** mit der Kennung
`qwtel.sqlite-viewer` installiert (festgestellte Version: 26.9.1).
Sie dient zur Ansicht der Datenbank und ist für die Anwendung nicht erforderlich.
Sie ist kein Python-Paket und gehört deshalb nicht in `pyproject.toml`.

1. In VS Code die Erweiterungen mit **Strg + Umschalt + X** öffnen.
2. Nach `qwtel.sqlite-viewer` suchen und die Erweiterung bei Bedarf installieren.
3. `instance/jobtracker.db` öffnen; falls nötig über **Öffnen mit …** die
   SQLite-Ansicht wählen.
4. Die Tabelle `stellenanzeigen` auswählen, um ID, Link und Titel zu sehen.

Die `.db`-Datei ist eine Binärdatei. Sie soll nicht als gewöhnlicher Text
bearbeitet werden. 
## Understanding the sources

Explain any high level concepts that you are using in your software. What were
your ideas for creating the whole software? What might not be apparent from the
sources alone? You can also add diagrams, photos of whiteboards or flipcharts
or even crudly drawing napkin sketches of the core concepts of your software
when they are readable and helpful for understanding.
