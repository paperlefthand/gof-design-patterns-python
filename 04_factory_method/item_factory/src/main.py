import injector

from client.client import Client
from factories.furniture_factory import FurnitureFactory
from factories.toy_factory import ToyFactory


class FactoryModule(injector.Module):
    """Module to configure dependency injection for factories."""

    def configure(self, binder: injector.Binder):
        """Bind factories to their implementations with singleton scope."""
        # NOTE singleton scope ensures only one instance of each factory is created
        binder.bind(
            interface=FurnitureFactory, to=FurnitureFactory, scope=injector.singleton
        )
        binder.bind(interface=ToyFactory, to=ToyFactory, scope=injector.singleton)


if __name__ == "__main__":
    # Create an injector instance with the factory module
    # This will allow us to inject dependencies into the Client class
    inj = injector.Injector([FactoryModule()])
    # clientインスタンスの生成をDIコンテナに任せる.
    # InjectorはClientクラスのコンストラクタに必要な依存関係を自動的に解決する.
    # (FactoryModuleで定義されたFurnitureFactoryとToyFactoryのシングルトンインスタンスが自動的に注入される.)
    client = inj.get(Client)

    client.create_and_use(
        factory_type="furniture",
        item_type="chair",
        name="Comfort Chair",
        price=14900,
        material="leather",
        has_armrests=True,
    )
    client.create_and_use(
        factory_type="toy",
        item_type="car",
        name="Speedster",
        price=4900,
        max_speed=120,
        is_electric=True,
    )
