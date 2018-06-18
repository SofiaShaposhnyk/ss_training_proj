from app.services.engine import DBEngine, convert_resultproxy
from app.services.models import projects


class Projects(object):

    @staticmethod
    async def insert_project(user_id, create_date, acl):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(projects.insert().values(user_id=user_id,
                                                        create_date=create_date,
                                                        acl=acl))

    @staticmethod
    async def delete_project(entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                delete_query = projects.delete().where(projects.c.id == int(entry_id))
            else:
                delete_query = projects.delete()
            await conn.execute(delete_query)

    @staticmethod
    async def get_project(user_id, entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                get_query = projects.select(projects.c.id == entry_id and projects.c.acl[user_id].astext == 'VIEW')
            else:
                get_query = projects.select(projects.c.acl[user_id].astext == 'VIEW')
            result = await convert_resultproxy(await conn.execute(get_query))
            return result

    @staticmethod
    async def update_project(project_id, **kwargs):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(projects.update().where(
                projects.c.id == project_id).values(**kwargs))
