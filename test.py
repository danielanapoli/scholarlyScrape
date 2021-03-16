#index = pubs.index[pubs['Tag']=='2000_UJendricke_Usability']
#print(pubs.loc[index])
 
import pandas

pubs = pandas.read_csv('scraped_data\pubs.csv')
tag = '2000_UJendricke_Usability'
excerpt = 'Hello there!'




print(pubs)



