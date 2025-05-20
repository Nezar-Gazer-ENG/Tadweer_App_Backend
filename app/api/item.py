from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.item import (
    create_item,
    update_item,
    delete_item,
    get_all_items,
    get_item,
    get_items_by_type
)
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User

item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# Create a new item (Admin only)
@item_router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_new_item(item_data: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_item(db=db, item_data=item_data, current_user=current_user)

# Update an existing item (Admin only)
@item_router.put("/{item_id}", response_model=ItemResponse)
def update_existing_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_item(db=db, item_id=item_id, item_data=item_data, current_user=current_user)

# Delete an item (Admin only)
@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_item(db=db, item_id=item_id, current_user=current_user)

# Get all items (Public)
@item_router.get("/", response_model=List[ItemResponse])
def list_all_items(db: Session = Depends(get_db)):
    return get_all_items(db=db)

# Get a specific item by ID (Public)
@item_router.get("/{item_id}", response_model=ItemResponse)
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    return get_item(db=db, item_id=item_id)

# Get items filtered by type (Public)
@item_router.get("/type/{item_type}", response_model=List[ItemResponse])
def get_items_by_type_name(item_type: str, db: Session = Depends(get_db)):
    return get_items_by_type(db=db, item_type=item_type)
