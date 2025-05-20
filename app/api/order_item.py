from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.order_item import (
    add_order_item,
    update_order_item,
    remove_order_item,
    get_order_items,
    confirm_collected_items
)
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

order_item_router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)

# Add a new item to an order
@order_item_router.post("/{order_id}", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_order(order_id: int, item_data: OrderItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_order_item(db=db, order_id=order_id, item_data=item_data)

# Update an existing order item
@order_item_router.put("/{order_item_id}", response_model=OrderItemResponse)
def update_existing_order_item(order_item_id: int, item_data: OrderItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_order_item(db=db, order_item_id=order_item_id, item_data=item_data)

# Remove an item from an order
@order_item_router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return remove_order_item(db=db, order_item_id=order_item_id)

# Get all items associated with a specific order
@order_item_router.get("/order/{order_id}", response_model=List[OrderItemResponse])
def list_order_items(order_id: int, db: Session = Depends(get_db)):
    return get_order_items(db=db, order_id=order_id)

# Driver: Confirm collected items during mission completion
@order_item_router.post("/confirm/{order_id}", status_code=status.HTTP_200_OK)
def confirm_collected_order_items(order_id: int, collected_items: List[OrderItemUpdate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Ensure only drivers can confirm collected items
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can confirm collected items")
    return confirm_collected_items(db=db, order_id=order_id, collected_items=collected_items, current_user=current_user)
