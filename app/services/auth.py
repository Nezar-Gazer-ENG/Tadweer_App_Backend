from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.utils.jwt import create_access_token, create_refresh_token, verify_token
from app.utils.common import hash_password, verify_password
from app.schemas.user import (
    UserCreate,
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    TokenData
)

# Customer Signup
def signup_customer(db: Session, user_data: UserCreate) -> dict:
    # Check for existing username or email
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create the customer user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=UserRole.CUSTOMER,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the access token
    access_token = create_access_token(data={"sub": new_user.username, "role": new_user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

# Customer Login
def login_customer(db: Session, login_data: LoginRequest) -> LoginResponse:
    user = db.query(User).filter(User.username == login_data.username, User.role == UserRole.CUSTOMER).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return LoginResponse(access_token=access_token)

# Driver Login
def login_driver(db: Session, login_data: LoginRequest) -> LoginResponse:
    user = db.query(User).filter(User.username == login_data.username, User.role == UserRole.DRIVER).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return LoginResponse(access_token=access_token)

# Admin and Moderator Login
def login_admin_or_moderator(db: Session, login_data: LoginRequest) -> LoginResponse:
    user = db.query(User).filter(
        User.username == login_data.username,
        User.role.in_([UserRole.ADMIN, UserRole.MODERATOR])
    ).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return LoginResponse(access_token=access_token)

# Change Password
def change_password(db: Session, user_id: int, password_data: PasswordChangeRequest) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not verify_password(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid current password")

    user.password_hash = hash_password(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# Refresh Token
def refresh_token(token: str) -> dict:
    try:
        token_data = verify_token(token)
        new_token = create_access_token(data={"sub": token_data.username})
        return {"access_token": new_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired")

# Validate Token
def validate_token(token: str) -> dict:
    try:
        token_data = verify_token(token)
        return {"is_valid": True, "username": token_data.username, "role": token_data.role}
    except Exception:
        return {"is_valid": False, "message": "Invalid token"}
