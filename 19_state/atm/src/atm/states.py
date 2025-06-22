from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from atm.exceptions import InvalidOperation, MaintenanceMode

# 型チェック時のみimportすることで循環参照を防ぐ
if TYPE_CHECKING:
    from atm.context import ATM


class ATMState(ABC):
    """すべての状態が持つインタフェース"""

    @abstractmethod
    def insert_card(self, atm: "ATM") -> None: ...
    @abstractmethod
    def eject_card(self, atm: "ATM") -> None: ...
    @abstractmethod
    def enter_pin(self, atm: "ATM", pin: str) -> None: ...
    @abstractmethod
    def withdraw_money(self, atm: "ATM", amount: int) -> None: ...
    @abstractmethod
    def check_balance(self, atm: "ATM") -> int: ...


class NoCard(ATMState):
    def insert_card(self, atm: "ATM"):
        atm.set_state(HasCard())

    def eject_card(self, atm: "ATM"):
        raise InvalidOperation("カードが挿入されていません。")

    def enter_pin(self, atm: "ATM", pin: str):
        raise InvalidOperation("カードを挿入してください。")

    def withdraw_money(self, atm: "ATM", amount: int):
        raise InvalidOperation("カードを挿入してください。")

    def check_balance(
        self,
        atm: "ATM",
    ):
        raise InvalidOperation("カードを挿入してください。")


class HasCard(ATMState):
    def insert_card(self, atm: "ATM"):
        raise InvalidOperation("すでにカードが挿入済みです。")

    def eject_card(self, atm: "ATM"):
        atm.set_state(NoCard())

    def enter_pin(self, atm: "ATM", pin: str):
        if pin == atm.correct_pin:
            atm.set_state(Authenticated())
        else:
            atm.set_state(NoCard())
            raise InvalidOperation("PIN が誤っています。カードを取り出しました。")

    def withdraw_money(self, atm: "ATM", amount: int):
        raise InvalidOperation("PIN を入力してください。")

    def check_balance(self, atm: "ATM"):
        raise InvalidOperation("PIN を入力してください。")


class Authenticated(ATMState):
    def insert_card(self, atm: "ATM"):
        raise InvalidOperation("操作中です。新しいカードは挿入不可。")

    def eject_card(self, atm: "ATM"):
        atm.set_state(NoCard())

    def enter_pin(self, atm: "ATM", pin: str):
        raise InvalidOperation("すでに認証済みです。")

    def withdraw_money(self, atm: "ATM", amount: int):
        atm.account.withdraw(amount)
        atm.set_state(NoCard())

    def check_balance(self, atm: "ATM"):
        return atm.account.balance


class Maintenance(ATMState):
    """メンテナンス中はすべての顧客操作をブロック"""

    def __init__(self):
        self.message = "現在メンテナンス中です。"

    def insert_card(self, atm: "ATM"):
        raise MaintenanceMode(self.message)

    eject_card = enter_pin = withdraw_money = check_balance = insert_card
