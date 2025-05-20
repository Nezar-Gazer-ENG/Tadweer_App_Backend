from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.utils.permission_checker import require_admin

# Helper function to get an item by ID
def get_item_by_id(db: Session, item_id: int) -> Item:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# Admin: Create a new item
def create_item(db: Session, item_data: ItemCreate, current_user) -> Item:
    require_admin(current_user)

    # Check for duplicate items
    existing_item = db.query(Item).filter(Item.name == item_data.name, Item.type == item_data.type).first()
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with the same name and type already exists."
        )

    new_item = Item(
        name=item_data.name,
        type=item_data.type,
        subtype=item_data.subtype,
        icon_url=item_data.icon_url,
        description=item_data.description,
        created_by=current_user.id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Admin: Update an existing item
def update_item(db: Session, item_id: int, item_data: ItemUpdate, current_user) -> Item:
    require_admin(current_user)

    item = get_item_by_id(db, item_id)

    # Update fields if provided
    if item_data.name:
        item.name = item_data.name
    if item_data.type:
        item.type = item_data.type
    if item_data.subtype:
        item.subtype = item_data.subtype
    if item_data.icon_url:
        item.icon_url = item_data.icon_url
    if item_data.description:
        item.description = item_data.description

    db.commit()
    db.refresh(item)
    return item

# Admin: Delete an item
def delete_item(db: Session, item_id: int, current_user):
    require_admin(current_user)

    item = get_item_by_id(db, item_id)
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

# Public: Get all items
def get_all_items(db: Session) -> List[ItemResponse]:
    items = db.query(Item).all()
    return items

# Public: Get item by ID
def get_item(db: Session, item_id: int) -> ItemResponse:
    item = get_item_by_id(db, item_id)
    return item

# Public: Filter items by type
def get_items_by_type(db: Session, item_type: str) -> List[ItemResponse]:
    items = db.query(Item).filter(Item.type == item_type).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found for the given type")
    return items
