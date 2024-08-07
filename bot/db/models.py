from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    ...

class Projects(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    material: Mapped[str] = mapped_column(String(150), nullable=False)
    cover: Mapped[str] = mapped_column(String(150), nullable=False)
    color: Mapped[str] = mapped_column(String(150), nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)

class Colors(Base):
    __tablename__ = 'colors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    image: Mapped[str] = mapped_column(String(150), nullable=False)

class Materials(Base):
    __tablename__ = 'materials'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(String(150), nullable=False)

class Underframe(Base):
    __tablename__ = 'underframe'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

class Utils(Base):
    __tablename__ = 'utils'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)