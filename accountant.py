# ALLOWED_COMMANDS: 'payment', 'sale', 'purchase', 'account', 'warehouse', 'history', 'stop'


class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, action_name):
        def decorate(callback):
            self.actions[action_name] = callback
        return decorate

    def execute(self, action_name):
        if action_name not in self.actions:
            print("Action not defined")
        else:
            self.actions[action_name](self)


class Product:
    def __init__(self, nm, nb):
        self.name = nm  # unikalna
        self.number = nb  # ile mamy na stanie

    def __str__(self):
        return f'{self.name}: {self.number}'


class Warehouse:
    def __init__(self, local_account):
        self.products = {}  # warehouse status - key - name, value - Product
        self.account = local_account
        self.read_warehouse()  # tworząc obiekt wywołujemy metodę czytającą z pliku,
                                # zapisującą dane do słownika produktów
        # self.read_history()  # i tak samo z historią, też ją ładujemy od razu

    def read_warehouse(self):
        with open("warehouse.txt", "r") as file:
            for line in file.readlines():
                current_line = line.split(",")
                self.products[current_line[0]] = Product(current_line[0], int(current_line[1].split("\n")[0]))

    def read_history(self):
        with open("history.txt", "r") as file:
            for line in file.readlines():
                self.account.account_history.append(line)

    def add_product(self, local_product, price):
        if not self.account.update_balance(-price * local_product.number):  # jeśli nie mamy tyle pieniędzy
            return False
        if local_product.name in self.products:
            self.products[local_product.name].number += local_product.number
        else:
            self.products[local_product.name] = local_product
        self.account.account_history.append(f'Purchase: {local_product.name}, {price}, {local_product.number}')
        return True

    def remove_product(self, local_product, price):
        if local_product.name not in self.products:
            return False
        if self.products[local_product.name].number < local_product.number:
            return False
        self.products[local_product.name].number -= local_product.number
        self.account.update_balance(price * local_product.number)
        self.account.account_history.append(f'Sale: {local_product.name}, {price}, {local_product.number}')
        return True

    def show_products(self, local_input):
        for product_name in local_input:
            if product_name not in self.products:
                print(f'Product: {product_name} not in offer.')
            else:
                print(f'Product: {product_name} - in stock: {self.products[product_name].number}')
        self.account.account_history.append(f'Stock status for: {local_input}')

    def save_stock(self):
        last_product = list(self.products.keys())[-1]
        with open("warehouse.txt", "w") as file:
            for name, product in self.products.items():
                file.write(name + "," + str(product.number))
                if name != last_product:
                    file.write("\n")

    def save_history(self):
        with open("history.txt", "a") as file:  # tutaj nadpisujemy, nie zapisujemy od nowa
            for action in self.account.account_history:
                file.write(action + "\n")


class Account:
    def __init__(self):
        self.balance = 0
        self.account_history = []
        self.read_account()

    def read_account(self):
        with open("account.txt", "r") as file:
            self.balance = int(file.readline())

    def show_account_balance(self):
        print(f'Current account balance is {self.balance}.')
        self.account_history.append(f'Show balance: {self.balance}')

    def add_payment(self, local_input_list):
        payment_amount = int(local_input_list[0])
        comment = local_input_list[1:]
        self.update_balance(payment_amount)
        self.account_history.append(f'Payment: {payment_amount}, {comment}')

    def update_balance(self, amount):  # amount can be negative
        if self.balance + amount < 0:
            return False
        self.balance += amount
        return True

    def save_account(self):
        with open("account.txt", "w") as file:  # otwieramy plik do zapisu
            file.write(str(self.balance))


my_manager = Manager()
my_account = Account()
my_warehouse = Warehouse(my_account)


@my_manager.assign("account")
def print_account_balance(my_manager):
    print(f'Current account balance is {my_account.balance}.')


@my_manager.assign("history")
def print_action_history(my_manager):
    my_warehouse.read_history()
    for action in my_account.account_history:
        print(action)


@my_manager.assign("payment")
def record_payment(my_manager):
    print("Hello!\nTo record a payment type the amount and the comment.\n"
          "When you are done with updates, type >stop< to finish.")
    while True:
        input_string = input("New payment: ")
        input_list = input_string.split()
        if input_list[0] == 'stop':
            my_warehouse.save_history()
            my_account.save_account()
            break
        if len(input_list) >= 2:  # if enough parameters given
            my_account.add_payment(input_list)
        continue


@my_manager.assign("purchase")
def record_purchase(my_manager):
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


@my_manager.assign("sale")
def record_sale(my_manager):
    print("Hello!\nTo note a sale write: product name, its price and number of sold products.\n"
          "When you are done with updates, type >stop< to finish.")
    while True:
        input_string = input("Write your sale: ")
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
        if not my_warehouse.remove_product(input_product, product_price):  # gdy nie udało się odjąć produktu
            print(f'Error - out of stock')
        continue


@my_manager.assign("warehouse")
def show_stock(my_manager):
    print("Hello!\nTo see the stock status of a product type names of chosen products after space."
          "When you are done, type >stop< to finish.")

    while True:
        input_string = input("Product names: ")
        input_list = input_string.split()
        if input_list[0] == 'stop':
            my_warehouse.save_stock()
            my_warehouse.save_history()
            my_account.save_account()
            break
        print(f'Stock status:')
        my_warehouse.show_products(input_list)
        continue