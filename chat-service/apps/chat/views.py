from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .repositories import MessageRepository

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """List messages between the authenticated user and a peer. Query params: peer_id, room_name"""
        user_id = request.user.id if hasattr(request.user, 'id') else None
        peer_id = request.query_params.get('peer_id')
        room_name = request.query_params.get('room_name')
        if not room_name and not peer_id:
            return Response({'detail': 'peer_id or room_name required'}, status=status.HTTP_400_BAD_REQUEST)
        if room_name:
            messages = MessageRepository.get_messages_by_room(room_name)
        else:
            messages = MessageRepository.get_messages_between(user_id, peer_id)
        page = self.request.query_params.get('page')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        message_id = request.data.get('message_id')
        if not message_id:
            return Response({'detail': 'message_id required'}, status=status.HTTP_400_BAD_REQUEST)
        MessageRepository.mark_read(message_id)
        return Response({'status': 'ok'})
