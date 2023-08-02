from manageProductsJSON import *


def createProduct():
    productsJSON = openProductsDataJSON()
    productName, productDate, productCurrentPrice, productCost,\
        productCurrentInventory = gatherProductDate()
    if productName in productsJSON:
        print("Product already exists. Were you trying to edit? if so use -editProduct")
        return
    else:
        productsJSON[productName] = {
            "dateCreated": productDate,
            "purchasePrice": productCost,
            "currentPrice": productCurrentPrice,
            "currentInventoryQuantity": productCurrentInventory,
            "currentTurnoverRate": 0,

            "lifetimeInventorySold": 0,
            "lifetimeRevenue": 0,
            "lifetimeProfit": 0,
            "averageLifetimeMargin": 0,

            "lifetimeSalesDetails": {
              "Dates": {

                }},

            "monthData": {
            },
            "percentChangeFromPreviousMonth": {
            }
          }
    writeProductsToFile(productsJSON)



def gatherProductDate():
    productName = input("Enter product name: ")
    productDate = input("Enter the date this product was created: ")
    productCurrentPrice = input("Enter the current price of this product: ")
    productCost = input("Enter the product's cost: ")
    productCurrentInventory = input("Enter the current product inventory: ")
    return productName, productDate, productCurrentPrice, productCost, productCurrentInventory
