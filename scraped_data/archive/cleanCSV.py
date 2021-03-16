import csv
import pandas

data = []

with open('data.csv', 'r') as inFile:
    for row in inFile:
        if (row != '\n'):
            row = row.replace(',', '')
            data.append(row.strip())

df = pandas.DataFrame(data)
df.to_csv(r'data copy.csv')