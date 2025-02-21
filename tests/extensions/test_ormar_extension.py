from enum import Enum
from typing import TYPE_CHECKING

import pytest

try:
    import sqlalchemy
    from databases import Database
    from ormar import DateTime, ForeignKey, Integer, Model, String
    from sqlalchemy import func

    from pydantic_factories.extensions import OrmarModelFactory
except ImportError:
    pytest.skip(allow_module_level=True)

postgres_dsn = "postgresql+asyncpg://pydantic-factories:pydantic-factories@postgres:5432/pydantic-factories"

database = Database(url=postgres_dsn, force_rollback=True)
metadata = sqlalchemy.MetaData()


if TYPE_CHECKING:
    from datetime import datetime


class BaseMeta:
    metadata = metadata
    database = database


class Mood(str, Enum):
    HAPPY = "happy"
    GRUMPY = "grumpy"


class Person(Model):
    id: int = Integer(autoincrement=True, primary_key=True)
    created_at: "datetime" = DateTime(timezone=True, server_default=func.now())
    updated_at: "datetime" = DateTime(timezone=True, server_default=func.now(), onupdate=func.now())
    mood: Mood = String(choices=Mood, max_length=20)

    class Meta(BaseMeta):
        pass


class Job(Model):
    id: int = Integer(autoincrement=True, primary_key=True)
    person: Person = ForeignKey(Person)
    name: str = String(max_length=20)

    class Meta(BaseMeta):
        pass


class PersonFactory(OrmarModelFactory):
    __model__ = Person


class JobFactory(OrmarModelFactory):
    __model__ = Job


def test_person_factory():
    result = PersonFactory.build()

    assert result.id
    assert result.created_at
    assert result.updated_at
    assert result.mood


def test_job_factory():
    job_name: str = "Unemployed"
    result = JobFactory.build(name=job_name)

    assert result.id
    assert result.name == job_name
    assert result.person
