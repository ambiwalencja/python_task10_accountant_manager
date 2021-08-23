from accountant import Account, Warehouse, Product, my_account, my_warehouse

print("Hello!\nTo note a purchase type: product name, its price and number of purchased products.\n"
      "When you are done with purchasing, type >stop< to finish.")

while True:
    input_string = input("Write your purchase: ")
    input_list = input_string.split()
    if input_list[0] == 'stop':
        my_warehouse.save_stock()
        my_warehouse.save_history()
        my_account.save_account()
        break
    if len(input_list) < 3:  # if not enough parameters given
        continue
    input_product = Product(input_list[0], int(input_list[2]))  # adding product with its name and number
    product_price = int(input_list[1])
    if product_price < 0 or input_product.number < 0:  # price and number must be positive
        print('Error - price and number must be positive.')
        continue  # try again
    if not my_warehouse.add_product(input_product, product_price):  # gdy nie udało się kupić produktu
        print(f'Error - not enough money!')
    continue
