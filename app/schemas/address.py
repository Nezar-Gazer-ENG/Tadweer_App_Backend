from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new address
class AddressCreate(BaseModel):
    label: Optional[str] = Field(None, example="Home")
    address_line: str = Field(..., example="123 Main St, Riyadh")
    city: str = Field(..., example="Riyadh")
    state: Optional[str] = Field(None, example="Central Province")
    postal_code: Optional[str] = Field(None, example="12345")
    latitude: float = Field(..., example=24.7136)
    longitude: float = Field(..., example=46.6753)
    place_id: Optional[str] = Field(None, example="ChIJm3_2Sd5TQj4Rw3a_HXzrRfM")
    is_default: bool = Field(default=False)

# Schema for updating an existing address
class AddressUpdate(BaseModel):
    label: Optional[str] = Field(None, example="Office")
    address_line: Optional[str] = Field(None, example="456 Business Rd, Jeddah")
    city: Optional[str] = Field(None, example="Jeddah")
    state: Optional[str] = Field(None, example="Western Province")
    postal_code: Optional[str] = Field(None, example="54321")
    latitude: Optional[float] = Field(None, example=21.4858)
    longitude: Optional[float] = Field(None, example=39.1925)
    place_id: Optional[str] = Field(None, example="ChIJrTLr-GyuEmsRBfy61i59si0")
    is_default: Optional[bool] = Field(default=False)

# Schema for returning address data
class AddressResponse(BaseModel):
    id: int
    label: Optional[str]
    address_line: str
    city: str
    state: Optional[str]
    postal_code: Optional[str]
    latitude: float
    longitude: float
    place_id: Optional[str]
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for deleting an address
class AddressDelete(BaseModel):
    id: int
    message: str = Field(default="Address deleted successfully.")
