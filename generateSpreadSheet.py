from manageAccountingSheet import *


def generateAccountingSheet(path, month, year):
    data = []
    month = month.strip().lower()
    year = int(year.strip())
    generateHeaders(data)
    generateDates(data, month, year)
    fillZeroes(data)
    print(data)


def generateHeaders(accountingSheetData):

    accountingSheetData.append(['Platform', 'Etsy'])
    extendFourteen(accountingSheetData)
    accountingSheetData[0].append('Shopify')
    extendFourteen(accountingSheetData)
    accountingSheetData[0].append("Facebook")
    extendFourteen(accountingSheetData)
    accountingSheetData[0].append()
    extendFourteen(accountingSheetData)
    accountingSheetData[0].append("RestockOrdersOverhead", "", "OtherPurchases", "",
                                  "TotalRevenue", "TotalCost", "TotalProfit")

    accountingSheetData.append(['Dates'])
    generateKPIs(accountingSheetData, "Etsy")
    generateKPIs(accountingSheetData, "Shopify")
    generateKPIs(accountingSheetData, "Facebook")
    accountingSheetData.append("Shipping Cost", "Transaction Fees", "Purchase Name/Reason", "Purchase Total",0,0,0)


def extendFourteen(accountingSheetData):
    for i in range(13):
        accountingSheetData[0].append("")


def fillZeroes(accountingSheetData):
    for i in range(3, len(accountingSheetData)):
        for j in range(len(accountingSheetData[2])):
            accountingSheetData[i].append(0)


def generateDates(accountingSheetData, month, year):
    days = 0
    if month == "january" or month == "march" or \
        month == "may" or month == "july" or month == "august" or \
            month == "december":
        days = 31
    elif month == "april" or month == "june" or \
            month == "september" or month == "november":
        days = 30
    elif month == "february":
        if year % 4 == 0:
            days = 29
        else:
            days = 28
    else:
        print("invalid month entered, quitting")
        return

    for i in range(1, days + 1):
        accountingSheetData.append([f"{month}/{i}/{year}"])


def generateKPIs(accountingSheetData, platformName):
    accountingSheetData[1].append(f"Total Revenue (Minus {platformName} Fees)")
    accountingSheetData[1].append(f"Total Cost on {platformName}")
    accountingSheetData[1].append(f"Total Shipping Cost on {platformName}")
    accountingSheetData[1].append(f"Total Product Cost on {platformName}")
    accountingSheetData[1].append(f"Total Advertising Spend on {platformName}")
    accountingSheetData[1].append(f"Total Profit on {platformName}")
    accountingSheetData[1].append(f"Average Margin on {platformName}")
    accountingSheetData[1].append(f"Per Day Revenue (Minus {platformName} Fees)")
    accountingSheetData[1].append(f"Per Day Cost on {platformName}")
    accountingSheetData[1].append(f"Per Day Shipping Cost on {platformName}")
    accountingSheetData[1].append(f"Per Day Product Cost on {platformName}")
    accountingSheetData[1].append(f"Per Day Advertising Spend on {platformName}")
    accountingSheetData[1].append(f"Per Day Profit on {platformName}")
    accountingSheetData[1].append(f"Per Day Margin on {platformName}")
