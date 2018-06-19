from app.services.redis_connection import RedisConnection
from app.services.engine import DBEngine
from app.services.models import projects


view_access = ('VIEW', 'UPDATE', 'DELETE')
update_access = ('UPDATE', 'DELETE')
delete_access = 'DELETE'


async def get_id_by_token(request):
    token = request.headers.get('Authorization')
    connection = await RedisConnection.get_connection()
    return int(await connection.get(token))


async def set_delete_permissions(request):
    user_id = await get_id_by_token(request)
    acl = {
        user_id: delete_access
    }
    return acl


async def check_sharing_permissions(request):
    user_id = await get_id_by_token(request)
    acl = await get_acl(request.form.get('item_id'))
    if acl[str(user_id)] == delete_access:
        return True
    else:
        return False


async def give_access(item_id, user_id, permissions):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as connection:
        curr_acl = await get_acl(item_id)
        curr_acl[user_id] = permissions
        query = projects.update().where(projects.c.id == item_id).values(acl=curr_acl)
        await connection.execute(query)


async def get_acl(item_id):
    engine = await DBEngine.get_engine()
    async with engine.acquire() as connection:
        curr_entry = await connection.execute(projects.select(projects.c.id == item_id))
        curr = await curr_entry.fetchone()
        return curr['acl']


async def get_permissions(user_id, item_id):
    acl = await get_acl(item_id)
    try:
        return acl[str(user_id)]
    except KeyError:
        return False
