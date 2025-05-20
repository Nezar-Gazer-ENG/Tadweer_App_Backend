from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.user import (
    create_user,
    update_user,
    suspend_user,
    reactivate_user,
    delete_user,
    list_users,
    get_user,
    grant_moderator_privileges,
    revoke_moderator_privileges
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithRoleCreate
)
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create a new user (Admin only)
@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserWithRoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user(db=db, user_data=user_data, current_user=current_user)

# Update user details (Admin only)
@user_router.put("/{user_id}", response_model=UserResponse)
def update_user_details(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user(db=db, user_id=user_id, user_data=user_data, current_user=current_user)

# Suspend a user (Admin only)
@user_router.patch("/{user_id}/suspend", status_code=status.HTTP_200_OK)
def suspend_existing_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return suspend_user(db=db, user_id=user_id, current_user=current_user)

# Reactivate a suspended user (Admin only)
@user_router.patch("/{user_id}/reactivate", status_code=status.HTTP_200_OK)
def reactivate_existing_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return reactivate_user(db=db, user_id=user_id, current_user=current_user)

# Delete a user permanently (Admin only)
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_user(db=db, user_id=user_id, current_user=current_user)

# List all users (Admin only)
@user_router.get("/", response_model=List[UserResponse])
def list_all_users(role: Optional[UserRole] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_users(db=db, role=role, current_user=current_user)

# Get user details by ID (Admin/Moderator)
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_details(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user(db=db, user_id=user_id, current_user=current_user)

# Grant moderator privileges (Admin only)
@user_router.post("/{user_id}/grant-permissions", status_code=status.HTTP_200_OK)
def grant_permissions(user_id: int, permissions: List[str], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return grant_moderator_privileges(db=db, user_id=user_id, permissions=permissions, current_user=current_user)

# Revoke moderator privileges (Admin only)
@user_router.post("/{user_id}/revoke-permissions", status_code=status.HTTP_200_OK)
def revoke_permissions(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return revoke_moderator_privileges(db=db, user_id=user_id, current_user=current_user)
