from django.urls import path
from apps.chat import consumers

websocket_urlpatterns = [
    # client connects to ws://.../ws/chat/<room_name>/?token=JWT
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
