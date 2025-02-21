from typing import Any

import pytest
from pydantic import BaseModel

from pydantic_factories import (
    AsyncPersistenceProtocol,
    ModelFactory,
    SyncPersistenceProtocol,
)


class MyModel(BaseModel):
    name: str


class MySyncPersistenceHandler(SyncPersistenceProtocol):
    def save(self, data: Any, *args, **kwargs) -> Any:
        return data

    def save_many(self, data: Any, *args, **kwargs) -> Any:
        return data


class MyAsyncPersistenceHandler(AsyncPersistenceProtocol):
    async def save(self, data: Any, *args, **kwargs) -> Any:
        return data

    async def save_many(self, data: Any, *args, **kwargs) -> Any:
        return data


def test_sync_persistence_handler_is_set_and_called_with_instance():
    class MyFactory(ModelFactory):
        __model__ = MyModel
        __sync_persistence__ = MySyncPersistenceHandler()

    assert MyFactory.create_sync().name
    assert [instance.name for instance in MyFactory.create_batch_sync(size=2)]


def test_sync_persistence_handler_is_set_and_called_with_class():
    class MyFactory(ModelFactory):
        __model__ = MyModel
        __sync_persistence__ = MySyncPersistenceHandler

    assert MyFactory.create_sync().name
    assert [instance.name for instance in MyFactory.create_batch_sync(size=2)]


@pytest.mark.asyncio()
async def test_async_persistence_handler_is_set_and_called_with_instance():
    class MyFactory(ModelFactory):
        __model__ = MyModel
        __async_persistence__ = MyAsyncPersistenceHandler()

    assert (await MyFactory.create_async()).name
    assert [instance.name for instance in (await MyFactory.create_batch_async(size=2))]


@pytest.mark.asyncio()
async def test_async_persistence_handler_is_set_and_called_with_class():
    class MyFactory(ModelFactory):
        __model__ = MyModel
        __async_persistence__ = MyAsyncPersistenceHandler

    assert (await MyFactory.create_async()).name
    assert [instance.name for instance in (await MyFactory.create_batch_async(size=2))]
