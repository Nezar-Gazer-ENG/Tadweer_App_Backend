from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth import (
    signup_customer,
    login_customer,
    login_driver,
    login_admin_or_moderator,
    change_password,
    refresh_token,
    validate_token
)
from app.schemas.user import (
    UserCreate,
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    TokenData,
    SignUpRequest
)
from app.utils.dependencies import get_db
from fastapi.security import OAuth2PasswordBearer

# Router setup
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# OAuth2 scheme for extracting token from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Customer Signup
@auth_router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: SignUpRequest, db: Session = Depends(get_db)):
    return signup_customer(db=db, user_data=user_data)


# Customer Login
@auth_router.post("/login/customer", response_model=LoginResponse)
def customer_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return login_customer(db=db, login_data=login_data)

# Driver Login
@auth_router.post("/login/driver", response_model=LoginResponse)
def driver_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return login_driver(db=db, login_data=login_data)

# Admin/Moderator Login
@auth_router.post("/login/admin", response_model=LoginResponse)
def admin_or_moderator_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return login_admin_or_moderator(db=db, login_data=login_data)

# Change Password
@auth_router.post("/change-password", status_code=status.HTTP_200_OK)
def change_user_password(user_id: int, password_data: PasswordChangeRequest, db: Session = Depends(get_db)):
    return change_password(db=db, user_id=user_id, password_data=password_data)

# Refresh Token
@auth_router.post("/refresh", response_model=LoginResponse)
def refresh_access_token(token: str = Depends(oauth2_scheme)):
    return refresh_token(token)

# Validate Token
@auth_router.get("/validate", response_model=TokenData)
def validate_user_token(token: str = Depends(oauth2_scheme)):
    return validate_token(token)
