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
