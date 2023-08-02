import json


def openProductsDataJSON():
    file_path = 'products.json'
    with open(file_path, 'r') as file:
        products = json.load(file)
    return products


def writeProductsToFile(products):
    file_path = 'products.json'
    with open(file_path, 'w') as json_file:
        json.dump(products, json_file, indent=4)
    print("Finished Adding Product")
