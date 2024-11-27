from abc import ABC, abstractmethod


class ATMState(ABC):
    @abstractmethod
    def insert_card(self, atm):
        pass

    @abstractmethod
    def eject_card(self, atm):
        pass

    @abstractmethod
    def enter_pin(self, atm, pin):
        pass

    @abstractmethod
    def withdraw_money(self, atm, amount):
        pass


class NoCardState(ATMState):
    def insert_card(self, atm):
        print("カードが挿入されました。")
        atm.set_state(HasCardState())

    def eject_card(self, atm):
        print("カードは挿入されていません。")

    def enter_pin(self, atm, pin):
        print("カードを挿入してください。")

    def withdraw_money(self, atm, amount):
        print("カードを挿入してください。")


class HasCardState(ATMState):
    def insert_card(self, atm):
        print("すでにカードが挿入されています。")

    def eject_card(self, atm):
        print("カードが取り出されました。")
        atm.set_state(NoCardState())

    def enter_pin(self, atm, pin):
        if pin == atm.correct_pin:
            print("PINコードが正しいです。")
            atm.set_state(AuthenticatedState())
        else:
            print("PINコードが間違っています。カードを取り出してください。")
            atm.set_state(NoCardState())

    def withdraw_money(self, atm, amount):
        print("PINコードを入力してください。")


class AuthenticatedState(ATMState):
    def insert_card(self, atm):
        print("操作中です。新しいカードは挿入できません。")

    def eject_card(self, atm):
        print("カードが取り出されました。")
        atm.set_state(NoCardState())

    def enter_pin(self, atm, pin):
        print("すでに認証されています。")

    def withdraw_money(self, atm, amount):
        if amount <= atm.balance:
            atm.balance -= amount
            print(f"{amount}円を引き出しました。残高: {atm.balance}円")
        else:
            print("残高が不足しています。")
        print("操作を終了します。")
        atm.set_state(NoCardState())


class MaintenanceState(ATMState):
    def insert_card(self, atm):
        print("現在メンテナンス中です。カードを挿入できません。")

    def eject_card(self, atm):
        print("カードは挿入されていません。")

    def enter_pin(self, atm, pin):
        print("現在メンテナンス中です。操作できません。")

    def withdraw_money(self, atm, amount):
        print("現在メンテナンス中です。操作できません。")
