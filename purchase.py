from accountant import Product, my_account, my_warehouse, get_input_and_save

print("Hello!\nTo note a purchase type: product name, its price and number of purchased products.\n"
      "When you are done with purchasing, type >stop< to finish.")


@get_input_and_save("Write your purchase:", 0, 1, 2)
def record_purchase(product_name, product_price, product_qty):
    input_product = Product(product_name, product_qty) # adding product with its name and number
    if product_price < 0 or input_product.number < 0:  # price and number must be positive
        print('Error - price and number must be positive.')
        return False
    if not my_warehouse.add_product(input_product, product_price):  # gdy nie udało się kupić produktu
        print(f'Error - not enough money!')
        return False
