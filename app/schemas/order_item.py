from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new order item
class OrderItemCreate(BaseModel):
    order_id: int = Field(..., example=1)
    item_id: int = Field(..., example=101)
    quantity: int = Field(..., example=2)
    unit_price: float = Field(..., example=50.0)

# Schema for updating an existing order item
class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, example=3)
    unit_price: Optional[float] = Field(None, example=45.0)

# Schema for returning order item details
class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    unit_price: float
    total_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for deleting an order item
class OrderItemDelete(BaseModel):
    id: int
    message: str = Field(default="Order item deleted successfully.")
