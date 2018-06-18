import asyncio_redis
from app.config import redis


class RedisConnection(object):

    __connection = None

    @classmethod
    async def get_connection(cls):
        if not cls.__connection:
            cls.__connection = await asyncio_redis.Connection.create(host=redis['redis_host'],
                                                                     port=redis['redis_port'])
        return cls.__connection
