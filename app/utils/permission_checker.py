from fastapi import HTTPException, status
from app.models.user import User, UserRole

def is_admin(user: User) -> bool:
    """
    Check if the user has admin privileges.
    """
    return user.role == UserRole.ADMIN

def is_moderator(user: User) -> bool:
    """
    Check if the user has moderator privileges.
    """
    return user.role == UserRole.MODERATOR

def is_driver(user: User) -> bool:
    """
    Check if the user has driver privileges.
    """
    return user.role == UserRole.DRIVER

def is_customer(user: User) -> bool:
    """
    Check if the user has customer privileges.
    """
    return user.role == UserRole.CUSTOMER

def require_admin(user: User):
    """
    Raise an exception if the user is not an admin.
    """
    if not is_admin(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )

def require_moderator(user: User):
    """
    Raise an exception if the user is not a moderator.
    """
    if not (is_admin(user) or is_moderator(user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator or admin privileges required."
        )

def require_driver(user: User):
    """
    Raise an exception if the user is not a driver.
    """
    if not (is_admin(user) or is_driver(user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver or admin privileges required."
        )

def require_customer(user: User):
    """
    Raise an exception if the user is not a customer.
    """
    if not (is_admin(user) or is_customer(user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer or admin privileges required."
        )

def has_permission(user: User, required_role: UserRole) -> bool:
    """
    Generic function to check if a user has the specified role.
    """
    return user.role == required_role

def check_permission(user: User, required_role: UserRole):
    """
    Raise an exception if the user does not have the required role.
    """
    if not has_permission(user, required_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{required_role.value} privileges required."
        )
