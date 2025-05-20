from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.notification import (
    create_notification,
    list_notifications,
    list_unread_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    remove_notification
)
from app.schemas.notification import NotificationResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User

notification_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# Send a notification (internal use)
@notification_router.post("/", status_code=status.HTTP_201_CREATED)
def send_notification(recipient_id: int, message: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_notification(db=db, recipient_id=recipient_id, message=message)

# Get all notifications for the current user
@notification_router.get("/", response_model=List[NotificationResponse])
def get_all_user_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_notifications(db=db, user_id=current_user.id)

# Get unread notifications for the current user
@notification_router.get("/unread", response_model=List[NotificationResponse])
def get_unread_user_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_unread_notifications(db=db, user_id=current_user.id)

# Mark a specific notification as read
@notification_router.patch("/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_as_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return mark_notification_read(db=db, notification_id=notification_id)

# Mark all notifications as read
@notification_router.patch("/mark-all-read", status_code=status.HTTP_200_OK)
def mark_all_as_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return mark_all_notifications_read(db=db, user_id=current_user.id)

# Delete a specific notification
@notification_router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_notification(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return remove_notification(db=db, notification_id=notification_id)
