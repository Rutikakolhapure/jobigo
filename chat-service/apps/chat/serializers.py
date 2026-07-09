from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room_name', 'sender_id', 'receiver_id', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
