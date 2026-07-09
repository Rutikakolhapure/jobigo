from django.db import models
import uuid

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(max_length=255, db_index=True)
    sender_id = models.UUIDField(db_index=True)
    receiver_id = models.UUIDField(db_index=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['room_name', 'created_at']),
            models.Index(fields=['sender_id', 'receiver_id']),
        ]
        ordering = ['-created_at']

    def mark_read(self):
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])
