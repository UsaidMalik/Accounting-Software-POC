from manageAccountingSheet import *


def addPurchase():
    purchaseInformation = input("Enter purchase information: Date, Purchase Name/Explanation, Purchase Cost, example, "
                                "Bubble Wrap 25pcs, 10, Date2, PurchaseName2, Purchase Cost2.... ")
    datesPurchasesInformation = parseInformation(purchaseInformation)
    accountingSheetName = input("Enter the name of the accounting sheet you want to add these purchases to: ")
    accountingSheet = openAccountingSheet(accountingSheetName)

    for key in datesPurchasesInformation:
        date = datesPurchasesInformation[key][0]
        if len(accountingSheet[date]) < 47:
            for i in range(47 - len(accountingSheet[date])):
                accountingSheet[date].append(0)
        # preprocessing data
        accountingSheet[date][45] = key
        accountingSheet[date][46] = datesPurchasesInformation[key][1]

        accountingSheet[2][49] = float(accountingSheet[2][49])
        accountingSheet[2][48] = float(accountingSheet[2][48])

        accountingSheet[2][49] -= datesPurchasesInformation[key][1]
        accountingSheet[2][48] += datesPurchasesInformation[key][1]

    writeToAccountingSheet(accountingSheet, accountingSheetName)


def parseInformation(purchaseInformation):
    purchaseInformation.split(",")
    datesPurchasesInformation = {}
    for i in range(len(purchaseInformation), 3):
        datesPurchasesInformation[purchaseInformation[i + 1]] = [int(purchaseInformation[i].split("/")[1]),
                                                                 float(purchaseInformation[i + 2])]
    return purchaseInformation
