import pandas

df2 = pandas.DataFrame
pubs = pandas.read_csv('scraped_data\pubs.csv')
print(pubs.to_dict())

