import re
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

DB_DSN = "postgresql+asyncpg://admin:123456@localhost:5432/db_example"


def camelcase_to_snakecase(value):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', value).lower()


class ExampleCreateSchema(BaseModel):
    id: int
    desc: str

    class Config:
        orm_mode = True


class ExampleCreateSchemaResponse(BaseModel):
    id: int
    desc: str

    class Config:
        orm_mode = True


@as_declarative()
class BaseModelExample:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camelcase_to_snakecase(cls.__name__)


class ExampleModel(BaseModelExample):
    id = Column(Integer, primary_key=True)
    desc = Column(String)


def get_engine():
    return create_async_engine(
        DB_DSN,
        echo=True,
    )


def get_session():
    DBSession = sessionmaker(class_=AsyncSession)
    DBSession.configure(binds={
        ExampleModel: get_engine(),
    })
    return DBSession()


class ExampleDAO:

    def __init__(self):
        self.model = ExampleModel

    def obj_in_to_db_obj(self, obj_in: Any):
        obj_in_data = jsonable_encoder(obj_in)
        user_id = obj_in_data.pop("id")
        return self.model(**obj_in_data, id=user_id)

    async def create(self, obj_in: ExampleCreateSchema):
        try:
            data_db = self.obj_in_to_db_obj(obj_in=obj_in)
            async with get_session() as db:
                db.add(data_db)
                await db.commit()
                response = ExampleCreateSchemaResponse.from_orm(data_db)

            return response
        except Exception as e:
            raise e
