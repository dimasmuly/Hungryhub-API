from decimal import Decimal

from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=50)
    opening_hours: str | None = Field(None, max_length=255)


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    address: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=50)
    opening_hours: str | None = Field(None, max_length=255)


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    category: str | None = Field(None, max_length=100)
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    category: str | None = Field(None, max_length=100)
    is_available: bool | None = None


class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True


class RestaurantRead(RestaurantBase):
    id: int

    class Config:
        from_attributes = True


class RestaurantWithMenuItems(RestaurantRead):
    menu_items: list[MenuItemRead] = []


class PaginatedRestaurants(BaseModel):
    data: list[RestaurantRead]
    page: int
    page_size: int
    total: int


class PaginatedMenuItems(BaseModel):
    data: list[MenuItemRead]
    page: int
    page_size: int
    total: int

