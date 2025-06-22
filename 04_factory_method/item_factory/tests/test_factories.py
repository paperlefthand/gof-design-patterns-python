import pytest
from pydantic import ValidationError

from factories.furniture_factory import FurnitureFactory
from factories.toy_factory import ToyFactory
from items.furniture import Chair, Table
from items.toy import Car, Doll


@pytest.fixture
def furniture_factory():
    return FurnitureFactory()


@pytest.fixture
def toy_factory():
    return ToyFactory()


@pytest.mark.parametrize(
    "kwargs, expected_type",
    [
        (
            {"name": "C1", "price": 100, "material": "wood", "has_armrests": False},
            Chair,
        ),
        ({"name": "T1", "price": 200, "shape": "circle", "capacity": 4}, Table),
    ],
)
def test_furniture_factory_creates_valid_items(
    furniture_factory, kwargs, expected_type
):
    item = furniture_factory.create_item(expected_type.__name__.lower(), **kwargs)
    assert isinstance(item, expected_type)
    # pydantic のモデルとして整合性が取れていること
    assert item.name == kwargs["name"]
    assert item.price == kwargs["price"]


def test_furniture_factory_unknown_type(furniture_factory):
    with pytest.raises(ValueError) as ei:
        furniture_factory.create_item(
            "sofa", name="S", price=50, material="fabric", has_armrests=True
        )
    assert "Unknown furniture" in str(ei.value)


@pytest.mark.parametrize(
    "kwargs, expected_type",
    [
        ({"name": "Car1", "price": 50, "max_speed": 80, "is_electric": True}, Car),
        ({"name": "D1", "price": 30, "age_range": "3-5", "material": "plastic"}, Doll),
    ],
)
def test_toy_factory_creates_valid_items(toy_factory, kwargs, expected_type):
    item = toy_factory.create_item(expected_type.__name__.lower(), **kwargs)
    assert isinstance(item, expected_type)
    assert item.price == kwargs["price"]


def test_toy_factory_unknown_type(toy_factory):
    with pytest.raises(ValueError) as ei:
        toy_factory.create_item(
            "robot", name="R", price=100, max_speed=10, is_electric=False
        )
    assert "Unknown toy" in str(ei.value)


def test_validation_error_on_negative_price(furniture_factory):
    with pytest.raises(ValidationError) as ei:
        furniture_factory.create_item(
            "chair", name="C2", price=-1, material="metal", has_armrests=True
        )
    assert "Input should be greater than 0" in str(ei.value)
