from collections import Counter, deque  # noqa: TC003
from datetime import date, datetime, time, timedelta
from decimal import Decimal  # noqa: TC003
from enum import Enum
from ipaddress import (  # noqa: TC003
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path  # noqa: TC003
from typing import Callable
from uuid import UUID  # noqa: TC003

import pytest
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    AmqpDsn,
    AnyHttpUrl,
    AnyUrl,
    BaseConfig,
    BaseModel,
    ByteSize,
    DirectoryPath,
    EmailStr,
    Field,
    FilePath,
    FutureDate,
    HttpUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    Json,
    KafkaDsn,
    NameEmail,
    NegativeFloat,
    NegativeInt,
    NonNegativeInt,
    NonPositiveFloat,
    PastDate,
    PaymentCardNumber,
    PositiveFloat,
    PositiveInt,
    PostgresDsn,
    PyObject,
    RedisDsn,
    SecretBytes,
    SecretStr,
    StrictBool,
    StrictBytes,
    StrictFloat,
    StrictInt,
    StrictStr,
)
from pydantic.color import Color  # noqa: TC002
from typing_extensions import Literal

from pydantic_factories import ModelFactory
from pydantic_factories.exceptions import ParameterError
from tests.models import Person, PersonFactoryWithDefaults, Pet


def test_enum_parsing():
    class MyStrEnum(str, Enum):
        FIRST_NAME = "Moishe Zuchmir"
        SECOND_NAME = "Hannah Arendt"

    class MyIntEnum(Enum):
        ONE_HUNDRED = 100
        TWO_HUNDRED = 200

    class MyModel(BaseModel):
        name: MyStrEnum
        worth: MyIntEnum

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()

    assert isinstance(result.name, MyStrEnum)
    assert isinstance(result.worth, MyIntEnum)


def test_callback_parsing():
    today = date.today()

    class MyModel(BaseModel):
        name: str
        birthday: date
        secret: Callable

    class MyFactory(ModelFactory):
        __model__ = MyModel

        name = lambda: "moishe zuchmir"  # noqa: E731
        birthday = lambda: today  # noqa: E731

    result = MyFactory.build()

    assert result.name == "moishe zuchmir"
    assert result.birthday == today
    assert callable(result.secret)


def test_alias_parsing():
    class MyModel(BaseModel):
        aliased_field: str = Field(alias="special_field")

    class MyFactory(ModelFactory):
        __model__ = MyModel

    assert isinstance(MyFactory.build().aliased_field, str)


def test_literal_parsing():
    class MyModel(BaseModel):
        literal_field: "Literal['yoyos']"
        multi_literal_field: "Literal['nolos', 'zozos', 'kokos']"

    class MyFactory(ModelFactory):
        __model__ = MyModel

    assert MyFactory.build().literal_field == "yoyos"
    batch = MyFactory.batch(30)
    values = {v.multi_literal_field for v in batch}
    assert values == {"nolos", "zozos", "kokos"}


def test_embedded_models_parsing():
    class MyModel(BaseModel):
        pet: Pet

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()
    assert isinstance(result.pet, Pet)


def test_embedded_factories_parsing():
    class MyModel(BaseModel):
        person: Person

    class MyFactory(ModelFactory):
        __model__ = MyModel
        person = PersonFactoryWithDefaults

    result = MyFactory.build()
    assert isinstance(result.person, Person)


def test_type_property_parsing():
    class MyModel(BaseModel):
        object_field: object
        float_field: float
        int_field: int
        bool_field: bool
        str_field: str
        bytes_field: bytes
        # built-in objects
        dict_field: dict
        tuple_field: tuple
        list_field: list
        set_field: set
        frozenset_field: frozenset
        deque_field: deque
        # standard library objects
        Path_field: Path
        Decimal_field: Decimal
        UUID_field: UUID
        # datetime
        datetime_field: datetime
        date_field: date
        time_field: time
        timedelta_field: timedelta
        # ip addresses
        IPv4Address_field: IPv4Address
        IPv4Interface_field: IPv4Interface
        IPv4Network_field: IPv4Network
        IPv6Address_field: IPv6Address
        IPv6Interface_field: IPv6Interface
        IPv6Network_field: IPv6Network
        # types
        Callable_field: Callable
        # pydantic specific
        ByteSize_pydantic_type: ByteSize
        PositiveInt_pydantic_type: PositiveInt
        FilePath_pydantic_type: FilePath
        NegativeFloat_pydantic_type: NegativeFloat
        NegativeInt_pydantic_type: NegativeInt
        PositiveFloat_pydantic_type: PositiveFloat
        NonPositiveFloat_pydantic_type: NonPositiveFloat
        NonNegativeInt_pydantic_type: NonNegativeInt
        StrictInt_pydantic_type: StrictInt
        StrictBool_pydantic_type: StrictBool
        StrictBytes_pydantic_type: StrictBytes
        StrictFloat_pydantic_type: StrictFloat
        StrictStr_pydantic_type: StrictStr
        DirectoryPath_pydantic_type: DirectoryPath
        EmailStr_pydantic_type: EmailStr
        NameEmail_pydantic_type: NameEmail
        PyObject_pydantic_type: PyObject
        Color_pydantic_type: Color
        Json_pydantic_type: Json
        PaymentCardNumber_pydantic_type: PaymentCardNumber
        AnyUrl_pydantic_type: AnyUrl
        AnyHttpUrl_pydantic_type: AnyHttpUrl
        HttpUrl_pydantic_type: HttpUrl
        PostgresDsn_pydantic_type: PostgresDsn
        RedisDsn_pydantic_type: RedisDsn
        UUID1_pydantic_type: UUID1
        UUID3_pydantic_type: UUID3
        UUID4_pydantic_type: UUID4
        UUID5_pydantic_type: UUID5
        SecretBytes_pydantic_type: SecretBytes
        SecretStr_pydantic_type: SecretStr
        IPvAnyAddress_pydantic_type: IPvAnyAddress
        IPvAnyInterface_pydantic_type: IPvAnyInterface
        IPvAnyNetwork_pydantic_type: IPvAnyNetwork
        AmqpDsn_pydantic_type: AmqpDsn
        KafkaDsn_pydantic_type: KafkaDsn
        PastDate_pydantic_type: PastDate
        FutureDate_pydantic_type: FutureDate
        Counter_pydantic_type: Counter

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()

    for key in MyFactory.get_provider_map().keys():
        key_name = key.__name__ if hasattr(key, "__name__") else key._name
        if hasattr(result, f"{key_name}_field"):
            assert isinstance(getattr(result, f"{key_name}_field"), key)
        elif hasattr(result, f"{key_name}_pydantic_type"):
            assert getattr(result, f"{key_name}_pydantic_type") is not None


def test_class_parsing():
    class TestClassWithoutKwargs:
        def __init__(self):
            self.flag = "123"

    class MyModel(BaseModel):
        class Config(BaseConfig):
            arbitrary_types_allowed = True

        class_field: TestClassWithoutKwargs
        # just a few select exceptions, to verify this works
        exception_field: Exception
        type_error_field: TypeError
        attribute_error_field: AttributeError
        runtime_error_field: RuntimeError

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()

    assert isinstance(result.class_field, TestClassWithoutKwargs)
    assert result.class_field.flag == "123"
    assert isinstance(result.exception_field, Exception)
    assert isinstance(result.type_error_field, TypeError)
    assert isinstance(result.attribute_error_field, AttributeError)
    assert isinstance(result.runtime_error_field, RuntimeError)

    class TestClassWithKwargs:
        def __init__(self, flag: str):
            self.flag = str

    class MyModel(BaseModel):
        class Config(BaseConfig):
            arbitrary_types_allowed = True

        class_field: TestClassWithKwargs

    class MySecondFactory(ModelFactory):
        __model__ = MyModel

    with pytest.raises(ParameterError):
        MySecondFactory.build()
