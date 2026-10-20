# US 10003 – Geprüfte Stellenanzeige in PostgreSQL speichern

Status: Geplant

Datum: 2026-10-20

## User Story

Als Nutzerin möchte ich die geprüften und bearbeiteten Anzeigenangaben bewusst
speichern, damit sie beim nächsten Aufruf weiterhin verfügbar sind.

## Umfang

Frontend → Backend → PostgreSQL → Bestätigung.
Die funktionierende PostgreSQL-Verbindung allein erfüllt diese Story nicht.
Grundlage ist das Formular aus [US 10002](10002-weitere-felder-vorschauen.md).
Gespeicherte Werte werden für den Nachweis über eine neue Verbindung wieder gelesen.

## Ablauf

1. Angaben laden oder manuell erfassen und prüfen.
2. „Speichern“ anklicken.
3. Backend validiert Werte, ordnet den aktuellen Benutzer zu und speichert.
4. Oberfläche bestätigt die Speicherung; bei Fehlern bleiben Eingaben erhalten.

## Akzeptanzkriterien

- [ ] Link, Titel und Firma sind nach Normalisierung nicht leer.
- [ ] Optionale Formularwerte werden ebenfalls gespeichert; leere Werte werden NULL.
- [ ] Maximallängen und eine gegebenenfalls angegebene Schweizer Adresse werden im Backend geprüft.
- [ ] Die URL wird ausschliesslich in der vereinbarten deutschen jobs.ch-Normalform gespeichert.
- [ ] benutzer_id kommt aus aktuelle_benutzer_id(), nie aus einer vertrauenswürdigen Annahme über Frontenddaten.
- [ ] Der Demo-Benutzer mit ID 1 ist gemäss Datenmodell vorhanden.
- [ ] Neue Einträge erhalten status „gespeichert“, eine ID und UTC-Zeitstempel.
- [ ] Ohne separate manuelle Angaben bleiben Lohn, Bewerbungsdatum und Notizen leer.
- [ ] Pro Benutzer und normalisierter URL ist nur ein Eintrag möglich.
- [ ] Ein Duplikat wird mit verständlichem Hinweis und ID des bestehenden Eintrags beantwortet.
- [ ] Fehler führen nicht zu einer Erfolgsmeldung oder einem unvollständigen Datensatz.
- [ ] Nach erfolgreichem Speichern sind die bestätigten Werte erneut abrufbar.
- [ ] Die Daten bleiben über einen App-Neustart beziehungsweise ein neues Deployment erhalten.

## Prüfung

Validierung und Fehlerpfade automatisiert prüfen.
Schreiben und Lesen zusätzlich gegen eine ausdrücklich gewählte Testdatenbank
prüfen; keine produktiven Datensätze für automatisierte Tests verwenden.
Manueller Online-Nachweis von Speichern und erneutem Lesen erforderlich.

## Noch nicht enthalten

Eine vollständige Übersicht, Filter und die Verwaltung bestehender Einträge
gehören zu Use Case 2. Keine Anmeldung, kein Versenden einer Bewerbung.

## Grundlagen

[Datenmodell](../../datenmodell.md), Tabellen benutzer und stellenanzeigen,
Regeln S1–S3, A1, Z1 und B1;
[ADR 0003](../../decisions/0003-benutzer-ohne-login.md).
