import json
import csv


def addProductDataFacebook():
    productOrderData = []
    with open('Facebook Order Data.csv', newline='', encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            productOrderData.append(row)
    productOrderData.pop(0)

    productData = {}
    with open("products.json", 'r') as json_file:
        productData = json.load(json_file)

    id = 0
    for row in productOrderData:
        if "1,1"not in row[9]:
            key = row[8]
            totalRevenue = float(row[3][1:]) + float(row[4][1:]) + float(row[6][1:])
            transactionFee = 0
            platformFee = 0
            actualRevenue = totalRevenue - float(row[4][1:]) - float(row[6][1:])
            profit = actualRevenue - float(productData[key]["purchasePrice"])
            if row[1][1:] not in productData[key]["lifetimeSalesDetails"]["Dates"]:
                productData[key]["lifetimeSalesDetails"]["Dates"][row[1][1:]] = {
                    "totalOrderRevenue": totalRevenue,
                    "itemPriceAtSale": row[3][1:],
                    "Discount": "N/A",
                    "shippingCostPaidByBuyer": row[6][1:],
                    "shippingCostPaidByKord": 4,  # amortized
                    "taxPaidByBuyer": row[4][1:],
                    "transactionFeesPaid": transactionFee,
                    "platformFeesPaid": platformFee,
                    "actualRevenue": round(actualRevenue, 2),
                    "Platform": "Facebook",
                    "Profit": round(profit, 2),
                    "Margin": round(profit / totalRevenue, 2)
                }
            else:
                productData[key]["lifetimeSalesDetails"]["Dates"][row[1][1:] + str(id)] = {
                    "totalOrderRevenue": totalRevenue,
                    "itemPriceAtSale": row[3][1:],
                    "Discount": "N/A",
                    "shippingCostPaidByBuyer": row[6][1:],
                    "shippingCostPaidByKord": 4,  # amortized
                    "taxPaidByBuyer": row[4][1:],
                    "transactionFeesPaid": transactionFee,
                    "platformFeesPaid": platformFee,
                    "actualRevenue": round(actualRevenue, 2),
                    "Platform": "Facebook",
                    "Profit": round(profit, 2),
                    "Margin": round(profit / totalRevenue, 2)
                }

    with open("products.json", 'w') as json_file:
        json.dump(productData, json_file, indent=4)


addProductDataFacebook()