from accountant import Account, Warehouse, my_warehouse, my_account

my_warehouse.read_history()

for action in my_account.account_history:
    print(action)
