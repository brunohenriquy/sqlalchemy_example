import asyncio

from sqlalchemy_example import ExampleDAO, ExampleCreateSchema


async def run_exemple():
    exemple_item = ExampleCreateSchema(
        id=1,
        desc="test"
    )

    user_favorite_event = ExampleDAO()
    result = await user_favorite_event.create(obj_in=exemple_item)


asyncio.run(run_exemple())
