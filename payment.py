from accountant import my_manager

my_manager.execute("payment")

#from accountant import Account, Warehouse, my_warehouse, my_account

# print("Hello!\nTo record a payment type the amount and the comment.\n"
#       "When you are done with updates, type >stop< to finish.")
#
# while True:
#     input_string = input("New payment: ")
#     input_list = input_string.split()
#     if input_list[0] == 'stop':
#         my_warehouse.save_history()
#         my_account.save_account()
#         break
#     if len(input_list) >= 2:  # if enough parameters given
#         my_account.add_payment(input_list)
#     continue
