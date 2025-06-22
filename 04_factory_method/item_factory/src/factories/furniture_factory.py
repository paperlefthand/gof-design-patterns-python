from typing import Any

from factories.base import ItemFactory
from items.furniture import Chair, Table


class FurnitureFactory(ItemFactory):
    def create_item(self, item_type: str, **kwargs: Any):
        mapping = {
            "chair": Chair,
            "table": Table,
        }
        cls = mapping.get(item_type.lower())
        if not cls:
            raise ValueError(f"Unknown furniture: {item_type}")
        return cls(**kwargs)
