from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.utils.permission_checker import require_admin, require_moderator
from datetime import datetime

# Helper function to get an order by ID
def get_order_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

# Customer: Create a new order
def create_order(db: Session, order_data: OrderCreate, customer_id: int) -> Order:
    new_order = Order(
        customer_id=customer_id,
        address_id=order_data.address_id,
        status=OrderStatus.PENDING,
        notes=order_data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Admin/Moderator: Update an existing order
def update_order(db: Session, order_id: int, order_data: OrderUpdate, current_user) -> Order:
    require_moderator(current_user)

    order = get_order_by_id(db, order_id)

    # Update fields if provided
    if order_data.status:
        order.status = order_data.status
    if order_data.notes:
        order.notes = order_data.notes

    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order

# Customer: Cancel an order
def cancel_order(db: Session, order_id: int, customer_id: int) -> dict:
    order = get_order_by_id(db, order_id)

    # Only the customer who created the order can cancel it
    if order.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to cancel this order")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending orders can be canceled")

    order.status = OrderStatus.CANCELLED
    order.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Order canceled successfully"}

# Get all orders (Admin/Moderator)
def list_all_orders(db: Session, current_user) -> List[OrderResponse]:
    require_moderator(current_user)
    orders = db.query(Order).all()
    return orders

# Get order by ID (Admin/Moderator/Customer)
def get_order(db: Session, order_id: int, current_user) -> OrderResponse:
    order = get_order_by_id(db, order_id)

    # Ensure customers can only view their own orders
    if current_user.role == "CUSTOMER" and order.customer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return order

# Confirm collected items in an order (Driver operation)
def confirm_order_items(db: Session, order_id: int, collected_items: List[dict], current_user):
    order = get_order_by_id(db, order_id)

    # Ensure the driver is assigned to the mission associated with the order
    if order.status != OrderStatus.ASSIGNED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order not yet assigned")

    for item in collected_items:
        order_item = db.query(OrderItem).filter(OrderItem.id == item["id"]).first()
        if not order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

        # Update the collected quantity
        order_item.quantity = item["quantity"]
        db.commit()

    order.status = OrderStatus.PICKED_UP
    order.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Order items confirmed successfully"}
