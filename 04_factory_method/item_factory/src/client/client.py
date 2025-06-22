from typing import Any

import injector
from pydantic import ValidationError

from factories.furniture_factory import FurnitureFactory
from factories.toy_factory import ToyFactory


class Client:
    # DIコンテナ(Injector)経由でインスタンス化することで,
    # FurnitureFactoryインスタンスの生成ロジックはDIコンテナに隠蔽されるため,
    # __init__に書く必要がなくなる.
    @injector.inject
    def __init__(
        self,
        furniture_factory: FurnitureFactory,
        toy_factory: ToyFactory,
    ):
        self.furniture_factory = furniture_factory
        self.toy_factory = toy_factory

    def create_and_use(self, factory_type: str, item_type: str, **kwargs: Any):
        try:
            factory = {
                "furniture": self.furniture_factory,
                "toy": self.toy_factory,
            }.get(factory_type.lower())
            if not factory:
                raise ValueError(f"Unknown factory: {factory_type}")

            item = factory.create_item(item_type, **kwargs)
            print(f"Created: {item}")
            print(f"Use: {item.use()}\n")
        except (ValueError, ValidationError) as e:
            print(f"Error: {e}\n")
