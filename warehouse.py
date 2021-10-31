from accountant import my_warehouse

print("Hello!\nTo see the stock status of a product type names of chosen products after commas."
      "When you are done, type >stop< to finish.")

while True:
    input_string = input("Product names: ")
    input_list = input_string.split(", ")
    if input_list[0] == 'stop':
        my_warehouse.save_history()
        break
    print(f'Stock status:')
    my_warehouse.show_products(input_list)
    continue
