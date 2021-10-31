from accountant import Account, Warehouse, my_warehouse, my_account, get_input_and_save

print("Hello!\nTo record a payment type the amount and the comment.\n"
      "When you are done with updates, type >stop< to finish.")


@get_input_and_save("New payment: ", 1, 1, 0)
def record_payment(payment_amount, payment_comment):
    input_list = [payment_amount, payment_comment]
    my_account.add_payment(input_list)
