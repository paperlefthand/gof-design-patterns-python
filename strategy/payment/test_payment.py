from payment.cart import Item, ShoppingCart
from payment.payments import CreditCardPayment


def test_credit_card_payment(capfd):
    cart = ShoppingCart(payment_strategy=CreditCardPayment())
    book = Item(name="Book", price=10)
    pen = Item(name="Pen", price=2)
    cart.add_item(book)
    cart.add_item(pen)
    cart.checkout()
    out, err = capfd.readouterr()
    assert "Paid 12 using credit card." in out
