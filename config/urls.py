
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.test import Client


def test_room_status():
    response = Client().get("/api/status/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "available"
    assert data["service"] == "RoomBook"


def test_home():
    response = Client().get("/")
    assert response.status_code == 200
    assert "/api/status/" in response.json()["endpoints"]
