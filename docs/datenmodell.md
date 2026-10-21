# Datenmodell JobTracker

Stand: 2026-10-20

> **Wichtig für alle Agenten:** Dieses Dokument ist die Grundlage für das
> Programmieren. Weicht etwas, das programmiert wird, von diesem Datenmodell
> ab, muss der Nutzer das wissen. Der Agent informiert ihn, welche
> Auswirkungen die Abweichung hat und warum sie nötig ist.

## 1 Grundsätze

- Zwei Tabellen: `benutzer` und `stellenanzeigen`.
- Namen nach den Team-Konventionen in
  [`code-stil.md`](../.agents/skills/learn-coding/references/code-stil.md):
  Deutsch, `snake_case`, ohne Umlaute, Einheit im Namen. Spaltennamen und
  JSON-Felder sind identisch.
- Die Typen sind logisch angegeben. Die Datenbank ist PostgreSQL bei Neon
  ([ADR 0007](decisions/0007-postgresql-bei-neon.md)); Abschnitt 7 zeigt die
  Umsetzung, die Hinweise zu SQLite sind noch nachzuführen.
- Das Schema wird an genau einer Stelle im Code angelegt (heute
  `tabellen_erstellen()` in `src/app/datenbank.py`).
- Regeln, die die Daten schützen, prüft das Backend. Pflichtfelder, erlaubte
  Statuswerte und Eindeutigkeit sichert zusätzlich die Datenbank ab
  (`NOT NULL`, `CHECK`, `UNIQUE`). Prüfungen im Frontend sind nur Komfort.

## 2 Diagramm

```mermaid
erDiagram
    benutzer ||--o{ stellenanzeigen : besitzt
    benutzer {
        integer id PK
        text name
        text wohnadresse_strasse
        text wohnadresse_postleitzahl
        text wohnadresse_ort
        text erstellt_am
        text geaendert_am
    }
    stellenanzeigen {
        integer id PK
        integer benutzer_id FK
        text url
        text titel
        text firma
        text arbeitsort
        text inseratadresse_strasse
        text inseratadresse_postleitzahl
        text inseratadresse_ort
        text pensum
        text stellenbeschreibung
        integer lohn_in_chf_pro_jahr
        text status
        text beworben_am
        text notizen
        integer fahrzeit_auto_in_minuten
        integer strecke_auto_in_metern
        text erstellt_am
        text geaendert_am
    }
```

## 3 Tabelle `benutzer`

| Feld | Typ | Pflicht | Standard | Bedeutung und Regeln |
|---|---|---|---|---|
| `id` | Ganzzahl | ja | automatisch | Primärschlüssel |
| `name` | Text, max. 100 Zeichen | ja | | Anzeigename (Regel S3) |
| `wohnadresse_strasse` | Text, max. 200 Zeichen | nein | leer | Strasse mit Hausnummer; Startpunkt des Arbeitswegs (Regel A1) |
| `wohnadresse_postleitzahl` | Text, max. 20 Zeichen | nein | leer | Regel A1 |
| `wohnadresse_ort` | Text, max. 200 Zeichen | nein | leer | Regel A1 |
| `erstellt_am` | Zeitstempel | ja | vom Backend | Regel Z1 |
| `geaendert_am` | Zeitstempel | ja | vom Backend | Regel Z1 |

**Version 1:** höchstens ein Datensatz mit `id` 1. Er entsteht beim ersten
Speichern des Profils, nicht beim Anlegen der Tabellen. Solange er fehlt,
können keine Stellen gespeichert werden (Regel B2).
Für die öffentliche Instanz eine öffentliche Adresse verwenden (Vorschlag:
Bundesplatz 3, 3005 Bern). Es gibt keine Funktion zum Löschen von Benutzern
([ADR 0003](decisions/0003-benutzer-ohne-login.md)).

## 4 Tabelle `stellenanzeigen`

| Feld | Typ | Pflicht | Standard | Quelle | Bedeutung und Regeln |
|---|---|---|---|---|---|
| `id` | Ganzzahl | ja | automatisch | System | Primärschlüssel |
| `benutzer_id` | Ganzzahl | ja | `aktuelle_benutzer_id()` | System | Fremdschlüssel auf `benutzer.id`. Wird nie vom Frontend übernommen (Regel B1). |
| `url` | Text | ja | | Benutzer | Anzeigenlink in Normalform (Regel S1). Pro Benutzer eindeutig (Regel S2). Nach dem Anlegen nicht änderbar. |
| `titel` | Text, max. 200 Zeichen | ja | | Import oder manuell | Stellentitel |
| `firma` | Text, max. 200 Zeichen | ja | | Import oder manuell | Name des Arbeitgebers |
| `arbeitsort` | Text, max. 200 Zeichen | nein | leer | Import oder manuell | Nur zur Anzeige. Mehrere Orte durch Komma getrennt, z.B. «Bern, Zürich» ([ADR 0004](decisions/0004-adresse-getrennt-vom-arbeitsort.md)). |
| `inseratadresse_strasse` | Text, max. 200 Zeichen | nein | leer | Import oder manuell | Strasse mit Hausnummer der Arbeitsadresse; Ziel des Arbeitswegs (Regel A1) |
| `inseratadresse_postleitzahl` | Text, max. 20 Zeichen | nein | leer | Import oder manuell | Regel A1 |
| `inseratadresse_ort` | Text, max. 200 Zeichen | nein | leer | Import oder manuell | Regel A1 |
| `pensum` | Text, max. 50 Zeichen | nein | leer | Import oder manuell | Freitext wie auf jobs.ch, z.B. «60-100%». Kein Filter, keine Berechnung. |
| `stellenbeschreibung` | Text, unbegrenzt | nein | leer | Import oder manuell | Reiner Text ohne HTML (Regel S4) |
| `lohn_in_chf_pro_jahr` | Ganzzahl, mindestens 0 | nein | leer | manuell | Bruttolohn pro Jahr laut Anzeige oder Angebot. Wird nicht importiert. |
| `status` | Text | ja | `gespeichert` | Benutzer | Nur Werte aus Abschnitt 5 |
| `beworben_am` | Datum | nein | leer | Benutzer | Datum der Bewerbung. Wird nicht automatisch gesetzt. |
| `notizen` | Text, unbegrenzt | nein | leer | Benutzer | Freitext, z.B. Termin des Vorstellungsgesprächs. Wird nicht durchsucht. |
| `fahrzeit_auto_in_minuten` | Ganzzahl, mindestens 0 | nein | leer | Web Service | Geschätzte Fahrzeit mit dem Auto, einfacher Hinweg. Siehe unten. |
| `strecke_auto_in_metern` | Ganzzahl, mindestens 0 | nein | leer | Web Service | Strecke mit dem Auto; die Oberfläche zeigt Kilometer. Siehe unten. |
| `erstellt_am` | Zeitstempel | ja | vom Backend | System | Regel Z1 |
| `geaendert_am` | Zeitstempel | ja | vom Backend | System | Regel Z1 |

**Arbeitsweg** ([ADR 0008](decisions/0008-arbeitsweg-mit-openrouteservice.md)):
Das Backend berechnet Fahrzeit und Strecke bei jedem Speichern einer Stelle mit
OpenRouteService und speichert beide Werte. Leer heisst: Berechnung
gescheitert, zum Beispiel wegen einer unbrauchbaren Adresse oder weil der
Dienst nicht erreichbar war. Die Stelle wird trotzdem gespeichert.

## 5 Status

```python
ERLAUBTE_STATUS = (
    "gespeichert",
    "beworben",
    "interview",
    "zusage",
    "absage",
    "zurueckgezogen",
)
```

| Wert | Anzeige in der Oberfläche | Bedeutung |
|---|---|---|
| `gespeichert` | Gespeichert | Erfasst, noch nicht beworben. Startwert jeder neuen Stellenanzeige. |
| `beworben` | Beworben | Bewerbung abgeschickt |
| `interview` | Vorstellungsgespräch | Einladung zu einem Gespräch erhalten |
| `zusage` | Zusage | Angebot erhalten |
| `absage` | Absage | Absage erhalten |
| `zurueckgezogen` | Zurückgezogen | Bewerbung selbst zurückgezogen |

- Jeder Status darf in jeden anderen wechseln. Version 1 kennt keine
  Ablaufregeln.
- Die Anzeigetexte stehen nur im Frontend. Backend und Datenbank verwenden
  ausschliesslich die Werte.

## 6 Regeln

| Nr. | Regel |
|---|---|
| S1 | **Normalform des Links.** Akzeptiert werden Anzeigenlinks (`https://www.jobs.ch/de/stellenangebote/detail/<jobid>/`) und Suchlinks (`https://www.jobs.ch/de/stellenangebote/?...&jobid=<jobid>`). Das Backend liest die jobid, prüft sie als UUID und speichert immer `https://www.jobs.ch/de/stellenangebote/detail/<jobid>/`. Umgesetzt in `anzeigenlink_bestimmen()`. Andere Links, auch französische und englische jobs.ch-Links, werden abgelehnt. |
| S2 | **Eindeutigkeit.** Die Kombination `benutzer_id` und `url` ist eindeutig. Wer eine bereits erfasste Anzeige nochmals erfasst, erhält einen Hinweis mit der `id` des bestehenden Eintrags. |
| S3 | **Textfelder.** Leerzeichen am Anfang und Ende werden entfernt. Eine danach leere Zeichenkette wird als leer (`NULL`) gespeichert. Pflichtfelder dürfen danach nicht leer sein. Maximallängen prüft das Backend. |
| S4 | **Stellenbeschreibung.** HTML aus der Anzeige wird beim Import in reinen Text umgewandelt; Absätze bleiben als Zeilenumbrüche erhalten. Das Frontend zeigt Texte nie als HTML an (kein `v-html`). |
| A1 | **Adressen** (`inseratadresse_*`, `wohnadresse_*`) bestehen aus drei Feldern: Strasse mit Hausnummer (z.B. «Bahnhofstrasse 12»), Postleitzahl und Ort. Es gibt keine Pflicht-, Format- oder Plausibilitätsprüfung; nur die Maximallänge gilt (Regel S3). Version 1 kennt nur Schweizer Adressen ([ADR 0009](decisions/0009-adresse-in-drei-feldern.md)). |
| Z1 | **Zeitstempel** setzt nur das Backend, in UTC. `erstellt_am` beim Anlegen, `geaendert_am` bei jeder Änderung, auch bei einer reinen Statusänderung. |
| B1 | **Benutzerbezug.** Jede Abfrage und Änderung auf `stellenanzeigen` filtert über `benutzer_id = aktuelle_benutzer_id()`. Die Funktion liefert in Version 1 immer 1. Eine Stellenanzeige eines anderen Benutzers verhält sich wie nicht vorhanden ([ADR 0003](decisions/0003-benutzer-ohne-login.md)). |
| B2 | **Profil zuerst.** Eine Stellenanzeige kann erst gespeichert werden, wenn der Datensatz in `benutzer` existiert, also das Profil einmal gespeichert wurde. Fehlt er, lehnt das Backend das Speichern ab; der Fremdschlüssel `benutzer_id` sichert das zusätzlich ab. Die Oberfläche sperrt «+ Neue Stelle» ([ADR 0010](decisions/0010-minimale-oberflaeche.md)). |
| U1 | **Nicht änderbar** nach dem Anlegen: `id`, `benutzer_id`, `url`, `erstellt_am`. Fahrzeit und Strecke setzt nur das Backend. |

## 7 Typen in SQLite und PostgreSQL

| Logischer Typ | SQLite | PostgreSQL | Format in JSON |
|---|---|---|---|
| Ganzzahl | `INTEGER` | `INTEGER` | Zahl |
| Text | `TEXT` | `TEXT` | Zeichenkette |
| Datum | `TEXT`, Format `YYYY-MM-DD` | `DATE` | `"2026-10-19"` |
| Zeitstempel | `TEXT`, Format `YYYY-MM-DDTHH:MM:SSZ` | `TIMESTAMPTZ` | `"2026-10-19T08:15:00Z"` |
| leer | `NULL` | `NULL` | `null` |

Stolperfallen in SQLite:

- SQLite prüft Fremdschlüssel nur, wenn pro Verbindung
  `PRAGMA foreign_keys = ON` ausgeführt wird. Das gehört in
  `verbindung_oeffnen()`.
- SQLite erzwingt keine Maximallängen bei `TEXT`. Das Backend prüft sie
  (Regel S3).
- `LIKE` ignoriert in SQLite Gross- und Kleinschreibung nur bei Buchstaben
  ohne Umlaut: «zürich» findet «Zürich» nicht. Bei unseren Datenmengen ist es
  einfacher, eine Suche in Python mit `casefold()` zu filtern.

## 8 Schemaänderungen während der Entwicklung

`CREATE TABLE IF NOT EXISTS` legt eine Tabelle nur an, wenn sie fehlt. Neue
Spalten kommen in einer bestehenden lokalen Datenbank deshalb nicht an, und der
Code bricht mit «no such column» ab.

Teamregel, solange nur Demodaten existieren:

1. Wer das Schema ändert, schreibt das in die Beschreibung des Pull Requests.
2. Nach dem Merge löschen alle ihre lokale Datei `instance/jobtracker.db`; sie
   wird beim nächsten Start neu angelegt.
3. Sobald online echte Daten liegen, braucht es stattdessen Migrationen
   (`ALTER TABLE`).

Die Tabelle `stellenanzeigen` auf dem Branch `stellenanzeige_speichern` hat am
19.10.2026 nur `id`, `url` und `titel`. Mit diesem Datenmodell kommen die
übrigen Felder und die Tabelle `benutzer` dazu. Danach einmal die lokale Datei
löschen.

## 9 Import aus jobs.ch

Grundlage: [ADR 0006](decisions/0006-import-nur-von-jobs-ch.md).

| Feld | Quelle in der Anzeige | Stand |
|---|---|---|
| `url` | Normalform des eingegebenen Links (Regel S1) | umgesetzt |
| `titel` | erste Hauptüberschrift `h1` | umgesetzt ([Stellenlink erfassen](Use_cases/Use_Case_1/10001-stellenlink-erfassen.md)) |
| `firma` | offen; Kandidat: strukturierte Daten `JobPosting`, Feld `hiringOrganization.name` | zu prüfen |
| `arbeitsort` | Ortsangaben der Anzeige, Feld `city`; mehrere Orte durch Komma getrennt | zu prüfen |
| `inseratadresse_*` | erster Ort mit Feld `street`: `street` unverändert als Strasse mit Hausnummer, dazu `postalCode` und `city`, z.B. «Bahnhofstrasse 12» · «6300» · «Zug». Ohne `street` bleiben die Felder leer. | zu prüfen |
| `pensum` | offen; auf der Seite sichtbar | Fundstelle offen |
| `stellenbeschreibung` | offen; Kandidat: `JobPosting`, Feld `description` (HTML, Regel S4) | zu prüfen |
| `lohn_in_chf_pro_jahr`, `status`, `beworben_am`, `notizen` | nicht importiert | |

| Nr. | Regel |
|---|---|
| I1 | **Nur Daten der eigenen Anzeige.** Die Seite enthält auch Daten anderer Stellen, z.B. im Abschnitt «Andere haben sich auch angeschaut». Der Import verwendet nur Daten, die zur jobid des Links gehören, nie einfach den ersten Treffer im HTML. |
| I2 | **Nichts erfinden.** Fehlende Angaben bleiben leer. Fehlen Pflichtfelder, ergänzt der Benutzer sie im Formular vor dem Speichern. |

**Befund vom 19.10.2026.** Die Ortsangaben mit `street`, `postalCode`, `city`
und `cantonCode` sind jobs.ch-eigene Daten, kein Standardformat; ein Feld
`streetAddress` aus dem Standard schema.org wurde nicht gefunden. Für die jobid
`a1c0a39e-0de4-4f51-92aa-58e1b918b165` nennt die Detailseite laut einem
KI-Abruf «Bahnhofstrasse 12, 6300 Zug», der Quelltext der Suchseite enthielt
«Kasernenstrasse 7, 8180 Bülach». Vor der Umsetzung im Quelltext der
Detailseite prüfen, welche Ortsangabe zur jobid gehört.
