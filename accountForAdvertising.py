from manageAccountingSheet import *


def accountForAdvertising():
    command = input("Enter sheet name followed by date, advertising amounts, and platforms. "
                    "For a range use - For example: \n"
                    "June2021.csv, 06/09/21 - 06/11/21, 10, Etsy, 06/01/21, 15$, "
                    "Shopify, 06/01/21-06/30/21, 13$, Facebook \n"
                    "Enter your data: ")
    etsyPlatformData, shopifyPlatformData, facebookPlatformData, accountingSheetName = parseCommand(command)
    accountingSheetData = openAccountingSheet(accountingSheetName)
    
    modifyAccountingSheetData(accountingSheetData, etsyPlatformData, 0)
    modifyAccountingSheetData(accountingSheetData, facebookPlatformData, 28)
    modifyAccountingSheetData(accountingSheetData, shopifyPlatformData, 14)
    writeToSheet(accountingSheetName, accountingSheetData)


def parseCommand(command):
    advertisingData = command.split(",")
    accountingSheetName = advertisingData.pop(0)
    platformsIndices = {}  # this variable finds teh index the platform is found at in the command
    # and stores it as index : platform

    for i in range(len(advertisingData)):
        # this loop goes through the product data array and then finds the
        # location of all the platform data so it can be split
        if advertisingData[i] == "Etsy" or advertisingData[i] == "Shopify" or advertisingData[i] == "Facebook":
            platformsIndices[i] = advertisingData[i]

    etsyData = []
    shopifyData = []
    facebookData = []
    # product data arrays
    prevIndex = 0
    for key in platformsIndices:
        if platformsIndices[key] == "Etsy":
            etsyData = advertisingData[prevIndex: key]
        elif platformsIndices[key] == "Shopify":
            shopifyData = advertisingData[prevIndex: key]
        elif platformsIndices[key] == "Facebook":
            facebookData = advertisingData[prevIndex: key]
        prevIndex = key + 1
    return etsyData, shopifyData, facebookData, accountingSheetName


def modifyAccountingSheetData(accountingSheetData, platformData, offset):
    dates = platformData[0].split("-")
    dateOne = int(dates[0].split("/")[1])
    dateTwo = int(dates[1 % len(dates)].split("/")[1])
    adspend = float(platformData[1][1:])
    
    accountingSheetData[7 + offset] = float(accountingSheetData[7 + offset])
    for i in range(dateOne, dateTwo + 1):
        accountingSheetData[14 + offset] = adspend
        accountingSheetData[7 + offset] += adspend
    