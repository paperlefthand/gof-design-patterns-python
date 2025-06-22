from strategy.base import PaymentStrategy


class BitcoinPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid {amount:.2f} using Bitcoin.")
