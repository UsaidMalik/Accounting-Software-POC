from manageAccountingSheet import *
from manageProductsJSON import *


def restockInventory():
    inventoryValues = input("Enter inventory restock order: date, shipping cost, transaction fees, item, qty, "
                            "item2, qty2...")

    date, shippingCost, transactionFees, products = parseInventory(inventoryValues)
    accountingSheetName = input("Enter the name of the accounting sheet this order belongs to")
    accountingSheet = openAccountingSheet(accountingSheetName)
    accountingSheet[date + 1][43] = shippingCost
    accountingSheet[date + 1][44] = transactionFees

    accountingSheet[2][48] = float(accountingSheet[2][48])
    accountingSheet[2][48] += shippingCost + transactionFees
    accountingSheet[2][49] = float(accountingSheet[2][49])
    accountingSheet[2][49] -= shippingCost + transactionFees

    writeToSheet(accountingSheetName, accountingSheet)

    productsData = openProductsDataJSON()
    for key in products:
        productsData[key]["currentInventoryQuantity"] = int(productsData[key]["currentInventoryQuantity"])
        productsData[key]["currentInventoryQuantity"] += products[key]
    writeProductsToFile(productsData)


def parseInventory(inventoryData):
    dataEntries = inventoryData.split(",")
    date = int(dataEntries[0].split("/")[1])
    shippingCost = float(dataEntries[1])
    transactionFees = float(dataEntries[2])
    products = {}
    for i in range(3, len(inventoryData) - 3, 2):
        if inventoryData[i] in products:
            yOn = input("Mis-Input product entered twice. If you meant to do this enter Y and the values will be added"
                        "otherwise enter N to quit and re-enter value.")
            while yOn.lower() != "n" & yOn.lower() != "y":
                yOn = input(
                    "Mis-Input product entered twice. If you meant to do this enter Y and the values will be added"
                    "otherwise enter N to quit and re-enter value.")
            if yOn.lower() == "y":
                products[inventoryData[i]] += int(inventoryData[i + 1])
            elif yOn.lower() == "n":
                return 1
        else:
            products[inventoryData[i]] = int(inventoryData[i + 1])
    return date, shippingCost, transactionFees, products
