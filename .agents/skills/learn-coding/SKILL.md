---
name: learn-coding
description: Hilft Programmier-Anfängern im SWEN-Projekt (HSLU), Features als Vertical Slice (Frontend → Backend → Datenbank) zu bauen und den Code dabei zu verstehen – der Agent baut in kleinen, lauffähigen Schritten im Stil der Codebeispiele aus dem Unterricht und erklärt jeden Schritt in einfachen Worten, damit das Team den Code in der Präsentation erklären kann. Der Skill wird immer verwendet, wenn jemand etwas programmieren, eine User Story oder ein Feature umsetzen, eine Seite, Route, Funktion, Datenbanktabelle oder einen Test schreiben, einen Fehler im Code beheben oder bestehenden Code erklärt haben will, z. B. «bau das Formular für neue Bewerbungen», «wir brauchen eine Liste aller Jobs», «wie speichere ich das in der Datenbank?», «da kommt ein Fehler» oder «erklär mir, was diese Datei macht». Vorher hilft start-coding beim Start, danach end-coding beim Abschliessen.
---

# Learn Coding

Das Team besteht aus Programmier-Anfängern. In der Präsentation (40 % der
Note) haben sich die Dozierenden vorher den Code angeschaut und stellen 1–2
Fragen dazu; bewertet wird, ob das Team den eigenen Code erklären kann. Ziel
dieses Skills ist deshalb nicht nur funktionierender Code, sondern Code, den
das Team versteht.

Der Agent schreibt den Code selbst und erklärt jeden Schritt so, dass ein
Anfänger ihn nacherzählen kann. Er fragt das Team nicht ab und lässt keine
Lücken zum Selberfüllen – das Verstehen entsteht über gute Erklärungen. Er
antwortet auf Deutsch.

## Grundprinzipien aus dem Unterricht

- **Vertical Slicing:** Eine User Story wird als dünner Schnitt durch alle
  Schichten gebaut – ein bisschen Frontend, ein bisschen Backend, ein bisschen
  Datenbank – statt zuerst das ganze Frontend und dann das ganze Backend.
  So läuft nach jedem Schritt etwas im Browser, Fehler zeigen sich früh, und
  jedes Teammitglied kann einen ganzen Ablauf von Klick bis Datenbank
  präsentieren.
- **Zerlegen:** Grosse Aufgaben werden in kleine Schritte geteilt, die je für
  sich ausprobiert werden können.
- **Gesamtbild im Auge behalten:** Bei jedem Schritt sagt der Agent, wo im
  Bild Frontend → Backend → Datenbank man gerade ist.

Details, Reihenfolge der Schritte und ein Beispiel stehen in
`references/vertical-slicing.md`. Der Agent liest diese Datei, bevor er einen
Slice plant.

## Ablauf

1. **User Story und Slice planen.** Der Agent formuliert die Aufgabe als User
   Story in einem Satz («Als Bewerber:in möchte ich …, damit …»). Ist sie zu
   gross, teilt er sie in mehrere Slices und beginnt mit dem dünnsten. Dann
   zeigt er den Plan:
   - was danach im Browser funktioniert,
   - die Schritte in der Reihenfolge aus `references/vertical-slicing.md`,
     jeweils mit Schicht (Frontend, Backend, Datenbank) und betroffener Datei,
   - das Schichtenbild mit dem aktuellen Stand.

   Sind wichtige Entscheidungen offen (Technologie, Umfang, wo die Logik
   hingehört), nutzt der Agent zuerst den Skill
   `challenge-development-decisions`. Erst nach dem OK des Teams beginnt er.

2. **Schritt für Schritt bauen.** Ein Schritt ist ein Stück, das man danach
   ausprobieren kann, z. B. eine Route, ein Formular, eine Tabelle. Den Code
   schreibt der Agent im Stil von `references/code-stil.md`. Nach jedem
   Schritt:
   - **Erklären:** Immer im festen Format aus
     `references/erklaer-format.md`: Überschrift «Schritt N ist fertig: …»,
     welche Datei ab welcher Zeile geändert wurde, «Wozu gibt es den neuen
     Teil?» mit Beispiel und «Was der neue Teil macht, der Reihe nach» – pro
     Funktion die Codestücke in Reihenfolge, je `codestück` → Erklärung, mit
     dem Warum. Das gilt nach **jeder** Umsetzung im Code, auch bei
     Vereinfachungen und Korrekturen; eine kurze Stichwortliste der
     geänderten Dateien genügt nicht. Neue Begriffe (Route, Request, JSON,
     SQL-Abfrage, …) erklärt der Agent beim ersten Auftreten in einem Satz,
     wenn möglich mit einem Alltagsvergleich.
   - **Gesamtbild:** Das Schichtenbild mit dem neuen Stand.
   - **Ausprobieren:** Wie man das Ergebnis sieht – App starten, welche URL
     öffnen, was dort erscheinen sollte.
   - Erst dann folgt der nächste Schritt.

   Fragt das Teammitglied nach, erklärt der Agent es anders, mit einem
   Vergleich oder einem kleineren Beispiel, statt dieselben Worte zu
   wiederholen.

3. **Test dazu.** Zu jedem neuen Stück Logik schreibt der Agent einen
   Unittest in `tests/` (Stil siehe `references/code-stil.md`), erklärt in
   einem Satz, was er prüft, und führt ihn mit `uv run pytest` aus.
   Unittests werden bewertet.

4. **Zusammenfassung für die Präsentation.** Am Ende eines Slices schreibt
   der Agent kurz:
   - **Ablauf:** 3–5 Sätze, was vom Klick im Browser bis zur Datenbank und
     zurück passiert, mit den Namen der beteiligten Dateien und Funktionen.
   - **Knackpunkt:** Die schwierigste Stelle dieses Slices und wie sie gelöst
     wurde – ein Kandidat für die «technische Herausforderung» in der
     Präsentation.
   - **Mögliche Dozierenden-Fragen:** 2 Fragen, die man zu diesem Code
     stellen könnte, je mit einer kurzen Antwort.

   Dann weist er darauf hin, dass der Skill `end-coding` beim Committen und
   Pushen hilft. Ein fertiger Slice ist ein guter Moment für einen Commit.

## Bestehenden Code erklären

Will jemand Code verstehen («was macht diese Datei?», «erklär mir die Route»),
ändert der Agent nichts, sondern geht den Code von oben nach unten in
sinnvollen Blöcken durch (nicht jede triviale Zeile einzeln): pro Block was
er tut und warum. Er ordnet ihn ins Schichtenbild ein und zeigt, welcher
Request ihn auslöst. Zum Schluss ein Satz, was die Datei als Ganzes leistet.
Das gilt auch für Code von anderen Teammitgliedern – in der Präsentation muss
jede Person auch die Teile der anderen grob erklären können.

## Fehler beheben

Bei einer Fehlermeldung liest der Agent sie mit dem Teammitglied: welche
Zeile, was die Meldung in einfachen Worten bedeutet und in welcher Schicht der
Fehler entsteht (Browser-Konsole, Flask-Terminal, Test). Dann behebt er die
Ursache, nicht nur das Symptom, und erklärt, warum der Fehler passiert ist und
wie man ihn nächstes Mal selbst erkennt.

## Regeln für den Code

- **Einfach vor elegant:** kurze Funktionen, sprechende Namen, keine cleveren
  Tricks. Was ein Anfänger nicht lesen kann, kann er nicht präsentieren.
- **Stil wie in den Codebeispielen** aus dem Unterricht: Namenskonventionen
  von Python (`snake_case`, `PascalCase`, `KONSTANTEN`), Team-Konventionen
  (deutsche Namen, Einheiten im Namen, max. 88 Zeichen pro Zeile, max. 3
  Verschachtelungsebenen), Docstrings und Kommentare, die das *Warum* und den
  Denkweg erklären – siehe `references/code-stil.md`.
- **Technologien laut Kursempfehlung:** Backend mit Flask oder FastAPI,
  Frontend ohne Build-Tools (z. B. Vue 3 über CDN, HTMX oder einfaches
  JavaScript), eine SQL-Datenbank. Neue Bibliotheken nur nach Rückfrage und
  dann mit `uv add <paket>`.
- **Styling zuletzt:** Das UI muss funktionieren, nicht schön sein. CSS kommt
  erst, wenn der Slice durchläuft, und nur wenn das Team es will.
- **Projektstruktur einhalten:** Backend in `src/app/`, Frontend in
  `src/app/static/`, Tests in `tests/` (siehe `docs/directories.md`).
- **Keine Geheimnisse im Code:** Passwörter und API-Keys gehören in eine
  `.env`-Datei, nicht in den Code.
- **Projekt-relative Pfade**, keine absoluten wie `/Users/...`.
- **Eigene Lösung statt Tutorial-Kopie:** Die Bewertung fragt, ob das Projekt
  mehr ist als die Umsetzung eines Tutorials. Der Agent passt Beispiele an das
  eigene Projekt an, statt sie eins zu eins zu übernehmen.
