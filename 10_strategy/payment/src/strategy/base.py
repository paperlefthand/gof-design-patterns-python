from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """支払いアルゴリズムの共通インターフェース"""

    @abstractmethod
    def pay(self, amount: float) -> None: ...
