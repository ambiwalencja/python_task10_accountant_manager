from accountant import my_manager

my_manager.execute("sale")


# from accountant import Account, Warehouse, Product, my_account, my_warehouse
#
# print("Hello!\nTo note a sale write: product name, its price and number of sold products.\n"
#       "When you are done with updates, type >stop< to finish.")
#
# while True:
#     input_string = input("Write your sale: ")
#     input_list = input_string.split()
#     if input_list[0] == 'stop':
#         my_warehouse.save_stock()
#         my_warehouse.save_history()
#         my_account.save_account()
#         break
#     if len(input_list) < 3:  # if not enough parameters given
#         continue
#     input_product = Product(input_list[0], int(input_list[2]))  # adding product with its name and number
#     product_price = int(input_list[1])
#     if product_price < 0 or input_product.number < 0:  # price and number must be positive
#         print('Error - price and number must be positive.')
#         continue  # try again
#     if not my_warehouse.remove_product(input_product, product_price):  # gdy nie udało się odjąć produktu
#         print(f'Error - out of stock')
#     continue
