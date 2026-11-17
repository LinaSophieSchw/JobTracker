## Technologie

Dieses Projekt ist eine Webapplikation mit einem Backend und einem Frontend.
Das Backend ist vollständig in Python geschrieben. Das Frontend ist frei
wählbar.

 * Für alle Aufgaben rund um Python verwenden wir `uv`.

## Dateien und Ordner

 * Die Ordnerstruktur des Projekts steht in `docs/directories.md`.
 * Das Backend ist eine Flask-App in `src/app/`. `src/app/__init__.py`
   stellt das Flask-Objekt mit dem Namen `app` bereit.
 * Das Frontend liegt in `public/index.html` (Vue 3 und Bootstrap über CDN).
   Vercel liefert `public/` direkt aus; lokal liefert Flask denselben Ordner
   aus.
 * Die Applikation wird bei jedem Push auf `master` automatisch auf Vercel
   deployt. Lokal wird sie mit `flask run` gestartet (ADR 0012).

## Gestaltungsrichtlinien

Das Projekt entsteht im Modul SWEN an der HSLU. Im Vordergrund steht, alle
Teile einer vollständigen Webapplikation kennenzulernen, nicht eine produktive,
skalierbare und langfristig wartbare Applikation zu bauen. Was entsteht, soll
leicht verständlich sein.

 * Bei Designfragen zuerst die einfacheren Varianten vorschlagen, zum Beispiel
   Flask oder Starlette statt Django und einfaches JavaScript, HTMX oder
   Alpine.js statt umfangreicher Frameworks wie Angular oder React.
   Komplexere Lösungen erst übernehmen, wenn das Team klar gemacht hat, dass
   sie nötig sind, und die Folgen versteht.
 * Frontend-Technologien bevorzugen, die über CDN eingebunden werden können
   und keinen Build-Schritt brauchen.
 * Als WSGI- bzw. ASGI-Server je nach Webframework mit Gunicorn oder Uvicorn
   beginnen.
 * Architekturentscheide, die mit dem Team besprochen wurden, im Ordner
   `docs/decisions` festhalten. Für jeden Entscheid eine eigene Datei mit
   fortlaufender Nummer im Format `0001-framework-wahl.md` anlegen.

## Lernen statt nur Code erzeugen

Das Projekt dient dazu, Softwareentwicklung zu lernen, nicht nur Code zu
erzeugen. Wenn das Team einen Agenten bittet, ein Feature umzusetzen, eine
Technologie zu wählen oder die Architektur zu ändern, hilft der Agent zuerst,
den Entscheid zu durchdenken, und setzt ihn erst danach um.

Die Anleitung dafür steht im Skill
`.agents/skills/challenge-development-decisions`. Agenten, die Skills
unterstützen, verwenden ihn bei Feature-Wünschen, Technologiewahl, Fragen zur
Platzierung in der Architektur und bei Entscheidungsdokumenten.

Entscheidungsdokumente gehören nach `docs/decisions` und basieren auf
`docs/decision-template.md`.

## Git-Ablauf

Das Team besteht aus Anfängern in Git und Programmierung. Drei Skills decken
den Ablauf ab:

 * `.agents/skills/start-coding`: wenn jemand eine neue Aufgabe beginnt.
   Neuesten Stand holen, Abhängigkeiten aktualisieren, Feature-Branch anlegen.
 * `.agents/skills/learn-coding`: während des Programmierens. Jede User Story
   als Vertical Slice (Frontend → Backend → Datenbank) in kleinen, lauffähigen
   Schritten umsetzen, Code im Stil der Codebeispiele aus dem Unterricht
   schreiben und jeden Schritt in einfachem Deutsch erklären, damit das Team
   den Code in der Präsentation erklären kann.
 * `.agents/skills/end-coding`: wenn jemand fertig ist. Änderungen prüfen,
   eine deutsche Commit-Message mit Typ-Präfix wie `feat:` schreiben,
   committen, pushen und einen Pull Request öffnen.

Für Claude Code sind diese drei Skills zusätzlich in `.claude/skills/`
eingetragen. Diese Einträge verweisen nur auf die gemeinsamen Dateien oben.

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
