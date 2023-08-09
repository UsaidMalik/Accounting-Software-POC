import csv


def openAccountingSheet(accountingSheetName):
    data = []
    with open(accountingSheetName, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data


def writeToSheet(accountingSheetName, data):
    with open(accountingSheetName, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)
