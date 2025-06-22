from typing import Any

from factories.base import ItemFactory
from items.toy import Car, Doll


class ToyFactory(ItemFactory):
    def create_item(self, item_type: str, **kwargs: Any):
        mapping = {
            "car": Car,
            "doll": Doll,
        }
        cls = mapping.get(item_type.lower())
        if not cls:
            raise ValueError(f"Unknown toy: {item_type}")
        return cls(**kwargs)
