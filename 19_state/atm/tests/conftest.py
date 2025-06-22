import pytest

from atm.context import ATM


@pytest.fixture
def atm():
    """ATMのテスト用インスタンスを作成する"""
    return ATM(initial_balance=5000, correct_pin="1234")
