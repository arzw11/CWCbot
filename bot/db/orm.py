from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.engine import engine
from bot.db.models import Base, Projects, Colors, Materials, Underframe, Utils


class AsyncOrm:
    @staticmethod
    async def create_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_project(session: AsyncSession, data: dict):
        project = Projects(
            name=data['name'],
            material=data['material'],
            cover=data['cover'],
            color=data['color'],
            image=data['image'],
        )
        session.add(project)
        await session.commit()

    @staticmethod
    async def delete_project(session: AsyncSession, project_id: int):
        query = delete(Projects).where(Projects.id == project_id)
        await session.execute(query)
        await session.commit()

    @staticmethod   
    async def change_project(session: AsyncSession, project_id: int, data: dict):
        query = update(Projects).where(Projects.id == project_id).values(
            name=data['name'],
            material=data['material'],
            cover=data['cover'],
            color=data['color'],
            image=data['image'],
        )
        await session.execute(query)
        await session.commit()
    
    @staticmethod
    async def get_project(session: AsyncSession, project_id: int):
        query = select(Projects).where(Projects.id == project_id)
        result = await session.execute(query)

        return result.scalar()

    @staticmethod
    async def get_all_projects(session: AsyncSession):
        query = select(Projects)
        result = await session.execute(query)

        return result.scalars().all()
    
    @staticmethod
    async def add_color(session: AsyncSession, data: dict):
        color = Colors(
            image=data['image'],
        )
        session.add(color)
        await session.commit()

    @staticmethod
    async def delete_color(session: AsyncSession, color_id: int):
        query = delete(Colors).where(Colors.id == color_id)
        await session.execute(query)
        await session.commit()

    @staticmethod   
    async def change_color(session: AsyncSession, color_id: int, data: dict):
        query = update(Colors).where(Colors.id == color_id).values(
            image=data['image'],
        )
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def get_color(session: AsyncSession, color_id: int):
        query = select(Colors).where(Colors.id == color_id)
        result = await session.execute(query)

        return result.scalar()

    @staticmethod
    async def get_all_colors(session: AsyncSession):
        query = select(Colors)
        result = await session.execute(query)

        return result.scalars().all()
    

    @staticmethod
    async def get_material(session: AsyncSession, material_id: int):
        query = select(Materials).where(Materials.id == material_id)
        result = await session.execute(query)

        return result.scalar()
    
    @staticmethod
    async def get_all_materials(session: AsyncSession):
        query = select(Materials)
        result = await session.execute(query)

        return result.scalars().all()
    
    @staticmethod   
    async def change_material_price(session: AsyncSession, data: dict):
        query = update(Materials).where(Materials.id == data['id']).values(
            price=data['price'],
            
        )
        await session.execute(query)
        await session.commit()
    
    @staticmethod
    async def add_underframe(session: AsyncSession, data: dict):
        underframe = Underframe(
            name=data['name'],
            price=data['price'],
        )
        session.add(underframe)
        await session.commit()

    @staticmethod
    async def delete_underframe(session: AsyncSession, underframe_id: int):
        query = delete(Underframe).where(Underframe.id == underframe_id)
        await session.execute(query)
        await session.commit()

    @staticmethod   
    async def change_underframe(session: AsyncSession, underframe_id: int, data: dict):
        query = update(Underframe).where(Underframe.id == underframe_id).values(
            name=data['name'],
            price=data['price'],
        )
        await session.execute(query)
        await session.commit()
    
    @staticmethod
    async def get_underframe(session: AsyncSession, underframe_id: int):
        query = select(Underframe).where(Underframe.id == underframe_id)
        result = await session.execute(query)

        return result.scalar()

    @staticmethod
    async def get_all_underframes(session: AsyncSession):
        query = select(Underframe)
        result = await session.execute(query)

        return result.scalars().all()

    @staticmethod
    async def add_utils(session:AsyncSession, data: dict):
        util = Utils(
            name=data['name'],
            image=data['image'],
        )
        session.add(util)
        await session.commit()

    @staticmethod
    async def get_util(session: AsyncSession, util_id: int):
        query = select(Utils).where(Utils.id == util_id)
        result = await session.execute(query)

        return result.scalar()

    @staticmethod
    async def get_all_utils(session: AsyncSession):
        query = select(Utils)
        result = await session.execute(query)

        return result.scalars().all()
    
    @staticmethod   
    async def change_util(session: AsyncSession, util_id: int, data: dict):
        query = update(Utils).where(Utils.id == util_id).values(
            image=data['image'],
        )
        await session.execute(query)
        await session.commit()