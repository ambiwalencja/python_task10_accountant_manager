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


my_account = Account()
my_warehouse = Warehouse(my_account)


# dekorator, który zajmuje się wykonaniem tych czynności, które powtarzają się przy rejestrowaniu płatności, sprzedaży
# i zakupu, czyli pobiera informacje ze standardowego wejścia i pakuje je do zmiennych, a następnie po wykonaniu
# funkcji zapisuje do plików historię, stan konta i stan magazynu
def get_input_and_save(label, int_before, str_count, int_after): # label - message to user, int_before - number of
    # integer values needed as input arguments for the function before the string value, then str_count - number of
    # strings needed for the function, and int_after - number of integers after string value. eg. if for my
    # function I need product name (str), price (int) and number (int), the values here will be 0, 1, 2.
    def decorate(callback):
        while True:
            input_string = input(label)
            input_list = input_string.split()  # lista stringów
            if input_list[0] == 'stop':
                my_warehouse.save_stock()
                my_warehouse.save_history()
                my_account.save_account()
                break
            if len(input_list) < (int_before + str_count + int_after):  # if not enough parameters given
                print("Please give appropriate number of arguments.")
                continue
            arg_before = [int(arg) for arg in input_list[0:int_before]]  # skrótowy zapis pętli. arg_before to lista
            # (bo jest w []) parametrów przekształconych w integery - z całej listy parametrów iput_list wzięliśmy
            # slice z int_before parametrów z początku
            input_list_int_after = input_list[-int_after:] if int_after else []  # dodałam tę linijkę, ponieważ
            # input_list[-int_after:] nie działa, gdy int_after = 0, zwraca wtedy pełną listę
            arg_after = [int(arg) for arg in input_list_int_after]  # i od końca
            glue = " "
            arg_str = [glue.join(input_list[int_before:-int_after])]  # a wszystko, co było pomiędzy, łączymy razem
            #                                                             w stringa poprzedzielanego spacjami
            args = arg_before + arg_str + arg_after  # następnie łączę otrzymane, przekształcone odpowiednio
            #                                        argumenty w listę, którą wciągnę do funkcji działającej (callback)
            #                                        w takiej formie, w jakiej ich potrzebuję
            if not callback(*args):  # dzięki gwiazdce nie muszę w definicji ani w wywołaniu funkcji callback podawać
            # listy (bo lista jest jednym obiektem) składającej się z argumentów, których potrzebuję, ale mogę podać
            # po kolei już argumenty, które mnie interesują i zostaną one wszystkie zinterpretowane
                continue
    return decorate



