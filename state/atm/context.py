from .states import NoCardState, MaintenanceState, HasCardState, AuthenticatedState


class ATM:
    def __init__(self, initial_balance, correct_pin):
        self.balance = initial_balance
        self.correct_pin = correct_pin
        self.state = NoCardState()  # 初期状態

    def set_state(self, state):
        self.state = state

    def enter_maintenance(self):
        print("メンテナンスモードに移行します。")
        if isinstance(self.state, HasCardState) or isinstance(
            self.state, AuthenticatedState
        ):
            print("カードが取り出されます。")
            self.state.eject_card(self)
        self.set_state(MaintenanceState())

    def exit_maintenance(self):
        print("メンテナンスモードを終了します。")
        self.set_state(NoCardState())

    def insert_card(self):
        self.state.insert_card(self)

    def eject_card(self):
        self.state.eject_card(self)

    def enter_pin(self, pin):
        self.state.enter_pin(self, pin)

    def withdraw_money(self, amount):
        self.state.withdraw_money(self, amount)
