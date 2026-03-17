from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Restaurant, MenuItem


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

API_KEY_HEADER = {"X-API-Key": "supersecretapikey"}


def test_create_and_get_restaurant():
    response = client.post(
        "/restaurants",
        json={
            "name": "Test Restaurant",
            "address": "Test Address",
            "phone": "123456789",
            "opening_hours": "09:00 - 21:00",
        },
        headers=API_KEY_HEADER,
    )
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]
    assert data["name"] == "Test Restaurant"

    response = client.get(
        f"/restaurants/{restaurant_id}",
        headers=API_KEY_HEADER,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == restaurant_id
    assert data["menu_items"] == []


def test_add_menu_items_and_list_with_pagination_and_filter():
    response = client.post(
        "/restaurants",
        json={
            "name": "Menu Test Restaurant",
            "address": "Another Address",
        },
        headers=API_KEY_HEADER,
    )
    assert response.status_code == 201
    restaurant_id = response.json()["id"]

    items = [
        {
            "name": "Item A",
            "description": "Desc A",
            "price": "10.00",
            "category": "appetizer",
            "is_available": True,
        },
        {
            "name": "Item B",
            "description": "Desc B",
            "price": "20.00",
            "category": "main",
            "is_available": True,
        },
        {
            "name": "Item C",
            "description": "Desc C",
            "price": "30.00",
            "category": "main",
            "is_available": False,
        },
    ]
    for item in items:
        r = client.post(
            f"/restaurants/{restaurant_id}/menu_items",
            json=item,
            headers=API_KEY_HEADER,
        )
        assert r.status_code == 201

    response = client.get(
        f"/restaurants/{restaurant_id}/menu_items",
        headers=API_KEY_HEADER,
        params={"page": 1, "page_size": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert len(data["data"]) == 2

    response = client.get(
        f"/restaurants/{restaurant_id}/menu_items",
        headers=API_KEY_HEADER,
        params={"category": "main"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    categories = {item["category"] for item in data["data"]}
    assert categories == {"main"}

    response = client.get(
        f"/restaurants/{restaurant_id}/menu_items",
        headers=API_KEY_HEADER,
        params={"search": "Item B"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Item B"


def test_auth_required():
    response = client.get("/restaurants")
    assert response.status_code == 422 or response.status_code == 401

