from strategy.base import PaymentStrategy


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount:.2f} using credit card.")
