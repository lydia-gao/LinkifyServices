from typing import Optional, Any
import json
from app.utils.redis_client import get_redis_client


_redis = get_redis_client()


def cache_set_bytes(key: str, data: bytes, ttl_seconds: Optional[int] = 300) -> None:
    _redis.set(name=key, value=data, ex=ttl_seconds)


def cache_get_bytes(key: str) -> Optional[bytes]:
    val = _redis.get(name=key)
    return val if isinstance(val, (bytes, bytearray)) else None


# New helpers: cache S3 image URLs (strings) instead of storing raw image bytes.
# Use these where you previously cached raw image bytes. TTL default set longer
# because S3 objects are durable (one hour = 3600s by default).
def cache_set_s3_url(key: str, s3_url: str, ttl_seconds: Optional[int] = 3600) -> None:
    """Store an S3 URL (string) under `key` with an optional TTL."""
    _redis.set(name=key, value=s3_url, ex=ttl_seconds)


def cache_get_s3_url(key: str) -> Optional[str]:
    """Return the cached S3 URL string for `key`, or None if not found."""
    val = _redis.get(name=key)
    if not val:
        return None
    if isinstance(val, (bytes, bytearray)):
        return val.decode("utf-8")
    if isinstance(val, str):
        return val
    return None


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
