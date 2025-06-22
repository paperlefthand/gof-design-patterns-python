from strategy.base import PaymentStrategy


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount:.2f} using PayPal.")
