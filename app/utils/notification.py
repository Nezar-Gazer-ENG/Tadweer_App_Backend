from app.models.notification import Notification
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

def send_notification(db: Session, recipient_id: int, message: str, notification_type: str = "GENERAL") -> Notification:
    """
    Create and store a new notification for a user.
    """
    try:
        notification = Notification(
            recipient_id=recipient_id,
            message=message,
            type=notification_type,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error sending notification: {str(e)}")

def get_unread_notifications(db: Session, user_id: int) -> List[Notification]:
    """
    Retrieve all unread notifications for a specific user.
    """
    try:
        return db.query(Notification).filter(
            Notification.recipient_id == user_id,
            Notification.is_read == False
        ).all()
    except Exception as e:
        raise RuntimeError(f"Error retrieving unread notifications: {str(e)}")

def mark_notification_as_read(db: Session, notification_id: int) -> bool:
    """
    Mark a specific notification as read.
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id
        ).first()

        if notification:
            notification.is_read = True
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error marking notification as read: {str(e)}")

def mark_all_as_read(db: Session, user_id: int) -> int:
    """
    Mark all notifications for a user as read.
    Returns the number of notifications updated.
    """
    try:
        notifications = db.query(Notification).filter(
            Notification.recipient_id == user_id,
            Notification.is_read == False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.commit()
        return len(notifications)
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error marking all notifications as read: {str(e)}")

def delete_notification(db: Session, notification_id: int) -> bool:
    """
    Delete a specific notification.
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id
        ).first()

        if notification:
            db.delete(notification)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error deleting notification: {str(e)}")

def get_all_notifications(db: Session, user_id: int) -> List[Notification]:
    """
    Retrieve all notifications for a user.
    """
    try:
        return db.query(Notification).filter(
            Notification.recipient_id == user_id
        ).order_by(Notification.created_at.desc()).all()
    except Exception as e:
        raise RuntimeError(f"Error retrieving all notifications: {str(e)}")
