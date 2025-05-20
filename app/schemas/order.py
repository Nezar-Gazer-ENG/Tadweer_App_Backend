from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum for order status
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# Schema for creating a new order
class OrderCreate(BaseModel):
    customer_id: int = Field(..., example=1)
    address_id: int = Field(..., example=1)
    notes: Optional[str] = Field(None, example="Handle with care")
    items: List[dict] = Field(..., example=[{"item_id": 1, "quantity": 2}])

# Schema for updating an existing order
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = Field(None, example="ASSIGNED")
    notes: Optional[str] = Field(None, example="New handling instructions")

# Schema for an item within an order
class OrderItemResponse(BaseModel):
    item_id: int
    name: str
    quantity: int
    unit_price: float
    total_price: float

# Schema for returning order details
class OrderResponse(BaseModel):
    id: int
    customer_id: int
    address_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    notes: Optional[str]
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

# Schema for deleting an order
class OrderDelete(BaseModel):
    id: int
    message: str = Field(default="Order deleted successfully.")
