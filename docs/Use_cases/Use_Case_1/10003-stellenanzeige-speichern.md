# US 10003 – Geprüfte Stellenanzeige in PostgreSQL speichern

Status: Implementiert; manueller Nachweis der dauerhaften Speicherung noch offen

Datum: 2026-10-20

Aktualisiert: 2026-11-17 (Abgleich mit dem aktuellen Code)

## User Story

Als Nutzerin möchte ich die geprüften und bearbeiteten Anzeigenangaben bewusst
speichern, damit sie beim nächsten Aufruf weiterhin verfügbar sind.

## Umfang

Frontend → Backend → PostgreSQL → Bestätigung mit ID und Arbeitswegergebnis.
Die funktionierende PostgreSQL-Verbindung allein erfüllt diese Story nicht.
Grundlage ist das Formular aus [US 10002](10002-weitere-felder-vorschauen.md).
Die Arbeitsadresse wird in drei Feldern gespeichert: Strasse mit Hausnummer,
Postleitzahl und Ort. Nach dem Anlegen wird die Arbeitswegberechnung aus
Use Case 3 aufgerufen; fehlende Routenergebnisse verhindern die Speicherung
der Stellenanzeige nicht.
Für den manuellen Persistenznachweis werden gespeicherte Werte über eine neue
Verbindung erneut gelesen.

## Ablauf

1. Angaben laden oder manuell erfassen und prüfen.
2. „Speichern“ anklicken.
3. Backend validiert Werte, ordnet den aktuellen Benutzer zu und speichert.
4. Use Case 3 berechnet den Arbeitsweg und speichert Fahrzeit und Strecke, soweit berechenbar.
5. Die Oberfläche zeigt die ID des gespeicherten Eintrags und den Arbeitsweg beziehungsweise einen Hinweis zur fehlgeschlagenen Berechnung. Das Formular bleibt offen; bei Eingabefehlern bleiben die Eingaben erhalten.

## Akzeptanzkriterien

- [ ] Link, Titel und Firma sind nach Normalisierung nicht leer.
- [ ] Optionale Formularwerte werden ebenfalls gespeichert; leere Werte werden NULL.
- [ ] Texttypen und vereinbarte Maximallängen werden im Backend geprüft. Die drei optionalen Adressfelder werden ohne Pflicht-, Format- oder Plausibilitätsprüfung gespeichert.
- [ ] Die URL wird ausschliesslich in der vereinbarten deutschen jobs.ch-Normalform gespeichert.
- [ ] benutzer_id kommt aus aktuelle_benutzer_id(), nie aus einer vertrauenswürdigen Annahme über Frontenddaten.
- [ ] Der Demo-Benutzer mit ID 1 ist gemäss Datenmodell vorhanden.
- [ ] Neue Einträge erhalten status „gespeichert“, eine ID und UTC-Zeitstempel.
- [ ] Ohne separate manuelle Angaben bleiben Lohn, Bewerbungsdatum und Notizen leer.
- [ ] Pro Benutzer und normalisierter URL ist nur ein Eintrag möglich.
- [ ] Ein Duplikat wird mit HTTP 400 und einem verständlichen Hinweis beantwortet; die ID des bestehenden Eintrags steht im Meldungstext.
- [ ] Ungültige Eingaben und Datenbankfehler beim Anlegen werden als Fehler gemeldet. Die Speicherung des neuen Eintrags erfolgt in einer Datenbanktransaktion.
- [ ] Gespeicherte Anzeigenangaben sind über die Leseroute aus Use Case 2 erneut abrufbar.
- [ ] Manuell noch nachzuweisen: Die Daten bleiben über einen App-Neustart beziehungsweise ein neues Deployment erhalten.

## Umsetzungsstand und Prüfung

Die Speicherroute, die Eingabeprüfung und die PostgreSQL-Speicherfunktion sind
implementiert. Vorhandene automatisierte Tests in
`tests/test_stellenanzeige_speichern.py` prüfen unter anderem bereinigte Werte,
Pflichtfelder, Maximallängen, unvollständige Adressen, die Benutzerzuordnung,
Duplikate und Fehlerantworten. Datenbankzugriffe werden dabei simuliert.
Prüfung am 17.11.2026: Alle 74 automatisierten Tests bestanden, ebenso Ruff und Black. Die Prüfungen wurden unter Windows über die jeweiligen Python-Module gestartet.
Die offenen Kontrollkästchen werden erst nach dokumentierter Prüfung der
jeweiligen Kriterien abgehakt.

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
[ADR 0003](../../decisions/0003-benutzer-ohne-login.md),
[ADR 0007](../../decisions/0007-postgresql-bei-neon.md),
[ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md) und
[ADR 0009](../../decisions/0009-adresse-in-drei-feldern.md).
