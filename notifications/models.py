from django.db import models
from accounts.models import User
from uuid import uuid4
from enumfields import EnumField
from enum import Enum
from django.utils.timezone import now
from datetime import timedelta


"""
This file holds the notification model.
"""


class NotificationStatus(Enum):
    READ = "read"
    UNREAD = "unread"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    link = models.URLField(null=True)
    status = EnumField(NotificationStatus, default=NotificationStatus.UNREAD, null=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message if len(str(self.message)) <= 30 else f"{self.message[:30]} ..."
    
    class Meta:
        ordering = ["-created_at"]

    @property
    def is_unread(self):
        return self.status == NotificationStatus.UNREAD
    
    @property
    def get_humanized_time(self):
        diff = now() - self.created_at
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(days=2):
            return "Yesterday"
        elif diff < timedelta(weeks=1):
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        elif diff < timedelta(weeks=4):
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        else:
            return self.created_at.strftime("%b %d, %Y")
