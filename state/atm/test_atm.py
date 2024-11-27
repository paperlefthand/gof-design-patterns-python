import pytest

from atm.states import (
    NoCardState,
    AuthenticatedState,
    MaintenanceState,
    HasCardState,
)
from atm.context import ATM


@pytest.fixture
def atm():
    """ATMのテスト用インスタンスを作成する"""
    return ATM(initial_balance=5000, correct_pin=1234)


def test_initial_state(atm):
    """初期状態がNoCardStateであることを確認"""
    assert isinstance(atm.state, NoCardState)


def test_card_insertion(atm):
    """カード挿入後に状態がHasCardStateになることを確認"""
    atm.insert_card()
    assert isinstance(atm.state, HasCardState)


def test_pin_authentication(atm):
    """正しいPINコードでAuthenticatedStateに遷移することを確認"""
    atm.insert_card()
    atm.enter_pin(1234)
    assert isinstance(atm.state, AuthenticatedState)


def test_pin_authentication_failure(atm):
    """間違ったPINコードでNoCardStateに戻ることを確認"""
    atm.insert_card()
    atm.enter_pin(1111)
    assert isinstance(atm.state, NoCardState)


def test_withdraw_money(atm):
    """認証後に正しく引き出しができることを確認"""
    atm.insert_card()
    atm.enter_pin(1234)
    atm.withdraw_money(1000)
    assert atm.balance == 4000
    assert isinstance(atm.state, NoCardState)


def test_insufficient_balance(atm):
    """残高不足の場合の動作を確認"""
    atm.insert_card()
    atm.enter_pin(1234)
    atm.withdraw_money(6000)
    assert atm.balance == 5000  # 残高が変わらない
    assert isinstance(atm.state, NoCardState)


def test_maintenance_mode_from_has_card_state(atm, mocker):
    """カード挿入後にメンテナンスモードへ移行するとカードが取り出されることを確認"""
    atm.insert_card()
    mock_eject_card = mocker.patch.object(
        atm.state, "eject_card", wraps=atm.state.eject_card
    )
    atm.enter_maintenance()
    mock_eject_card.assert_called_once()  # eject_cardが1回呼ばれることを確認
    assert isinstance(atm.state, MaintenanceState)


def test_maintenance_mode_from_authenticated_state(atm, mocker):
    """認証後にメンテナンスモードへ移行するとカードが取り出されることを確認"""
    atm.insert_card()
    atm.enter_pin(1234)
    mock_eject_card = mocker.patch.object(
        atm.state, "eject_card", wraps=atm.state.eject_card
    )
    atm.enter_maintenance()
    mock_eject_card.assert_called_once()  # eject_cardが1回呼ばれることを確認
    assert isinstance(atm.state, MaintenanceState)


def test_exit_maintenance_mode(atm):
    """メンテナンスモード終了後にNoCardStateに戻ることを確認"""
    atm.enter_maintenance()
    atm.exit_maintenance()
    assert isinstance(atm.state, NoCardState)
