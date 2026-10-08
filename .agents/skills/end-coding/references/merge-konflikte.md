# Merge-Konflikte, Rückgängig machen, Vim

Basierend auf den Kursfolien «Merge-Konflikte, Merging und der Editor Vim».

## Push abgelehnt (ohne Konflikt)

Meldung bei `git push`: `! [rejected] ... (fetch first)`. Auf GitHub gibt es
Commits, die lokal noch fehlen.

```bash
git pull --no-edit
git push
```

`--no-edit` übernimmt die vorgeschlagene Merge-Message, ohne Vim zu öffnen.

## Merge-Konflikt lösen

Meldung: `CONFLICT (content): Merge conflict in <datei>`.

1. `git status` zeigt die betroffenen Dateien unter «Unmerged paths» (in
   VS Code unter «Merge Changes»).
2. In der Datei sieht die Konfliktstelle so aus:
   ```
   <<<<<<< HEAD
   eigene Änderung
   =======
   eingehende Änderung
   >>>>>>> origin/master
   ```
3. Der Agent zeigt die Stelle, erklärt beide Seiten in einfachen Worten und
   schlägt eine Auflösung vor. Das Teammitglied entscheidet. Bei Unklarheit
   wird die Person gefragt, von der die andere Änderung stammt – sonst geht
   deren Arbeit verloren.
4. Alle Marker (`<<<<<<<`, `=======`, `>>>>>>>`) werden gelöscht, danach
   `uv run pytest`.
5. Abschliessen:
   ```bash
   git add <datei>
   git commit --no-edit
   git push
   ```

Abbrechen, falls der Konflikt später gelöst werden soll: `git merge --abort`
(stellt den Zustand vor dem Merge wieder her).

## Vim

Öffnet Git trotzdem Vim: `Esc`, dann `:wq` und Enter (speichern und
schliessen) bzw. `:q!` und Enter (ohne Speichern). Einfacheren Editor dauerhaft
setzen: `git config --global core.editor "code --wait"`.

## Häufige Fehler rückgängig machen

| Situation | Lösung |
|---|---|
| Änderung an Datei verwerfen | `git restore <datei>` (Änderung ist weg – der Agent fragt vorher) |
| Datei versehentlich gestaged | `git restore --staged <datei>` |
| Letzte Commit-Message falsch, noch nicht gepusht | `git commit --amend -m "neue Message"` |
| Bereits gepushter Commit war falsch | `git revert <commit-hash>` (erzeugt einen Gegen-Commit) |
| Auf `master` committet, noch nicht gepusht | `git switch -c feature/...`, dann `git switch master` und `git reset --hard origin/master` (nur nach Erklärung und Zustimmung) |
| `.env` oder Passwort committet | Datei in `.gitignore`, `git rm --cached <datei>`, Passwort/Key **ändern** – es bleibt in der Historie |
