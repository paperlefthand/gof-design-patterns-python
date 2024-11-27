from pydantic import BaseModel, model_validator
from typing import Any
from payment.payments import PaymentStrategy


class Item(BaseModel):
    name: str
    price: int


class ShoppingCart(BaseModel):
    payment_strategy: Any
    items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def calculate_total(self) -> int:
        total = sum(item.price for item in self.items)
        return total

    def checkout(self) -> None:
        total = self.calculate_total()
        self.payment_strategy.pay(total)

    @model_validator(mode="before")
    def validate_payment_strategy(cls, values):
        strategy = values.get("payment_strategy")
        if not isinstance(strategy, PaymentStrategy):
            raise ValueError("payment_strategy must be an instance of PaymentStrategy.")
        return values
