from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        raise NotImplementedError


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using credit card.")


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using PayPal.")


class BitcoinPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using Bitcoin.")
