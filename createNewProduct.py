import json


def createProduct():
    productsJSON = openProductsDataJSON()


def openProductsDataJSON():
    file_path = 'products.json'
    with open(file_path, 'r') as file:
        products = json.load(file)
    return products
