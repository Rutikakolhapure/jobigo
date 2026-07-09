from django.db import models
import uuid

class Embedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, db_index=True)  # e.g., 'job:<job_id>' or 'resume:<user_id>'
    text = models.TextField()
    vector = models.TextField()  # JSON serialized list of floats
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['source']),
        ]
