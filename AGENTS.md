## Technology stack

This project represents a web application with a backend and a frontend part.
The backend is to be kept completely in Python. The frontend stack can be chosen
freely.

 * We use `uv` for any Python related tasks

## Files and directories

 * Check `docs/directories.md` for the directory structure of this project.
 * The backend is a Flask application in `src/app/`. `src/app/__init__.py`
   exposes the Flask application object named `app`.
 * The frontend lives in `public/index.html` (Vue 3 and Bootstrap via CDN).
   Vercel serves `public/` directly; locally, Flask serves the same folder.
 * The application is deployed automatically to Vercel on every push to
   `master`. Locally it is started with `flask run` (ADR 0012).

## Design guidelines

This is a project that is to be developed in the course of a master degree in
business informatics. The focus is on exploring and learning about all the parts
involved in running a full web application rather than building a fully
productive, scalable and long-term maintainable application. The created
elements should be easy to understand.

 * When discussing design options, start with the simpler options; for example
   suggest to start with Flask or Starlette rather than Django, suggest vanilla
   JavaScript, HTMX or Alpine.js rather than going straight for full fledged
   solutions like Angular or React. Accept more complex solutions once the
   developers made it clear that they are needed and they understand the
   implications.
 * Prefer frontend technologies that can be used through CDN and don't need any
   frontend build steps.
 * For WSGI/ASGI start with either Gunicorn or Uvicorn depending on the web
   framework used.
 * Document architectural design decisions that were discussed with the
   developers in the folder `docs/decisions`. Use a new file for every decision
   and use a continuous numbering scheme in the form
   `0001-framework-choice.md`.

## Educational collaboration

This template is used for learning software development, not only for producing
code. When students ask an agent to add a feature, choose a technology, or make
an architectural change, the agent should first help them reason about the
decision before implementing it.

Reusable guidance for this behavior is stored as the generic agent skill
`.agents/skills/challenge-development-decisions`. Agents that support skills
should use that skill for feature requests, technology choices, architecture
placement questions, and decision records in this project.

Decision records for this project belong in `docs/decisions` and should be
based on `docs/decision-template.md`.


## Git workflow

The team members are Git and programming beginners. Three skills cover the
workflow:

 * `.agents/skills/start-coding` – when someone starts a new task: get the
   latest code, sync dependencies, create a feature branch.
 * `.agents/skills/learn-coding` – while programming: build each user story
   as a vertical slice (frontend → backend → database) in small, runnable
   steps, write code in the style of the course examples and explain every
   step in simple German, so the team can explain the code in the
   presentation.
 * `.agents/skills/end-coding` – when someone is done: check changes, write
   a German commit message with a type prefix such as `feat:`, commit, push
   and open a pull request.

For Claude Code all three skills are also registered in `.claude/skills/`, which
only point to the shared files above.

## Learninglog zur Reflexionsvorbereitung

Verwende `.agents/skills/learninglog/SKILL.md` nach relevanten abgeschlossenen
Arbeitsschritten, wichtigen Entscheidungen oder gelösten Problemen sowie auf
ausdrücklichen Wunsch. Kläre die aktive Person, sofern sie nicht eindeutig ist.

Führe getrennte Learninglogs:

 * Lina: `docs/reflection/Lina/learninglog_lina.md`
 * Mirko: `docs/reflection/Mirko/learninglog_mirko.md`
 * Fabio: `docs/reflection/Fabio/learninglog_fabio.md`

Erstelle Ordner und Datei beim ersten relevanten Eintrag automatisch, sofern
Änderungen im Projektordner erlaubt sind. Halte beobachtbare Arbeit und
KI-Unterstützung fest; persönliche Reflexionen dürfen nicht erfunden werden.
Der Skill ist auch unter `.claude/skills/learninglog/` als Verweis registriert.
