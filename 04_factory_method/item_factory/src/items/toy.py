from items.base import Item
from pydantic import Field

class Car(Item):
    max_speed: int = Field(..., ge=0, description="最高速度 km/h")
    is_electric: bool = Field(False, description="電動かどうか")

    def use(self) -> str:
        mode = "electric" if self.is_electric else "gas-powered"
        return f"Driving the {mode} car at {self.max_speed} km/h."

class Doll(Item):
    age_range: str = Field(..., description="推奨年齢")
    material: str = Field(..., description="人形の材質")

    def use(self) -> str:
        return f"Playing with the {self.material} doll for ages {self.age_range}."
