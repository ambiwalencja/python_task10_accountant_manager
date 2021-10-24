from accountant import my_manager

my_manager.execute("warehouse")

# from accountant import Account, Warehouse, Product, my_account, my_warehouse
#
# print("Hello!\nTo see the stock status of a product type names of chosen products after space."
#       "When you are done, type >stop< to finish.")
#
# while True:
#     input_string = input("Product names: ")
#     input_list = input_string.split()
#     if input_list[0] == 'stop':
#         my_warehouse.save_stock()
#         my_warehouse.save_history()
#         my_account.save_account()
#         break
#     print(f'Stock status:')
#     my_warehouse.show_products(input_list)
#     continue
