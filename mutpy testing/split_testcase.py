import csv

file = open("mutpy_summary.csv", "r")

rows = csv.DictReader(file,  delimiter=',')

for row in rows:
    for col in row:
        print(col)