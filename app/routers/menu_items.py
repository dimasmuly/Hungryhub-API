from fastapi import APIRouter, Depends, HTTPException, status, Path

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import api_key_auth
from app.schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemRead,
    PaginatedMenuItems,
    MessageResponse,
)
from app.services.menu_items import MenuItemService


router = APIRouter(
    prefix="/menu_items",
    tags=["menu_items"],
    dependencies=[Depends(api_key_auth)],
)


def get_menu_item_service(db: Session = Depends(get_db)) -> MenuItemService:
    return MenuItemService(db)


@router.put(
    "/{menu_item_id}",
    response_model=MenuItemRead,
)
def update_menu_item(
    menu_item_id: int,
    menu_item_in: MenuItemUpdate,
    service: MenuItemService = Depends(get_menu_item_service),
):
    update_data = menu_item_in.model_dump(exclude_unset=True)
    menu_item = service.update(menu_item_id, update_data)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found",
        )
    return menu_item


@router.delete(
    "/{menu_item_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def delete_menu_item(
    menu_item_id: int = Path(..., ge=1),
    service: MenuItemService = Depends(get_menu_item_service),
):
    deleted = service.delete(menu_item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found",
        )
    return MessageResponse(message="Menu item deleted successfully")
