import json
import csv


def addProductDataShopify():
    productOrderData = []
    with open('Shopify Order Data.csv', newline='', encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            productOrderData.append(row)
    productOrderData.pop(0)

    productData = {}
    with open("products.json", 'r') as json_file:
        productData = json.load(json_file)

    id = 0
    currOrderID = 0
    productDataLength = len(productOrderData)
    for i in range(productDataLength):
        if productOrderData[i][0] != currOrderID:
            iteratorOffset = 1
            items = [productOrderData[i % productDataLength]]
            while productOrderData[i + iteratorOffset - 1 % productDataLength][0] == productOrderData[(i + iteratorOffset) % productDataLength][0]:
                items.append(productOrderData[i + iteratorOffset % productDataLength])
                iteratorOffset += 1
            orderSubtotal = float(items[0][8])
            shippingByBuyer = round(float(items[0][9]) / len(items), 2)
            taxRate = float(items[0][10])/(orderSubtotal + shippingByBuyer)

            print("location is ", items[0][32])
            shippingByKord = 4 / len(items) if items[0][32] == "US" else 17 / len(items)
            discountRate = round(float(items[0][13]) / (float(items[0][13]) + orderSubtotal), 2)
            date = items[0][3].split(" ")[0]
            for row in items:
                key = row[17]
                print("row is", row)
                itemRevenue = (float(row[18]) * (1 - discountRate)) + shippingByBuyer
                itemTaxes = itemRevenue * taxRate
                itemRevenue += itemTaxes
                productPrice = float(row[19]) if row[19] != "0" and row[19] != "" else float(row[18])
                transactionFee = 0.05 * (itemRevenue + itemTaxes)
                platformFee = 0
                actualRevenue = itemRevenue - shippingByKord - itemTaxes - transactionFee - platformFee
                profit = actualRevenue - float(productData[key]["purchasePrice"])

                print("discount is ", discountRate)

                if date not in productData[key]["lifetimeSalesDetails"]["Dates"]:
                    productData[key]["lifetimeSalesDetails"]["Dates"][date] = {
                        "totalOrderRevenue": itemRevenue,
                        "itemPriceAtSale": productPrice,
                        "Discount": discountRate,
                        "shippingCostPaidByBuyer": shippingByBuyer,
                        "shippingCostPaidByKord": shippingByKord,  # amortized
                        "taxPaidByBuyer": itemTaxes,
                        "transactionFeesPaid": transactionFee,
                        "platformFeesPaid": platformFee,
                        "actualRevenue": round(actualRevenue, 2),
                        "Platform": "Shopify",
                        "Profit": round(profit, 2),
                        "Margin": round(profit / itemRevenue, 2)
                    }
                else:
                    productData[key]["lifetimeSalesDetails"]["Dates"][date + str(id)] = {
                        "totalOrderRevenue": itemRevenue,
                        "itemPriceAtSale": productPrice,
                        "Discount": discountRate,
                        "shippingCostPaidByBuyer": shippingByBuyer,
                        "shippingCostPaidByKord": shippingByKord,  # amortized
                        "taxPaidByBuyer": itemTaxes,
                        "transactionFeesPaid": transactionFee,
                        "platformFeesPaid": platformFee,
                        "actualRevenue": round(actualRevenue, 2),
                        "Platform": "Shopify",
                        "Profit": round(profit, 2),
                        "Margin": round(profit / itemRevenue, 2)
                    }

        currOrderID = productOrderData[i][0]
        id += 1

    with open("products.json", 'w') as json_file:
        json.dump(productData, json_file, indent=4)


def removeShopify():
    productData = {}
    with open("products.json", 'r') as json_file:
        productData = json.load(json_file)

    keysToRemove = []
    for product in productData:
        for date in productData[product]["lifetimeSalesDetails"]["Dates"]:
            if productData[product]["lifetimeSalesDetails"]["Dates"][date]["Platform"] == "Shopify":
                keysToRemove.append([product, date])

    for keys in keysToRemove:
        del productData[keys[0]]["lifetimeSalesDetails"]["Dates"][keys[1]]

    with open("products.json", 'w') as json_file:
        json.dump(productData, json_file, indent=4)


addProductDataShopify()