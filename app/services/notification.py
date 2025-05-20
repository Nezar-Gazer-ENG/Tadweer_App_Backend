from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.schemas.notification import NotificationResponse
from app.utils.notification import (
    send_notification,
    get_unread_notifications,
    mark_notification_as_read,
    mark_all_as_read,
    delete_notification,
    get_all_notifications
)

# Send a notification (internal use)
def create_notification(db: Session, recipient_id: int, message: str, notification_type: str = "GENERAL") -> dict:
    try:
        notification = send_notification(db, recipient_id, message, notification_type)
        return {"message": "Notification sent successfully", "notification_id": notification.id}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Get all notifications for a specific user
def list_notifications(db: Session, user_id: int) -> List[NotificationResponse]:
    try:
        notifications = get_all_notifications(db, user_id)
        if not notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
        return notifications
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Get unread notifications for a specific user
def list_unread_notifications(db: Session, user_id: int) -> List[NotificationResponse]:
    try:
        notifications = get_unread_notifications(db, user_id)
        if not notifications:
            return []
        return notifications
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Mark a specific notification as read
def mark_notification_read(db: Session, notification_id: int) -> dict:
    try:
        success = mark_notification_as_read(db, notification_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found or already read")
        return {"message": "Notification marked as read"}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Mark all notifications as read for a user
def mark_all_notifications_read(db: Session, user_id: int) -> dict:
    try:
        count = mark_all_as_read(db, user_id)
        if count == 0:
            return {"message": "No unread notifications found"}
        return {"message": f"{count} notifications marked as read"}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete a specific notification
def remove_notification(db: Session, notification_id: int) -> dict:
    try:
        success = delete_notification(db, notification_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return {"message": "Notification deleted successfully"}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
