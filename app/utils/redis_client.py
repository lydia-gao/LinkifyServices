import json
import logging
from functools import lru_cache
from typing import Any, Union

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

@lru_cache
def get_redis_client() -> redis.Redis:
    """Return a singleton Redis client configured from settings."""
    return redis.from_url(settings.redis_url)


def build_ws_channel(user_id: Union[str, int]) -> str:
    return f"ws:user:{user_id}"


def publish_ws_event(user_id: Union[str, int], event: dict[str, Any]) -> str:
    """Publish a structured event for a user websocket channel."""
    channel = build_ws_channel(user_id)
    payload = json.dumps(event, ensure_ascii=False)
    client = get_redis_client()
    client.publish(channel, payload)
    # Store last event briefly to allow late websocket subscribers to catch up.
    client.setex(f"ws:last:{user_id}", 300, payload)
    logger.info(
        "publish_ws_event redis_url=%s channel=%s payload_len=%s",
        settings.redis_url,
        channel,
        len(payload),
    )
    return channel
