def updateProductData(productID, quantitySold, discount, platform, productsJSON, date, shippingCost):
    platformFees = 1
    if platform == "Shopify":
        platformFees = 0.95
    elif platform == "Etsy":
        platformFees = 0.935

    product = productsJSON[productID]
    product["currentInventoryQuantity"] = int("currentInventoryQuantity")
    product["lifetimeInventorySold"] = int(product["lifetimeInventorySold"])
    product["lifetimeRevenue"] = float(product["lifetimeRevenue"])
    product["lifetimeProfit"] = float("lifetimeProfit")
    product["averageLifetimeMargin"] = float(product["averageLifetimeMargin"])
    product["averageLifetimeTurnoverRate"] = float(product["averageLifetimeTurnoverRate"])

    product["currentInventoryQuantity"] -= quantitySold
    product["lifetimeInventorySold"] += quantitySold
    product["lifetimeRevenue"] += (float(product["currentPrice"]) * discount) * platformFees
    product["lifetimeProfit"] += ((float(product["currentPrice"]) * discount) * platformFees) - \
                                 float(product["purchasePrice"])

    product["averageLifetimeMargin"] = product["lifetimeProfit"]/product["lifetimeRevenue"]
    monthYear = date[0:2] + date[4:7]
    if monthYear in product["monthData"]:

        product["monthData"][monthYear]["inventoryEnd"] = \
            int(product["monthData"][monthYear]["inventoryEnd"])

        product["monthData"][monthYear]["turnoverRate"] = \
            float(product["monthData"][monthYear]["turnoverRate"])

        product["monthData"][monthYear]["Profit"] = \
            float(product["monthData"][monthYear]["Profit"])

        product["monthData"][monthYear]["totalSold"] = \
            int(product["monthData"][monthYear]["totalSold"])

        product["monthData"][monthYear]["Revenue"] = \
            float(product["monthData"][monthYear]["Revenue"])

        product["monthData"][monthYear]["Margin"] = \
            float(product["monthData"][monthYear]["Margin"])

        product["monthData"][monthYear]["inventoryEnd"] -= quantitySold
        product["monthData"][monthYear]["totalSold"] += quantitySold

        product["monthData"][monthYear]["turnoverRate"] = product["monthData"][monthYear]["totalSold"] \
                                                          / 30

        product["monthData"][monthYear]["Revenue"] += (float(product["currentPrice"]) * discount) * platformFees
        product["monthData"][monthYear]["Profit"] += ((float(product["currentPrice"]) * discount) * platformFees) - \
                                 float(product["purchasePrice"])

        product["monthData"][monthYear]["Margin"] =  product["monthData"][monthYear]["Profit"] \
                                                     / product["monthData"][monthYear]["Revenue"]
    else:
        # this doesnt work have to get data from prev month somehow
        prevMonthYear = ""
        if monthYear[0:2] == "01":
            prevMonthYear = "12" + str((int(monthYear[3:5]) - 1))
        else:
            prevMonthYear = str((int(monthYear[0:2]) - 1)) + monthYear[2:5]

        previousMonthDateData = product["monthData"][prevMonthYear]
        product["monthData"][monthYear] = {
            "inventoryBeginning": previousMonthDateData["inventoryEnd"],
            "inventoryEnd": previousMonthDateData["inventoryEnd"],
            "totalSold": quantitySold,
            "turnoverRate": 0,
            "Revenue": 0,
            "Profit": 0,
            "Margin": 0
          }


        product["monthData"][monthYear]["turnoverRate"] = product["monthData"][monthYear]["totalSold"] \
                                                          / 30

        product["monthData"][monthYear]["Revenue"] += (float(product["currentPrice"]) * discount) * platformFees
        product["monthData"][monthYear]["Profit"] += ((float(product["currentPrice"]) * discount) * platformFees) - \
                                                     float(product["purchasePrice"])

        product["monthData"][monthYear]["Margin"] = product["monthData"][monthYear]["Profit"] \
                                                    / product["monthData"][monthYear]["Revenue"]

        product["percentChangeFromPreviousMonth"][monthYear] = {
            "percentChangeTurnoverRate": (product["monthData"][monthYear]["turnoverRate"] - previousMonthDateData["turnoverRate"])/
            previousMonthDateData["turnoverRate"],
            "percentChangeProfit": (product["monthData"][monthYear]["Profit"] - previousMonthDateData["Profit"])/
            previousMonthDateData["Profit"],
            "percentChangeRevenue": (product["monthData"][monthYear]["Revenue"] - previousMonthDateData["Revenue"])/
            previousMonthDateData["Revenue"],
            "percentChangeMargin": (product["monthData"][monthYear]["Margin"] - previousMonthDateData["Margin"])/
            previousMonthDateData["Margin"]
          }

    product["lifetimeSalesDetails"]["Dates"][date] = {
        "priceAtSale": product["currentPrice"],
        "Discount": discount,
        "shippingCost": shippingCost,
        "Revenue": ((product["currentPrice"] * discount) * platformFees),
        "Platform": platform,
        "Profit": ((product["currentPrice"] * discount) * platformFees) - shippingCost - product["purchasePrice"],
    }

    return productsJSON