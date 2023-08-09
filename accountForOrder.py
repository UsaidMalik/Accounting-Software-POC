from manageAccountingSheet import *
from updateProductdata import parsePlatformDataForUpdating
from manageProductsJSON import openProductsDataJSON


def accountForOrder():
    # ask for accounting sheet first step
    accountingSheetName = input("Enter the Name of an existing accounting sheet or Create a New One "
                                "by typing in a name: ")
    accountingSheet = openAccountingSheet(accountingSheetName)
    saleData = input("Enter date, (mm/dd/yy format), pr1, qty1, discount1, shippingcost1, "
                            "pr2, qty2, discount2, shippingcost2..., platform, "
                            "and repeat for any other platforms: ").replace(" ", "").split(",")
    etsyData, shopifyData, facebookData, date = parseSaleData(saleData)

    parsePlatformDataForUpdating(etsyData, "Etsy", date)
    parsePlatformDataForUpdating(shopifyData, "Shopify", date)
    parsePlatformDataForUpdating(facebookData, "facebookData", date)

    writeDataToSheet(etsyData, date, 0, 0.9325, accountingSheet)
    writeDataToSheet(shopifyData, date, 14, 0.95, accountingSheet)
    writeDataToSheet(facebookData, date, 28, 1, accountingSheet)

    writeToSheet(accountingSheetName, accountingSheet)


def parseSaleData(saleData):
    # parsing works

    date = int(saleData.pop(0).split('/')[1])
    platformsIndices = {}  # this variable finds teh index the platform is found at in the command
    # and stores it as index : platform

    for i in range(len(saleData)):
        # this loop goes through the product data array and then finds the
        # location of all the platform data so it can be split
        if saleData[i] == "Etsy" or saleData[i] == "Shopify" or saleData[i] == "Facebook":
            platformsIndices[i] = saleData[i]

    etsyData = []
    shopifyData = []
    facebookData = []
    # product data arrays
    prevIndex = 0
    for key in platformsIndices:
        if platformsIndices[key] == "Etsy":
            etsyData = saleData[prevIndex: key]
        elif platformsIndices[key] == "Shopify":
            shopifyData = saleData[prevIndex: key]
        elif platformsIndices[key] == "Facebook":
            facebookData = saleData[prevIndex: key]
        prevIndex = key + 1
    return etsyData, shopifyData, facebookData, date


def writeDataToSheet(platformData, date, offset, platformFees, data):
    products = openProductsDataJSON()
    for i in range(0, len(platformData), 4):
        productID = platformData[i]
        product = products[productID]
        productQuantity = int(platformData[i + 1])
        productDiscount = float(platformData[i + 2])
        productShippingCost = float(platformData[i + 3])

        for j in range(1, 7):
            data[2][j + offset] = float(data[2][j + offset])
        for k in range(productQuantity):
            data[2][1 + offset] += (product["currentPrice"] * (1 - productDiscount)) * platformFees # revenue
            data[2][2 + offset] += product["purchasePrice"] + productShippingCost # cost total
            data[2][3 + offset] += productShippingCost
            data[2][4 + offset] += product["purchasePrice"]

        data[2][5 + offset] = data[2][1 + offset] - data[2][2 + offset]  # profit
        data[2][6 + offset] = round(data[2][5 + offset] / data[2][1 + offset], 2)  # margin

        for j in range(8, 14):
            data[date + 1][j + offset] = float(data[2][j + offset])
        for k in range(productQuantity):
            data[date + 1][8 + offset] += product["currentPrice"] * (1 - productDiscount) * platformFees # revenue
            data[date + 1][9 + offset] += product["purchasePrice"] + productShippingCost # cost
            data[date + 1][10 + offset] += productShippingCost
            data[date + 1][11 + offset] += product["purchasePrice"]
            data[date + 1][12 + offset] = data[date + 1][8 + offset] - data[date + 1][9 + offset]
            data[date + 1][13 + offset] = round(data[date + 1][12 + offset] / data[date + 1][8 + offset], 2) # margin
            # data[date + 1][14] is the days cost
            # TR, TC, TSC, TPC, TP, AM, TA, DR, DC, DSC, DPC, DP, DM, DA
