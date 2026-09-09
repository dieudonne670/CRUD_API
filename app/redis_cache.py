import json

import redis

from app.config import settings


# --------------------------------------------------
# Create Redis connection
# --------------------------------------------------

redis_cache = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1,
    decode_responses=True,
)


# --------------------------------------------------
# Cache lifetime (5 minutes)
# --------------------------------------------------

CACHE_EXPIRE = 300


# --------------------------------------------------
# Generate cache keys
# --------------------------------------------------

def make_key(prefix: str, *values):
    """
    Example:

    make_key("user", 5)

    user:5


    make_key("post", 17)

    post:17


    make_key("conversation", 5, 2)

    conversation:5:2
    """

    return f"{prefix}:{':'.join(map(str, values))}"


# --------------------------------------------------
# Save data into Redis
# --------------------------------------------------

def set_cache(
    key: str,
    value,
    expire: int = CACHE_EXPIRE,
):
    """
    Store Python data in Redis.

    Redis stores strings only.

    Therefore we convert
    Python dict/list

    →

    JSON string
    """

    redis_cache.set(
        key,
        json.dumps(value),
        ex=expire,
    )


# --------------------------------------------------
# Read data from Redis
# --------------------------------------------------

def get_cache(key: str):
    """
    Returns

    None
        if cache doesn't exist

    otherwise

    Python object
    """

    value = redis_cache.get(key)

    if value is None:
        return None

    return json.loads(value)


# --------------------------------------------------
# Delete cache
# --------------------------------------------------

def delete_cache(key: str):
    """
    Used whenever data changes.

    Example

    User updates profile

    delete user:5
    """

    redis_cache.delete(key)


# --------------------------------------------------
# Delete multiple keys
# --------------------------------------------------

def delete_pattern(pattern: str):
    """
    Deletes every key matching a pattern.

    Example

    notifications:*

    conversation:5:*

    post:*
    """

    keys = redis_cache.keys(pattern)

    if keys:
        redis_cache.delete(*keys)