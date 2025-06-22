import injector
import pytest

from client.client import Client
from factories.furniture_factory import FurnitureFactory
from factories.toy_factory import ToyFactory


class FactoryModule(injector.Module):
    def configure(self, binder: injector.Binder):
        binder.bind(
            interface=FurnitureFactory, to=FurnitureFactory, scope=injector.singleton
        )
        binder.bind(interface=ToyFactory, to=ToyFactory, scope=injector.singleton)


@pytest.fixture
def injector_instance() -> injector.Injector:
    return injector.Injector([FactoryModule()])


@pytest.fixture
def client(injector_instance) -> Client:
    return injector_instance.get(Client)
