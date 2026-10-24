# Learninglog – Mirko

### 2026-10-24 – Use Case 2 dokumentieren: README und US 20001

**Was haben wir gemacht?**
Für Use Case 2 (Stellenanzeigen verwalten) ein README erstellt: Ziel,
Story-Liste US 20001 bis US 20005 mit Endpunkten, Oberfläche, Abgrenzung zu
Use Case 1 und Use Case 3, offene und entschiedene Punkte
(`docs/Use_cases/Use_Case_2/README.md`). Danach die erste Story ausführlich nach
der Vorlage der anderen Use Cases geschrieben
(`docs/Use_cases/Use_Case_2/20001-uebersicht-aller-stellen.md`). Commit
`c2b7641` auf dem Branch `docs/20000-use-case-2`.

**Warum haben wir das gemacht?**
Die Story-Liste hängt vom Umfang ab. Steht der Umfang fest, müssen die Stories
später nicht umgebaut werden. Bewusst wird nur die erste Story ausführlich
geschrieben und umgesetzt, bevor die nächste folgt. Alternative wäre gewesen,
alle Stories vorab zu schreiben, wie bei Use Case 1 und Use Case 3.

**Welche Auswirkungen hat das?**
- Entscheide von Mirko: Status-Dropdown im Formular statt in der Übersicht;
  keine Suche und kein Filter (wie in ADR 0010 vorgeschlagen); vorerst keine
  Maske zum Ändern des Profils, der Demo-Benutzer bleibt fest hinterlegt.
- Abgesprochen mit der verantwortlichen Person von Use Case 1: Die Übersicht
  wird zur Startseite, Mirko baut die Umschaltung in `public/index.html`, die
  Person von Use Case 1 prüft den Pull Request.
- Offen: Mit Fabio klären, wer den `PUT` für bestehende Stellen baut (vor
  US 20003). ADR 0010 hat noch den Status «Vorgeschlagen»; die Annahme ist ein
  Teamentscheid.

**Welche Konzepte wurden behandelt?**
- Vertical Slice: eine Story geht vom Frontend über das Backend bis zur
  Datenbank; zuerst Lesen (US 20001), dann Schreiben (US 20003).
- Pull Request: Anfrage, einen Branch nach einem Review in `master` zu
  übernehmen.
- Branch und Worktree: Ein Branch ist ein Entwicklungsstrang in Git, ein
  Worktree ein zusätzlicher Ordner, in dem ein Branch ausgecheckt ist.

**Eigenleistung und KI-Unterstützung**
- Mirko: Entscheide zu Status-Dropdown, Suche/Filter, Profilmaske und Sortierung
  (neueste zuerst); Absprache mit Use Case 1; Prüfung der Story-Liste.
- KI (Claude): Lesen der Projektdokumente, Vorschlag der Story-Liste, Entwurf
  von README und US 20001, Commit und Push nach Zustimmung.

**Persönliche Reflexion – von Mirko zu ergänzen**
Antwort auf die Kontrollfrage, warum die Person von Use Case 1 den Pull Request
prüft: «weil sie Überschneidungen hat mit meinem UC und die Änderungen sie
betreffen.»

Offen: Was kann ich jetzt selbst erklären, und was würde ich bei der nächsten
Story anders machen?

**Nächster Lernschritt**
US 20001 umsetzen, beginnend mit der Datenbankfunktion in `datenbank.py`.
Offene Kontrollfrage: Warum ist es sinnvoll, US 20001 (nur lesen) vor US 20003
(speichern) umzusetzen?
