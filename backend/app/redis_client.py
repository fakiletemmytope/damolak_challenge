import redis.asyncio as redis

from app.config import redis_db, redis_host, redis_port

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=redis_db,
    decode_responses=True
)