import csv


data = []
with open("miscPurchases.csv", "r", newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        data.append(row)

total = 0
for i in range(1, len(data)):
    total += float(data[i][1])

print(total)