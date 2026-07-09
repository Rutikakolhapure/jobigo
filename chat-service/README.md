# Chat Service for JobiGo

This service provides WebSocket-based real-time chat functionality for the JobiGo platform.

Features
- Django + Django Channels (ASGI)
- Redis channel layer and presence via Redis
- One-to-one chat rooms
- Typing indicators
- Read receipts
- Message history REST API
- JWT-based authentication (verifies tokens issued by auth-service via shared secret or public key)

Environment variables are defined in `.env.example`.

See README for setup and development instructions.
