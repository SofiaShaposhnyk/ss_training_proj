from app.services.redis_connection import RedisConnection
from app.services.engine import DBEngine
from app.services.models import projects


async def get_id_by_token(request):
    token = request.headers.get('Authorization')
    connection = await RedisConnection.get_connection()
    return int(await connection.get(token))


async def set_delete_permissions(request):
    user_id = await get_id_by_token(request)
    acl = {
        user_id: ["DELETE"]
    }
    return acl


async def give_access(item_id, user_id, permissions):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as connection:
        acl = {
            user_id: permissions
        }
        query = projects.update().where(projects.c.id == item_id).values(projects.c.acl == acl)
        await connection.execute(query)
