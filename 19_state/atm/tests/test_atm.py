import pytest

from atm.exceptions import InvalidOperation
from atm.states import (
    Authenticated,
    HasCard,
    NoCard,
)


def test_initial_state(atm):
    """初期状態がNoCardであることを確認"""
    assert isinstance(atm.get_state(), NoCard)


def test_card_insertion(atm):
    """カード挿入後に状態がHasCardになることを確認"""
    atm.insert_card()
    assert isinstance(atm.get_state(), HasCard)


def test_pin_authentication(atm):
    """正しいPINコードでAuthenticatedに遷移することを確認"""
    atm.insert_card()
    atm.enter_pin("1234")
    assert isinstance(atm.get_state(), Authenticated)


def test_pin_authentication_failure(atm):
    """間違ったPINコードでNoCardに戻ることを確認"""
    atm.insert_card()
    with pytest.raises(InvalidOperation) as exc_info:
        atm.enter_pin("0000")
    assert str(exc_info.value) == "PIN が誤っています。カードを取り出しました。"
    assert isinstance(atm.get_state(), NoCard)


def test_withdraw_money(atm):
    """認証後に正しく引き出しができることを確認"""
    atm.insert_card()
    atm.enter_pin("1234")
    atm.withdraw_money(1000)
    assert isinstance(atm.get_state(), NoCard)
    atm.insert_card()
    atm.enter_pin("1234")
    assert atm.check_balance() == 4000


def test_check_balance_requires_auth(atm):
    """残高確認は認証後にのみ可能であることを確認"""
    atm.insert_card()
    with pytest.raises(InvalidOperation):
        atm.check_balance()
    atm.enter_pin("1234")
    assert atm.check_balance() == 5000


def test_insufficient_balance(atm):
    """残高不足の場合の動作を確認"""
    atm.insert_card()
    atm.enter_pin("1234")
    with pytest.raises(ValueError) as exc_info:
        atm.withdraw_money(6000)
    assert str(exc_info.value) == "残高不足、または日次上限超過です。"
    assert atm.check_balance() == 5000  # 残高が変わらない


def test_exit_maintenance_mode(atm):
    """メンテナンスモード終了後にNoCardに戻ることを確認"""
    atm.enter_maintenance()
    atm.exit_maintenance()
    assert isinstance(atm.get_state(), NoCard)
