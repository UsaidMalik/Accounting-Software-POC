import json


def addProductDataEtsy(itemName, keyName):
    productOrderData = {}
    with open("all.json", 'r') as json_file:
        productOrderData = json.load(json_file)

    myproductdata = {}
    with open("products.json", 'r') as json_file:
        myproductdata = json.load(json_file)


    itemsOrders = {}
    for key in productOrderData:
        if itemName in productOrderData[key]["Item"]:
            totalRevenue = round(float(productOrderData[key]["itemPrice"]) * (1 - float(productOrderData[key]["Discount"]) ) + \
                                     float(productOrderData[key]["shippingByBuyer"]) + \
                                     float(productOrderData[key]["Tax"]), 2)
            transactionFee = round(totalRevenue * 0.03 + 0.25, 2)
            platformFee = round((float(productOrderData[key]["itemPrice"]) * (1 - float(productOrderData[key]["Discount"])) * 0.065), 2)
            shippingByKord = 4.00 if productOrderData[key]["shippingByBuyer"] < 4.00 else productOrderData[key]["shippingByBuyer"] + 2
            actualRevenue = round(totalRevenue - shippingByKord - productOrderData[key]["Tax"] - transactionFee - platformFee, 2)
            profit = actualRevenue - float(myproductdata[keyName]["purchasePrice"])
            itemsOrders[productOrderData[key]["Date"]] = {
                "totalOrderRevenue": totalRevenue,
                "itemPriceAtSale": productOrderData[key]["itemPrice"],
                "Discount": productOrderData[key]["Discount"],
                "shippingCostPaidByBuyer": productOrderData[key]["shippingByBuyer"],
                "shippingCostPaidByKord": shippingByKord, # amortized
                "taxPaidByBuyer": productOrderData[key]["Tax"],
                "transactionFeesPaid": transactionFee,
                "platformFeesPaid": platformFee,
                "actualRevenue": actualRevenue,
                "Platform": "Etsy",
                "Profit": round(profit, 2),
                "Margin": round(profit/totalRevenue, 2)
            }


    currID = 0
    for key in itemsOrders:
        if key not in myproductdata[keyName]["lifetimeSalesDetails"]["Dates"]:
            myproductdata[keyName]["lifetimeSalesDetails"]["Dates"][key] = itemsOrders[key]
        else:
            myproductdata[keyName]["lifetimeSalesDetails"]["Dates"][key + f'{currID}'] = itemsOrders[key]
            currID += 1


    print(myproductdata[keyName]["lifetimeSalesDetails"])
    with open("products.json", 'w') as json_file:
        json.dump(myproductdata, json_file, indent=4)


    with open(f"{keyName}.json", 'w') as json_file:
        json.dump(myproductdata[keyName], json_file, indent=4)

addProductDataEtsy("Gupp", "guppyKeycaps")