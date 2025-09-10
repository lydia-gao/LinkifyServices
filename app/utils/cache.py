from typing import Optional, Any
import json
import redis
from app.core.config import settings


_redis = redis.from_url(settings.redis_url)


def cache_set_bytes(key: str, data: bytes, ttl_seconds: Optional[int] = 300) -> None:
    _redis.set(name=key, value=data, ex=ttl_seconds)


def cache_get_bytes(key: str) -> Optional[bytes]:
    val = _redis.get(name=key)
    return val if isinstance(val, (bytes, bytearray)) else None


def cache_set_json(key: str, obj: Any, ttl_seconds: Optional[int] = 300) -> None:
    _redis.set(name=key, value=json.dumps(obj, ensure_ascii=False), ex=ttl_seconds)


def cache_get_json(key: str) -> Optional[Any]:
    val = _redis.get(name=key)
    if not val:
        return None
    if isinstance(val, (bytes, bytearray)):
        return json.loads(val.decode("utf-8"))
    if isinstance(val, str):
        return json.loads(val)
    return None
