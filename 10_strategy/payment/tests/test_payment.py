import pytest

from models import Item, ShoppingCart
from strategy.bitcoin import BitcoinPayment
from strategy.credit_card import CreditCardPayment
from strategy.paypal import PayPalPayment


def test_credit_card_payment(capfd):
    cart = ShoppingCart(payment_strategy=CreditCardPayment())
    book = Item(name="Book", price=10.0)
    pen = Item(name="Pen", price=2.0)
    cart.add_item(book)
    cart.add_item(pen)
    cart.checkout()
    out, err = capfd.readouterr()
    assert "Paid 12.00 using credit card." in out


def test_total_calculation():
    cart = ShoppingCart(payment_strategy=CreditCardPayment())
    cart.add_item(Item(name="Book", price=12.5))
    cart.add_item(Item(name="Pen", price=2.5))
    assert cart.calculate_total() == 15.0


def test_strategy_switching(capsys):
    cart = ShoppingCart(payment_strategy=PayPalPayment())
    cart.add_item(Item(name="Game", price=60))
    cart.checkout()

    captured = capsys.readouterr()
    assert "Paid 60.00 using PayPal." in captured.out


@pytest.mark.parametrize(
    "strategy_cls, payment_methods",
    [(CreditCardPayment, "credit card"), (PayPalPayment, "PayPal"), (BitcoinPayment, "Bitcoin")],
)
def test_each_strategy(strategy_cls, payment_methods, capsys):
    cart = ShoppingCart(payment_strategy=strategy_cls())
    cart.add_item(Item(name="Subscription", price=9.99))
    cart.checkout()
    out = capsys.readouterr().out
    assert f"Paid 9.99 using {payment_methods}." in out
