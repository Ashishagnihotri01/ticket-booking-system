import redis
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class RedisService:
    @staticmethod
    def acquire_lock(lock_name: str, acquire_timeout: int = 5, lock_timeout: int = 10) -> bool:
        """Acquires a distributed lock using Redis to safeguard transactional integrity."""
        return bool(redis_client.set(f"lock:{lock_name}", "locked", nx=True, ex=lock_timeout))

    @staticmethod
    def release_lock(lock_name: str):
        redis_client.delete(f"lock:{lock_name}")

    @staticmethod
    def set_seat_hold(show_id: int, seat_id: int, user_id: int, ttl: int):
        key = f"hold:show:{show_id}:seat:{seat_id}"
        redis_client.set(key, user_id, ex=ttl)

    @staticmethod
    def remove_seat_hold(show_id: int, seat_id: int):
        key = f"hold:show:{show_id}:seat:{seat_id}"
        redis_client.delete(key)