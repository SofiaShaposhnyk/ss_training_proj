from app.services.engine import DBEngine, convert_resultproxy
from app.services.models import invoices


class Invoices(object):

    @staticmethod
    async def insert_invoice(project_id, description=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(invoices.insert().values(project_id=project_id,
                                                        description=description))

    @staticmethod
    async def delete_invoice(project_id, entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                delete_query = invoices.delete().where(invoices.c.id == int(entry_id) and
                                                       invoices.c.project_id == project_id)
            else:
                delete_query = invoices.delete().where(invoices.c.project_id == project_id)
            await conn.execute(delete_query)

    @staticmethod
    async def get_invoice(project_id, entry_id=None):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            if entry_id:
                get_query = invoices.select(invoices.c.id == entry_id and
                                            invoices.c.project_id == project_id)
            else:
                get_query = invoices.select(invoices.c.project_id == project_id)
            return await convert_resultproxy(await conn.execute(get_query))

    @staticmethod
    async def update_invoice(project_id, entry_id, **kwargs):
        engine = await DBEngine.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(invoices.update().where(
                invoices.c.project_id == project_id and
                invoices.c.id == entry_id).values(**kwargs))
