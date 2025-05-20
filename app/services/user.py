from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.utils.common import hash_password
from app.utils.permission_checker import require_admin
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithRoleCreate
)

# Helper function to find a user by ID
def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Admin: Create a new moderator or driver
def create_user(db: Session, user_data: UserWithRoleCreate, current_user: User) -> User:
    require_admin(current_user)

    # Hash the temporary password
    hashed_password = hash_password(user_data.temporary_password)

    # Check for existing username or email
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

    # Create the new user (moderator or driver)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Admin: Update a user's details
def update_user(db: Session, user_id: int, user_data: UserUpdate, current_user: User) -> User:
    require_admin(current_user)

    user = get_user_by_id(db, user_id)

    # Update fields if provided
    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.password_hash = hash_password(user_data.password)
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    return user

# Admin: Suspend a user (moderator or driver)
def suspend_user(db: Session, user_id: int, current_user: User):
    require_admin(current_user)

    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    return {"message": f"User {user.username} has been suspended."}

# Admin: Reactivate a suspended user
def reactivate_user(db: Session, user_id: int, current_user: User):
    require_admin(current_user)

    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    return {"message": f"User {user.username} has been reactivated."}

# Admin: Permanently delete a user (only admins can delete)
def delete_user(db: Session, user_id: int, current_user: User):
    require_admin(current_user)

    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} has been permanently deleted."}

# Admin: List all users or filter by role
def list_users(db: Session, role: Optional[UserRole], current_user: User) -> list:
    require_admin(current_user)

    query = db.query(User)
    if role:
        query = query.filter(User.role == role)

    return query.all()

# Admin/Moderator: Get a specific user's details
def get_user(db: Session, user_id: int, current_user: User) -> User:
    user = get_user_by_id(db, user_id)

    # Moderators can view only other moderators or drivers
    if current_user.role == UserRole.MODERATOR and user.role not in [UserRole.DRIVER, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderators can only view other moderators or drivers."
        )

    return user

# Admin: Grant additional privileges to a moderator
def grant_moderator_privileges(db: Session, user_id: int, permissions: list, current_user: User):
    require_admin(current_user)

    user = get_user_by_id(db, user_id)
    if user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a moderator.")

    # Add the granted permissions
    user.permissions = permissions
    db.commit()
    return {"message": f"Moderator {user.username} has been granted additional privileges."}

# Admin: Revoke privileges from a moderator
def revoke_moderator_privileges(db: Session, user_id: int, current_user: User):
    require_admin(current_user)

    user = get_user_by_id(db, user_id)
    if user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a moderator.")

    # Clear the permissions list
    user.permissions = []
    db.commit()
    return {"message": f"All privileges for moderator {user.username} have been revoked."}
