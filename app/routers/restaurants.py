from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import api_key_auth
from app.schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantRead,
    RestaurantWithMenuItems,
    PaginatedRestaurants,
    PaginatedMenuItems,
    MenuItemCreate,
    MenuItemRead,
    MessageResponse,
)
from app.services.restaurants import RestaurantService
from app.services.menu_items import MenuItemService


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    dependencies=[Depends(api_key_auth)],
)


def get_restaurant_service(db: Session = Depends(get_db)) -> RestaurantService:
    return RestaurantService(db)


def get_menu_item_service(db: Session = Depends(get_db)) -> MenuItemService:
    return MenuItemService(db)


@router.post(
    "",
    response_model=RestaurantRead,
    status_code=status.HTTP_201_CREATED,
)
def create_restaurant(
    restaurant_in: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
):
    restaurant = service.create(restaurant_in.model_dump())
    return restaurant


@router.get(
    "",
    response_model=PaginatedRestaurants,
)
def list_restaurants(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: RestaurantService = Depends(get_restaurant_service),
):
    restaurants, total = service.list(page=page, page_size=page_size)
    return PaginatedRestaurants(
        data=list(restaurants),
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantWithMenuItems,
)
def get_restaurant(
    restaurant_id: int = Path(..., ge=1),
    service: RestaurantService = Depends(get_restaurant_service),
):
    restaurant = service.get(restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    return restaurant


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantRead,
)
def update_restaurant(
    restaurant_id: int,
    restaurant_in: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
):
    update_data = restaurant_in.model_dump(exclude_unset=True)
    restaurant = service.update(restaurant_id, update_data)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    return restaurant


@router.delete(
    "/{restaurant_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def delete_restaurant(
    restaurant_id: int = Path(..., ge=1),
    service: RestaurantService = Depends(get_restaurant_service),
):
    deleted = service.delete(restaurant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    return MessageResponse(message="Restaurant deleted successfully")


@router.get(
    "/{restaurant_id}/menu_items",
    response_model=PaginatedMenuItems,
)
def list_menu_items_for_restaurant(
    restaurant_id: int,
    category: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
    menu_item_service: MenuItemService = Depends(get_menu_item_service),
):
    restaurant = restaurant_service.get(restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    items, total = menu_item_service.list_for_restaurant(
        restaurant_id=restaurant_id,
        category=category,
        search=search,
        page=page,
        page_size=page_size,
    )
    return PaginatedMenuItems(
        data=list(items),
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post(
    "/{restaurant_id}/menu_items",
    response_model=MenuItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item_for_restaurant(
    restaurant_id: int,
    menu_item_in: MenuItemCreate,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
    menu_item_service: MenuItemService = Depends(get_menu_item_service),
):
    restaurant = restaurant_service.get(restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    menu_item = menu_item_service.create_for_restaurant(
        restaurant_id=restaurant_id,
        data=menu_item_in.model_dump(),
    )
    return menu_item
