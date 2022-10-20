import csv

def writecsv(row_list, filepath):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)