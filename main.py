from accountForOrder import accountForOrder
from createNewProduct import createProduct
from accountForAdvertising import accountForAdvertising
from restockInventory import restockInventory
from addPurchase import addPurchase


def main():
    print("Hello Yahya, What would you like to do today? \n \nAdd New Product (-addProduct) \n"
          "Edit Existing Product (-editProduct) \nAdd Order To Accounting (-order) \n"
          "Add Restock of Inventory (-inventoryRestockPurchase) \nAdd Advertising Costs to Accounting (-advertising) \n"
          "Report a Miscellaneous Purchase (-addOtherPurchase) \n")
    command = input("Enter Command: ")
    if command == "-order":
        accountForOrder()
    elif command == "-addProduct":
        createProduct()
    elif command == "-advertising":
        accountForAdvertising()
    elif command == "-inventoryRestockPurchase":
        restockInventory()
    elif command == "-addOtherPurchase":
        addPurchase()
    elif command == "-editProduct":
        print("This doesnt exist yet lol")


if __name__ == "__main__":
    main()
