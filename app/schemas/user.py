from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# Schema for user sign-up request
class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str



# Schema for login request
class LoginRequest(BaseModel):
    username: str
    password: str

# Schema for login response
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schema for token data
class TokenData(BaseModel):
    username: Optional[str] = None

# Schema for token refresh
class TokenRefresh(BaseModel):
    refresh_token: str

# Schema for token validation response
class TokenValidation(BaseModel):
    is_valid: bool
    message: Optional[str] = None

# Schema for user sign-up request
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for updating user data
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for user response after successful sign-up
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    # Use `from_attributes` for Pydantic v2 compatibility
    class Config:
        from_attributes = True

# Schema for user with role assignment (Admin creating moderators/drivers)
class UserWithRoleCreate(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    temporary_password: str

# Schema for forcing password change on first login
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

# Schema for password reset
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Schema for response after password change or reset
class PasswordChangeResponse(BaseModel):
    message: str
