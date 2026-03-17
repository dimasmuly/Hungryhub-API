from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Restaurant


class RestaurantService:
    def __init__(self, db: Session):
        self._db = db

    def create(self, data: dict) -> Restaurant:
        restaurant = Restaurant(**data)
        self._db.add(restaurant)
        self._db.commit()
        self._db.refresh(restaurant)
        return restaurant

    def list(self, page: int, page_size: int) -> tuple[Iterable[Restaurant], int]:
        total = self._db.execute(select(func.count(Restaurant.id))).scalar_one()
        offset = (page - 1) * page_size
        restaurants = (
            self._db.execute(
                select(Restaurant).offset(offset).limit(page_size)
            )
            .scalars()
            .all()
        )
        return restaurants, total

    def get(self, restaurant_id: int) -> Restaurant | None:
        return self._db.get(Restaurant, restaurant_id)

    def update(self, restaurant_id: int, data: dict) -> Restaurant | None:
        restaurant = self.get(restaurant_id)
        if not restaurant:
            return None
        for field, value in data.items():
            setattr(restaurant, field, value)
        self._db.add(restaurant)
        self._db.commit()
        self._db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant_id: int) -> bool:
        restaurant = self.get(restaurant_id)
        if not restaurant:
            return False
        self._db.delete(restaurant)
        self._db.commit()
        return True

