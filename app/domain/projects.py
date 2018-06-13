from app.database import DBEngine, convert_resultproxy
from app.services.models import projects


class Projects(object):

    @staticmethod
    async def insert(user_id, create_date):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(projects.insert().values(user_id=user_id,
                                                        create_date=create_date))

    @staticmethod
    async def delete(entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                delete_query = projects.delete().where(projects.c.id == int(entry_id))
            else:
                delete_query = projects.delete()
            await conn.execute(delete_query)

    @staticmethod
    async def get(entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                get_query = projects.select(projects.c.id == entry_id)
            else:
                get_query = projects.select()
            return convert_resultproxy(await conn.execute(get_query))

    @staticmethod
    async def update(project_id, **kwargs):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(projects.update().where(
                projects.c.id == project_id).values(**kwargs))
