# Learninglog – Fabio

## 2026-10-20 – Wireframes, Prototyp und Entscheide zur Oberfläche

**Was haben wir gemacht?**
Fabio liess Wireframes und einen klickbaren Prototyp erstellen, um zu sehen,
welche Screens und Funktionen die Applikation braucht
([docs/wireframes](../../wireframes/README.md)). Ergebnis sind drei Screens
(Übersicht, Stellen-Formular, Profil) und eine Liste der nötigen
Backend-Aufrufe. Daraus entstanden die Entscheide
[ADR 0008](../../decisions/0008-arbeitsweg-mit-openrouteservice.md) bis
[ADR 0010](../../decisions/0010-minimale-oberflaeche.md). Linas Entscheidung
zu PostgreSQL wurde als
[ADR 0007](../../decisions/0007-postgresql-bei-neon.md) nachgetragen.
Datenmodell und Stories von Use Case 3 wurden angeglichen. Die Stories von
Use Case 1 passt die Person an, die Use Case 1 bearbeitet.

**Warum haben wir das gemacht?**
Die Use Cases standen einzeln nebeneinander, und es fehlte eine Vorstellung,
wie die Applikation als Ganzes funktioniert. Die Wireframes dienten nicht dem
Design, sondern dem Verständnis der Abläufe.

**Welche Auswirkungen hat das?**
Beim Zeichnen wurden Widersprüche zwischen Dokumenten sichtbar, zum Beispiel
beim Adressformat und beim externen Dienst. Fabio
legte fest:

- Adressen ändern gehört zu Use Case 2.
- Felder für Arbeitsadresse und Arbeitsweg gehören zum Formular von Use Case 1,
  ebenso das Profil mit Wohnadresse. Die Stories dazu bleiben in Use Case 3
  nur als Reserve (US 30004 und 30005).
- Use Case 3 berechnet nur den Arbeitsweg, mit OpenRouteService.
- «+ Neue Stelle» ist gesperrt, bis ein Profil gespeichert ist.
- Es gibt keine Hinweis- oder Erfolgsmeldungen.

Die Vorschläge (ADR 0009 und 0010) muss das Team noch bestätigen.

**Welche Konzepte wurden behandelt?**
Wireframe und klickbarer Prototyp als Mittel, Anforderungen zu klären;
Zuordnung von Funktionen zu Use Cases; Decision Records mit Status
«Vorgeschlagen» und «Ersetzt durch».

**Eigenleistung und KI-Unterstützung**
Fabio gab Ziel und Rahmen vor, beantwortete die offenen Fragen und traf die
oben genannten Entscheide. Die Stories zu Use Case 3 brachte er mit; wie sie
entstanden sind, ist hier nicht festgehalten. Der Agent zeichnete Wireframes
und Prototyp, wies auf Widersprüche hin und entwarf die ADRs sowie die
Anpassungen an Datenmodell und Stories.

**Persönliche Reflexion – von Fabio zu ergänzen**
Was hat das Durchklicken des Prototyps gezeigt, das in den Use-Case-Texten
nicht sichtbar war?

**Nächster Lernschritt**
Mit dem Team die vorgeschlagenen ADRs im
Pull Request besprechen.

## 2026-10-21 – Fest hinterlegter Benutzer statt Profilerfassung

**Was haben wir gemacht?**
Die Stories von Use Case 3 wurden an die Teambesprechung vom 21.10.2026
angepasst. US 30004 beschreibt neu, dass ein Demo-Benutzer mit Wohnadresse in
drei Feldern fest im System hinterlegt wird
([US 30004](../../Use_cases/Use_Case_3/30004-demo-benutzer-fest-hinterlegen.md)).
Sie ist keine Reserve mehr, sondern die erste Story von Use Case 3. Die
Stories 30001 bis 30003, 30005 und das
[README](../../Use_cases/Use_Case_3/README.md) verweisen nicht mehr auf ein
Profil.

**Warum haben wir das gemacht?**
Die Absprache vom Montag zum Profil wurde im Team unterschiedlich verstanden.
Im Code ist bereits ein Dummy-Benutzer angelegt, dem alle Stellen zugeordnet
werden. Das Team lässt das vorläufig so, bis geklärt ist, wer das Profil
anlegen übernimmt. Fabio legte fest, dass das Hardcoden des Benutzers eine
eigene Story in Use Case 3 ist und es keine Maske zur Erfassung des Nutzers
gibt.

**Welche Auswirkungen hat das?**
Stellen können ohne vorheriges Profil gespeichert werden. Die
Arbeitswegberechnung liest die Wohnadresse des Demo-Benutzers aus der
Datenbank. Offen: Im Code liegt die Wohnadresse noch in einer einzigen Spalte;
Datenmodell (Abschnitt 3, Regel B2) und ADR 0010 gehen noch von einer
Profilerfassung und einer Sperre von «+ Neue Stelle» aus. Der Eintrag vom
20.10.2026 nennt US 30004 noch als Reserve; das ist damit überholt.

**Welche Konzepte wurden behandelt?**
Testdaten bzw. Seed-Daten, die beim Anlegen der Datenbank eingefügt werden;
Abhängigkeiten zwischen Stories und deren Reihenfolge.

**Eigenleistung und KI-Unterstützung**
Fabio brachte das Ergebnis der Teambesprechung ein und entschied, das
Hardcoden als Story zu führen. Der Agent formulierte US 30004 neu, passte die
übrigen Stories und das README an und wies auf die offenen Widersprüche in
Datenmodell, ADR 0010 und Code hin.

**Persönliche Reflexion – von Fabio zu ergänzen**
Was hätte geholfen, das Missverständnis zur Absprache vom Montag früher zu
bemerken?

**Nächster Lernschritt**
Mit Lina klären, wer die Umstellung der Wohnadresse auf drei Spalten übernimmt
und wer Datenmodell und ADR 0010 anpasst.
