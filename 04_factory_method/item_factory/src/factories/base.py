from abc import ABC, abstractmethod
from typing import Any
from items.base import Item


class ItemFactory(ABC):
    @abstractmethod
    def create_item(self, item_type: str, **kwargs: Any) -> Item:
        pass
