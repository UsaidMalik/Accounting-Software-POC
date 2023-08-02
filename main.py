import json
from accountForOrder import accountForOrder


file_path = 'products.json'
with open(file_path, 'r') as file:
    products = json.load(file)


def main():
    print("Hello Yahya, What would you like to do today? \nAdd New Product (-addProduct) \n"
          "Edit Existing Product (-editProduct) \nAdd Order To Accounting (-order) \n"
          "Add Restock Order (-restockOrder) \nAdd Advertising Costs to Accounting (-advertising)")
    command = input("Enter Command: ")
    if command == "-order":
        accountForOrder()


if __name__ == "__main__":
    main()
