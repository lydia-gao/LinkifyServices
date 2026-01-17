import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import redis.asyncio as redis

from app.core.config import settings
from app.core.dependencies import decode_jwt_token
from app.utils.redis_client import build_ws_channel

router = APIRouter(tags=["realtime"])


@router.websocket("/ws/batch/{channel}")
async def websocket_batch_updates(websocket: WebSocket, channel: str):
    """Push batch-processing updates to authenticated clients."""
    raw_token = websocket.query_params.get("token")
    if not raw_token:
        await websocket.close(code=1008, reason="Missing token")
        return

    try:
        user = decode_jwt_token(raw_token)
        expected = build_ws_channel(user["id"])
        if channel != expected:
            await websocket.close(code=1008, reason="Channel mismatch")
            return
    except HTTPException:
        await websocket.close(code=1008, reason="Invalid token")
        return

    redis_channel = build_ws_channel(user.get("id"))
    await websocket.accept()

    redis_client = redis.from_url(settings.redis_url)
    pubsub = redis_client.pubsub()

    try:
        await pubsub.subscribe(redis_channel)
        print(
            f"WebSocket connected, subscribed to channel: {redis_channel} (redis_url={settings.redis_url})"
        )
        await websocket.send_json({"type": "ws_ready", "channel": redis_channel})

        # Send last cached event if present (handles late subscribers).
        last_key = f"ws:last:{user.get('id')}"
        last_payload = await redis_client.get(last_key)
        if last_payload:
            if isinstance(last_payload, bytes):
                last_payload = last_payload.decode("utf-8")
            try:
                parsed = json.loads(last_payload)
                print("Sending cached WebSocket event to client")
                await websocket.send_json(parsed)
            except (json.JSONDecodeError, TypeError):
                await websocket.send_text(last_payload)
            await redis_client.delete(last_key)

        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0,
            )
            if message and message.get("type") == "message":
                data = message.get("data")
                if isinstance(data, bytes):
                    data = data.decode("utf-8")

                print(f"Received message from Redis channel {redis_channel}: {str(data)[:200]}...")

                try:
                    parsed = json.loads(data)
                    print(f"Sending JSON message to WebSocket client: {parsed.get('type', 'unknown')}")
                    await websocket.send_json(parsed)
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Message is not valid JSON, sending as text. Error: {e}")
                    await websocket.send_text(data)

            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal error")
        except Exception:
            pass
    finally:
        try:
            await pubsub.unsubscribe(redis_channel)
            await pubsub.close()
        except Exception:
            pass
        try:
            await redis_client.close()
        except Exception:
            pass
