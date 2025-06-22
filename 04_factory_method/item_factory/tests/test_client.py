import pytest


@pytest.mark.parametrize(
    "factory_type,item_type,kwargs",
    [
        (
            "furniture",
            "chair",
            {"name": "X", "price": 10, "material": "fabric", "has_armrests": False},
        ),
        (
            "furniture",
            "table",
            {"name": "Y", "price": 20, "shape": "square", "capacity": 2},
        ),
        ("toy", "car", {"name": "Z", "price": 5, "max_speed": 50, "is_electric": False}),
        (
            "toy",
            "doll",
            {"name": "W", "price": 15, "age_range": "1-3", "material": "cloth"},
        ),
    ],
)
def test_client_creates_and_uses_items(client, capsys, factory_type, item_type, kwargs):
    # 呼び出し時にエラーが出ないこと
    client.create_and_use(factory_type, item_type, **kwargs)
    captured = capsys.readouterr()
    # 生成item名と use() メッセージが出力されること
    assert "Created: " in captured.out
    assert item_type in captured.out
    assert "Use:" in captured.out


def test_client_unknown_factory(client, capsys):
    client.create_and_use(
        "unknown", "chair", name="A", price=10, material="wood", has_armrests=True
    )
    captured = capsys.readouterr()
    assert "Unknown factory" in captured.out


def test_client_invalid_item_type(client, capsys):
    client.create_and_use("toy", "robot", name="B", price=10, max_speed=20, is_electric=True)
    captured = capsys.readouterr()
    assert "Unknown toy" in captured.out or "Unknown factory" in captured.out


def test_client_validation_error(client, capsys):
    # price がマイナスでバリデーションエラー
    client.create_and_use("toy", "car", name="BadCar", price=-5, max_speed=30, is_electric=False)
    captured = capsys.readouterr()
    assert "Input should be greater than 0" in captured.out
