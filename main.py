import json
import csv
from updateProductdata import updateProductData

file_path = 'products.json'
with open(file_path, 'r') as file:
    products = json.load(file)


def updateProductsInventory(products, platformData):
    for i in range(0, len(platformData), 4):
        productID = platformData[i]
        productQuantity = platformData[i + 1]
        products[productID]["inventoryQuantity"] = int(products[productID]["inventoryQuantity"])
        productQuantity = int(productQuantity)
        products[productID]["inventoryQuantity"] -= productQuantity

    file_path = "products.json"
    with open(file_path, 'w') as file:
        # Step 3: Serialize data and write to the file using json.dump()
        json.dump(products, file)


def addDataToSheet(platformData, date, offset, platformFees, data):
    print("platform data is", platformData)
    for i in range(0, len(platformData), 4):
        productID = platformData[i]
        product = products[productID]
        productQuantity = int(platformData[i + 1])
        productDiscount = float(platformData[i + 2])
        productShippingCost = float(platformData[i + 3])
        # edit this entire section
        for j in range(1, 7):
            data[2][j + offset] = float(data[2][j + offset])
        data[2][1 + offset] += (product["currentPrice"] * (1 - productDiscount)) * platformFees # revenue
        data[2][1 + offset] += product["purchasePrice"] * (1 - productDiscount) + productShippingCost # cost total
        data[2][3 + offset] += productShippingCost
        data[2][4 + offset] += product["purchasePrice"] * (1 - productDiscount)
        data[2][5 + offset] = data[2][1 + offset] - data[2][1 + offset] # profit
        data[2][6 + offset] = round(data[2][5 + offset]  / data[2][1 + offset], 2) # margin
        # data[2][7] is total adspend
        # these bottom ones are for the date
        for j in range(8, 14):
            data[date + 1][j + offset] = float(data[2][j + offset])
        data[date + 1][8 + offset] += product["currentPrice"] * (1 - productDiscount) * platformFees # revenue
        data[date + 1][9 + offset] += product["purchasePrice"] * (1 - productDiscount) + productShippingCost # cost
        data[date + 1][10 + offset] += productShippingCost
        data[date + 1][11 + offset] += product["purchasePrice"] * (1 - productDiscount)
        data[date + 1][12 + offset] = data[date + 1][8 + offset] - data[date + 1][9 + offset]
        data[date + 1][13 + offset] = round(data[date + 1][12 + offset] / data[date + 1][8 + offset], 2) # margin
        # data[date + 1][14] is the days cost
        # TR, TC, TSC, TPC, TP, AM, TA, DR, DC, DSC, DPC, DP, DM, DA
        return data

def addDate(productDateData, data):
    """This function will take a command when invoked with the command -date.
    The input comes in the format of: mm/dd/yy, pr1, qty1, discount1, shippingcost1, ... ,
    prN, qtyN, discountN, shippingN, platform1, ... , platformN and is then split
    by an array by the previous function
    then it will parse all the data by taking the date, and storing it in data
    which is then used to index the spread sheet.
    then all the product data is parsed by splitting it up via platforms
    so all product data from pr1 - prN in a platform 1 is stored in a variable called
    platform1 for all platformsN
    after parsing the data the product information is passed to a separate function to
    write the data to the csv file.

    productDateData: array of all data.
    data is the array of the csv file.
    """
    print("prduct date data is", productDateData)
    print("data data is", data)
    print("in add date function")
    date = int(productDateData.pop(0).split('/')[1]) # this variable stores the date the entry occurred
    print("prduct date data is after removing first", productDateData)

    platformsIndices = {} # this variable finds teh index the platform is found at in the command
                         # and stores it as index : platform

    for i in range(len(productDateData)):
        # this loop goes through the product data array and then finds the
        # location of all the platform data so it can be split
        if productDateData[i] == "Etsy" or productDateData[i] == "Shopify" or productDateData[i] == "Facebook":
            platformsIndices[i] = productDateData[i]

    etsyData = []
    shopifyData = []
    facebookData = []
    # product data arrays
    prevIndex = 0
    for key in platformsIndices:
        if platformsIndices[key] == "Etsy":
            etsyData = productDateData[prevIndex: key]
        elif platformsIndices[key] == "Shopify":
            shopifyData = productDateData[prevIndex: key]

        elif platformsIndices[key] == "Facebook":
            facebookData = productDateData[prevIndex: key]
        prevIndex = key + 1

    print(etsyData, "etsy date")
    print(shopifyData, "shopify data")
    print(facebookData, "facebook data")
    addDataToSheet(etsyData, date, 0, 0.9325, data)
    addDataToSheet(shopifyData, date, 14, 0.95, data)
    addDataToSheet(facebookData, date, 28, 1, data)
    # this adds the data to the sheet.
    # using the add data function

    updateProductsInventory(products, etsyData)
    updateProductsInventory(products, shopifyData)
    updateProductsInventory(products, facebookData)

    # Step 3: Write the modified data back to the CSV file
    # finally this writes baack to the csv file
    with open('myData.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)



def editFile(fileName):
    data = []
    with open(fileName, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)

    productDateData = "06/07/23, pr1, 1, 0, 4, Etsy".replace(" ", "").split(",")

    addDate(productDateData, data)

    exitFunction = "N"
    while exitFunction != "Y":
        command = input("Enter commands to edit this file, use -advertising to add in any "
              "advertising costs and use -date to edit products for a particular"
              " date: ")
        if command == "-date":
            productDateData = input("Enter date, (mm/dd/yy format), pr1, qty1, discount1, shippingcost1, pr2, qty2, sale2, shippingcost2..., platform, "
                  "and repeat for any other platforms: ").replace(" ", "").split(",")

            addDate(productDateData, data)
        if command == "-advertising":
            advertisingData = input("Enter a date range or a single date (mm/dd/yy - mm/dd/yy or just mm/dd/yy), "
                                    "amount spent in the period, and platform and repeat for any other platforms:").replace(" ", "").split(",")
        exitFunction = input("is that all? (Y/N)")
        while exitFunction != "Y" and exitFunction != "N":
            if exitFunction != "Y" and exitFunction != "N":
                input("invalid command please enter again (Y/N)")


def main():
    editFile("myData.csv")
    command = input("Enter a command: ")
    if command == "editFile":
        filename = input("Enter the name of an existing CSV file to edit, or create a new one "
                         "by typing in YOURFILENAME.CSV: ")
    pass

if __name__ == "__main__":
    main()