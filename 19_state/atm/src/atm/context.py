from atm.models import Account
from atm.states import ATMState, Maintenance, NoCard


class ATM:
    """Context: Stateオブジェクトを差し替えることで振る舞いを変更"""

    def __init__(self, initial_balance: int, correct_pin: str) -> None:
        self.account = Account(balance=initial_balance)
        self.correct_pin = correct_pin
        self._state: ATMState = NoCard()

    # --- 各Stateへの委譲 ---

    def insert_card(self) -> None:
        self._state.insert_card(self)

    def eject_card(self) -> None:
        self._state.eject_card(self)

    def enter_pin(self, pin: str) -> None:
        self._state.enter_pin(self, pin)

    def withdraw_money(self, amount: int) -> None:
        self._state.withdraw_money(self, amount)

    # ファサードとして現金残高を公開
    def check_balance(self) -> int:
        return self._state.check_balance(self)

    # --- ATM 内部 API ---

    def set_state(self, state: ATMState) -> None:
        self._state = state

    def get_state(self) -> ATMState:
        return self._state

    # --- メンテナンス制御 ---

    def enter_maintenance(self) -> None:
        self.set_state(Maintenance())

    def exit_maintenance(self) -> None:
        self.set_state(NoCard())
