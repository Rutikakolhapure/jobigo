import aioredis
import os
from django.conf import settings

class PresenceService:
    @staticmethod
    async def _get_redis():
        return await aioredis.from_url(settings.REDIS_URL)

    @staticmethod
    async def mark_online(user_id):
        if not user_id:
            return
        r = await PresenceService._get_redis()
        await r.sadd(settings.ONLINE_USERS_REDIS_KEY, str(user_id))

    @staticmethod
    async def mark_offline(user_id):
        if not user_id:
            return
        r = await PresenceService._get_redis()
        await r.srem(settings.ONLINE_USERS_REDIS_KEY, str(user_id))

    @staticmethod
    async def list_online():
        r = await PresenceService._get_redis()
        members = await r.smembers(settings.ONLINE_USERS_REDIS_KEY)
        return [m.decode() if isinstance(m, bytes) else str(m) for m in members]
