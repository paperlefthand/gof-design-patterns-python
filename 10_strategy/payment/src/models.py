from typing import List

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat

from strategy.base import PaymentStrategy


class Item(BaseModel):
    name: str = Field(..., min_length=1)
    price: PositiveFloat


class ShoppingCart(BaseModel):
    payment_strategy: PaymentStrategy
    items: List[Item] = []

    # BaseModelを継承していないPaymentStrategyを"任意の型"として許容
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- ビジネスロジック ---

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)

    def checkout(self) -> None:
        total = self.calculate_total()
        self.payment_strategy.pay(total)

    # @model_validator(mode="before")
    # def _validate_payment_strategy(cls, values):
    #     strategy = values.get("payment_strategy")
    #     if not isinstance(strategy, PaymentStrategy):
    #         raise TypeError("payment_strategy must implement PaymentStrategy")
    #     return values
