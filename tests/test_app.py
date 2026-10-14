"""Tests für das Grundgerüst des Backends.

Sie prüfen, ob die Flask-App startet und ihre ersten zwei Adressen
beantwortet. Ein echter Server ist dafür nicht nötig.
"""

from app import app


# Requirement 1: Das Backend meldet, dass es läuft
def test_status_route_antwortet_mit_ok():
    # Der Test-Client spielt den Browser: Er schickt eine Anfrage an die
    # App, ohne dass ein echter Server laufen muss.
    client = app.test_client()
    antwort = client.get("/api/status")
    assert antwort.status_code == 200
    assert antwort.get_json() == {"status": "ok"}


# Requirement 2: Die Startseite wird ausgeliefert
def test_startseite_wird_ausgeliefert():
    client = app.test_client()
    antwort = client.get("/")
    assert antwort.status_code == 200
    assert b"JobTracker" in antwort.data
