import csv
import os
import PyPDF2
import pandas

from scholarly import scholarly
from constants import *

# generate a tag per publication containing name of first author + year + first 10 chars of title
def genTag(authors, year, title):
    return(year + '_' + authors[0].replace(' ', '') + '_' + title[0:9].replace(' ', '')) 

# create a .csv file containing selected data from google scholar queries 
def saveQuery(search_query, file):
    n = 0
    pub = (next(search_query))
    with open(file, 'w', encoding='utf-8') as pubsFile:
        w = csv.writer(pubsFile)
        w.writerow(["Tag", "Author", "Year", "Title", "URL", "Excerpt"])
        while(next(search_query)):
            n += 1
            w.writerow([genTag(pub["bib"]["author"], pub["bib"]["pub_year"], pub["bib"]["title"]), 
                        pub["bib"]["author"], pub["bib"]["pub_year"], pub["bib"]["title"], pub["pub_url"], 'N/A'])
            pub = (next(search_query))
        print(f'Saved data from {n} scraped publications on Google scholar.')
    pubsFile.close()

# pass each tag identifier from the .csv to the extraction function
def handlePDF(file):
    n = 0
    pubs = pandas.read_csv(file)
    for tag in pubs.Tag:
        n += extractData(tag)
    print(f'Extracted and appended data from {n} PDFs.')

# extract first page (or first 4000 chars) from a PDF file        
def extractData(file):
    pageNum = 0
    pdfObj = open(DIR_PATH + '/' + file + '.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(pdfObj)
    extractedFromPDF = (reader.getPage(pageNum).extractText())
    while (len(extractedFromPDF) < 4000):
        if (pageNum == reader.getNumPages()-1): #avoid retrieving data beyond the last page
            break
        pageNum += 1
        extractedFromPDF += (' ' + reader.getPage(pageNum).extractText())
        updatePubs(extractedFromPDF, file)
        return 1

# append extracted data to corresponding publication rows based on tag; overwrite .csv file with updated dataframe 
def updatePubs(excerpt, tag):
    pubs = pandas.read_csv(PUBS_FILE)
    pubs = pubs.set_index('Tag')
    pubs.at[tag, 'Excerpt'] = excerpt
    pubs.to_csv(PUBS_FILE, index=False)