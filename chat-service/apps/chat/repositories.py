from .models import Message
from django.utils import timezone

class MessageRepository:
    @staticmethod
    def create_message(room_name, sender_id, receiver_id, content):
        return Message.objects.create(
            room_name=room_name,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
        )

    @staticmethod
    def get_messages_by_room(room_name, limit=100):
        return list(Message.objects.filter(room_name=room_name).order_by('-created_at')[:limit][::-1])

    @staticmethod
    def get_messages_between(user_a, user_b, limit=100):
        qs = Message.objects.filter(
            models.Q(sender_id=user_a, receiver_id=user_b) | models.Q(sender_id=user_b, receiver_id=user_a)
        ).order_by('-created_at')[:limit]
        return list(qs[::-1])

    @staticmethod
    def mark_read(message_id):
        try:
            m = Message.objects.get(id=message_id)
            m.is_read = True
            m.updated_at = timezone.now()
            m.save(update_fields=['is_read', 'updated_at'])
            return True
        except Message.DoesNotExist:
            return False
