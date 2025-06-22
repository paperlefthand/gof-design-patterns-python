from items.base import Item

from pydantic import Field


class Chair(Item):
    material: str = Field(..., description="椅子の材質")
    has_armrests: bool = Field(False, description="肘掛けの有無")

    def use(self) -> str:
        return f"Sitting on the {self.material} chair."


class Table(Item):
    shape: str = Field(..., description="テーブルの形状")
    capacity: int = Field(..., ge=1, description="人数")

    def use(self) -> str:
        return f"Dining at the {self.shape} table for {self.capacity} people."
