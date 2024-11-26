from django.db import models
from enumfields import EnumField
from enum import Enum
import uuid


class MessageStatus(Enum):
    READ = "read"
    UNREAD = "unread"


class ContactMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    status = EnumField(MessageStatus, default=MessageStatus.UNREAD, max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def is_unread(self):
        return self.status == MessageStatus.UNREAD
    
    class Meta:
        ordering = ["-sent_at"]