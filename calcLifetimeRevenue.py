import json

file_path = "Data/allProductData/products.json"
with open(file_path, 'r') as file:
    products = json.load(file)

totalLifetimeRevenue = 0
for key in products:
    for order in products[key]["lifetimeSalesDetails"]["Dates"]:
        totalLifetimeRevenue += float(products[key]["lifetimeSalesDetails"]["Dates"][order]["actualRevenue"])

print(totalLifetimeRevenue)
