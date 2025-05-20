from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.order import (
    create_order,
    update_order,
    cancel_order,
    list_all_orders,
    get_order,
    confirm_order_items
)
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.order_item import OrderItemUpdate
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# Create a new order (Customer)
@order_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can create orders")
    return create_order(db=db, order_data=order_data, customer_id=current_user.id)

# Update an existing order (Admin/Moderator)
@order_router.put("/{order_id}", response_model=OrderResponse)
def update_existing_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can update orders")
    return update_order(db=db, order_id=order_id, order_data=order_data, current_user=current_user)

# Cancel an order (Customer)
@order_router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def cancel_existing_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can cancel orders")
    return cancel_order(db=db, order_id=order_id, customer_id=current_user.id)

# Get all orders (Admin/Moderator)
@order_router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can view all orders")
    return list_all_orders(db=db, current_user=current_user)

# Get a specific order by ID (Admin/Moderator/Customer)
@order_router.get("/{order_id}", response_model=OrderResponse)
def get_order_details(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_order(db=db, order_id=order_id, current_user=current_user)

# Driver: Confirm collected items in an order
@order_router.post("/{order_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_collected_order_items(order_id: int, collected_items: List[OrderItemUpdate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can confirm collected items")
    return confirm_order_items(db=db, order_id=order_id, collected_items=collected_items, current_user=current_user)
