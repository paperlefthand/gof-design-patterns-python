from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class Item(BaseModel, ABC):
    """アイテムの基本クラス"""

    name: str = Field(..., description="アイテムの名前")
    price: int = Field(..., gt=0, description="アイテムの価格")

    @abstractmethod
    def use(self) -> str:
        pass
