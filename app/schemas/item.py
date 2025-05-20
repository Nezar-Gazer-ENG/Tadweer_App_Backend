from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new item
class ItemCreate(BaseModel):
    name: str = Field(..., example="Tire")
    type: str = Field(..., example="Battery")
    subtype: Optional[str] = Field(None, example="Large")
    icon_url: Optional[str] = Field(None, example="https://example.com/tire.png")
    description: Optional[str] = Field(None, example="High-quality tire for recycling")

# Schema for updating an existing item
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Battery")
    type: Optional[str] = Field(None, example="Car Battery")
    subtype: Optional[str] = Field(None, example="Mini")
    icon_url: Optional[str] = Field(None, example="https://example.com/battery.png")
    description: Optional[str] = Field(None, example="Refurbished car battery")

# Schema for item response
class ItemResponse(BaseModel):
    id: int
    name: str
    type: str
    subtype: Optional[str]
    icon_url: Optional[str]
    description: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    type: str
    subtype: Optional[str] = None
    icon_url: Optional[str] = None
    description: Optional[str] = None

# Schema for creating an item
class ItemCreate(ItemBase):
    pass

# Schema for updating an item
class ItemUpdate(ItemBase):
    name: Optional[str] = None
    type: Optional[str] = None

# Schema for deleting an item
class ItemDelete(BaseModel):
    id: int
    message: str = Field(default="Item deleted successfully.")
