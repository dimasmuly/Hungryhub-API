from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import MenuItem


class MenuItemService:
    def __init__(self, db: Session):
        self._db = db

    def create_for_restaurant(self, restaurant_id: int, data: dict) -> MenuItem:
        menu_item = MenuItem(**data, restaurant_id=restaurant_id)
        self._db.add(menu_item)
        self._db.commit()
        self._db.refresh(menu_item)
        return menu_item

    def list_for_restaurant(
        self,
        restaurant_id: int,
        category: str | None,
        search: str | None,
        page: int,
        page_size: int,
    ) -> tuple[Iterable[MenuItem], int]:
        query = select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        count_query = select(func.count(MenuItem.id)).where(
            MenuItem.restaurant_id == restaurant_id
        )

        if category:
            query = query.where(MenuItem.category == category)
            count_query = count_query.where(MenuItem.category == category)
        if search:
            pattern = f"%{search}%"
            query = query.where(MenuItem.name.ilike(pattern))
            count_query = count_query.where(MenuItem.name.ilike(pattern))

        total = self._db.execute(count_query).scalar_one()
        offset = (page - 1) * page_size
        items = (
            self._db.execute(query.offset(offset).limit(page_size))
            .scalars()
            .all()
        )
        return items, total

    def get(self, menu_item_id: int) -> MenuItem | None:
        return self._db.get(MenuItem, menu_item_id)

    def update(self, menu_item_id: int, data: dict) -> MenuItem | None:
        menu_item = self.get(menu_item_id)
        if not menu_item:
            return None
        for field, value in data.items():
            setattr(menu_item, field, value)
        self._db.add(menu_item)
        self._db.commit()
        self._db.refresh(menu_item)
        return menu_item

    def delete(self, menu_item_id: int) -> bool:
        menu_item = self.get(menu_item_id)
        if not menu_item:
            return False
        self._db.delete(menu_item)
        self._db.commit()
        return True

