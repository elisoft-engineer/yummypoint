from .models import Notification
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

def create_notification(user, message: str, link: str | None = None):
    if not isinstance(user, User) or not user or not user.is_active:
        logger.warning("Invalid or inactive user provided for notification.")
        return None

    if not message:
        logger.warning("Notification message cannot be empty.")
        return None

    try:
        notification = Notification.objects.create(user=user, message=message, link=link)
        return notification
    except Exception as e:
        logger.error(f"Failed to create notification: {e}")
        return None