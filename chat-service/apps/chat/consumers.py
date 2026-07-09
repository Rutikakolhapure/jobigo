import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import jwt
from django.conf import settings
from .repositories import MessageRepository
from .services import PresenceService

class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for one-to-one chat.

    Connection URL: ws://host/ws/chat/<room_name>/?token=JWT
    """

    async def connect(self):
        # Authenticate token
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        query_string = self.scope.get('query_string', b'').decode()
        token = None
        if 'token=' in query_string:
            # crude parse
            parts = query_string.split('&')
            for p in parts:
                if p.startswith('token='):
                    token = p.split('token=')[1]
        self.user = None
        if token:
            try:
                if settings.AUTH_JWT_PUBLIC_KEY:
                    payload = jwt.decode(token, settings.AUTH_JWT_PUBLIC_KEY, algorithms=[settings.AUTH_JWT_ALGORITHM])
                else:
                    payload = jwt.decode(token, settings.AUTH_JWT_SECRET, algorithms=[settings.AUTH_JWT_ALGORITHM])
                self.user = payload
            except Exception as e:
                await self.close(code=4001)
                return
        else:
            await self.close(code=4003)
            return

        # Join room group
        self.group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Mark online
        await PresenceService.mark_online(self.user.get('user_id'))
        # Broadcast presence
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'presence.update',
                'user_id': self.user.get('user_id'),
                'online': True,
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if self.user:
            await PresenceService.mark_offline(self.user.get('user_id'))
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'presence.update',
                    'user_id': self.user.get('user_id'),
                    'online': False,
                }
            )

    # Receive from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        data = json.loads(text_data)
        event = data.get('type')
        if event == 'message.send':
            content = data.get('content')
            sender = self.user.get('user_id')
            receiver = data.get('receiver_id')
            # Persist message
            message = await database_sync_to_async(MessageRepository.create_message)(
                room_name=self.room_name,
                sender_id=sender,
                receiver_id=receiver,
                content=content,
            )
            payload = {
                'type': 'chat.message',
                'message': {
                    'id': str(message.id),
                    'room_name': message.room_name,
                    'sender_id': str(message.sender_id),
                    'receiver_id': str(message.receiver_id),
                    'content': message.content,
                    'is_read': message.is_read,
                    'created_at': message.created_at.isoformat(),
                }
            }
            await self.channel_layer.group_send(self.group_name, payload)

        elif event == 'typing':
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.typing',
                'user_id': self.user.get('user_id'),
                'is_typing': data.get('is_typing', False),
            })
        elif event == 'message.read':
            message_id = data.get('message_id')
            await database_sync_to_async(MessageRepository.mark_read)(message_id)
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.read',
                'message_id': message_id,
                'reader_id': self.user.get('user_id'),
            })

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send_json({'type': 'message', 'message': event['message']})

    async def chat_typing(self, event):
        await self.send_json({'type': 'typing', 'user_id': event['user_id'], 'is_typing': event['is_typing']})

    async def chat_read(self, event):
        await self.send_json({'type': 'read', 'message_id': event['message_id'], 'reader_id': event['reader_id']})

    async def presence_update(self, event):
        await self.send_json({'type': 'presence', 'user_id': event['user_id'], 'online': event['online']})
