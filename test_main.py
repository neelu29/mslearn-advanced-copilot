from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root() -> None:
    """Verify that the root route redirects to the API documentation."""
    response = client.get("/")
    assert response.status_code == 200


def test_countries() -> None:
    """Verify that the countries endpoint lists every available country."""
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_country_cities() -> None:
    """Verify that the Spain city-list endpoint returns exactly Seville."""
    response = client.get("/countries/Spain")

    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_unknown_country() -> None:
    """Verify that an unknown country returns the agreed 404 response."""
    response = client.get("/countries/Atlantis")

    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}


def test_country_cities_post_not_allowed() -> None:
    """Verify that the city-list route does not accept POST requests."""
    response = client.post("/countries/Spain")

    assert response.status_code == 405


def test_country_cities_in_openapi() -> None:
    """Verify that the country city-list route is documented by OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/countries/{country}" in response.json()["paths"]


def test_seville_january_weather() -> None:
    """Verify Seville's January weather matches the stored historical data."""
    response = client.get("/countries/Spain/Seville/January")

    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}