from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.item import Item
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from app.utils.permission_checker import require_admin, require_moderator

# Helper function to get an order item by ID
def get_order_item_by_id(db: Session, order_item_id: int) -> OrderItem:
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return order_item

# Add a new item to an order
def add_order_item(db: Session, order_id: int, item_data: OrderItemCreate) -> OrderItem:
    # Validate order existence
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Validate item existence
    item = db.query(Item).filter(Item.id == item_data.item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    # Check for existing order item combination
    existing_order_item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.item_id == item_data.item_id
    ).first()

    if existing_order_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already exists in this order"
        )

    # Calculate total price
    total_price = item_data.quantity * item_data.unit_price

    new_order_item = OrderItem(
        order_id=order_id,
        item_id=item_data.item_id,
        quantity=item_data.quantity,
        unit_price=item_data.unit_price,
        total_price=total_price
    )
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return new_order_item

# Update an existing order item
def update_order_item(db: Session, order_item_id: int, item_data: OrderItemUpdate) -> OrderItem:
    order_item = get_order_item_by_id(db, order_item_id)

    # Update fields if provided
    if item_data.quantity:
        order_item.quantity = item_data.quantity
        order_item.total_price = order_item.quantity * order_item.unit_price
    if item_data.unit_price:
        order_item.unit_price = item_data.unit_price
        order_item.total_price = order_item.quantity * order_item.unit_price

    db.commit()
    db.refresh(order_item)
    return order_item

# Remove an item from an order
def remove_order_item(db: Session, order_item_id: int):
    order_item = get_order_item_by_id(db, order_item_id)
    db.delete(order_item)
    db.commit()
    return {"message": "Order item removed successfully"}

# Get all items associated with a specific order
def get_order_items(db: Session, order_id: int) -> List[OrderItemResponse]:
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    if not order_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found for this order")
    return order_items

# Confirm collected items (Driver operation)
def confirm_collected_items(db: Session, order_id: int, collected_items: List[OrderItemUpdate], current_user):
    for item_data in collected_items:
        order_item = get_order_item_by_id(db, item_data.id)
        
        # Validate that the driver is handling the correct order
        if order_item.order_id != order_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Order item does not belong to the specified order"
            )
        
        # Update collected quantity
        if item_data.quantity:
            order_item.quantity = item_data.quantity
            order_item.total_price = order_item.quantity * order_item.unit_price
        db.commit()
        db.refresh(order_item)

    return {"message": "Collected items confirmed successfully"}
