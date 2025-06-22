from pydantic import BaseModel, Field, PositiveInt


class Account(BaseModel):
    """現金残高と1日あたりの引き出し上限を表すドメインモデル"""

    balance: int = Field(..., ge=0)
    daily_limit: PositiveInt = 100_000
    withdrawn_today: int = 0  # 当日分

    @property
    def available(self) -> int:  # 利用可能額
        return min(self.balance, self.daily_limit - self.withdrawn_today)

    def withdraw(self, amount: int) -> None:
        if amount > self.available:
            raise ValueError("残高不足、または日次上限超過です。")
        self.balance -= amount
        self.withdrawn_today += amount
