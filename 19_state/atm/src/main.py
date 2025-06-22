from atm.context import ATM

atm = ATM(initial_balance=30_000, correct_pin="1234")
atm.insert_card()
try:
    atm.enter_pin("1230")
except Exception as e:
    print(f"Error: {e}")
atm.insert_card()
atm.enter_pin("1234")
try:
    atm.withdraw_money(50_000)
except Exception as e:
    print(f"Error: {e}")
atm.withdraw_money(5_000)
atm.enter_maintenance()
try:
    atm.eject_card()
except Exception as e:
    print(f"Error: {e}")
atm.exit_maintenance()
atm.insert_card()
