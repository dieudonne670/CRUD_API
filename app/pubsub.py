import asyncio
import json

from app.redis import redis_client
from app.websocket_manager import manager


async def publish_message(channel: str, data: dict):
    """
    Publish an event to a Redis channel.
    """
    await redis_client.publish(
        channel,
        json.dumps(data),
    )


async def redis_listener():
    """
    Listen for Redis Pub/Sub events forever.
    """

    pubsub = redis_client.pubsub()

    await pubsub.subscribe(
        "messages",
        "notifications",
    )

    while True:

        message = await pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            payload = json.loads(
                message["data"]
            )

            receiver = payload["receiver"]

            await manager.send_personal_message(
                receiver,
                payload,
            )

        await asyncio.sleep(0.01)