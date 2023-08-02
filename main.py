from accountForOrder import accountForOrder
from createNewProduct import createProduct


def main():
    print("Hello Yahya, What would you like to do today? \n \nAdd New Product (-addProduct) \n"
          "Edit Existing Product (-editProduct) \nAdd Order To Accounting (-order) \n"
          "Add Restock Order (-restockOrder) \nAdd Advertising Costs to Accounting (-advertising) \n")
    command = input("Enter Command: ")
    if command == "-order":
        accountForOrder()
    elif command == "-addProduct":
        createProduct()


if __name__ == "__main__":
    main()
