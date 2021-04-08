import sys
import csv
import os
import PyPDF2
import pandas
import time
import uuid

from scholarly import scholarly
from constants import *

# generate a tag per publication based on some portion of the query metadata + first portion of a randomly generated UUID
def genTag(authors, year, title):
    u = uuid.uuid1()
    u = str(u)
    return(year + authors[0][0] + title[0] + '_' + u[0:6]) 

# create a .csv file containing selected data from google scholar queries 
def saveQuery(search_query, file):
    print('Scraping search queries...')
    n = 0
    pub = (next(search_query))
    with open(file, 'w', encoding='utf-8') as pubsFile:
        w = csv.writer(pubsFile)
        w.writerow(["Tag", "Author", "Year", "Title", "Venue", "URL", "GS_Rank", "Citations", "Excerpt"])
        while(next(search_query)):
            n += 1
            w.writerow([genTag(pub["bib"]["author"], pub["bib"]["pub_year"], pub["bib"]["title"]), #Output from genTag()
                        pub["bib"]["author"], pub["bib"]["pub_year"], pub["bib"]["title"], pub["bib"]["venue"], #Data in bib object
                        pub["pub_url"], pub["gsrank"], pub["num_citations"], #Data not in bib object
                        'N/A']) #Placeholder for excerpt that will be populated after running PDFscrape.py
            time.sleep(2) #Buffer time before next call so we can get more entries
            pub = (next(search_query))
            if (n == 500):
                break
        print(f'Saved data from {n} scraped publications on Google scholar.')
    pubsFile.close()

# pass each tag identifier from the .csv to the extraction function
def handlePDF(file):
    print('Scraping article data...')
    n = 0
    pubs = pandas.read_csv(file)
    for tag in pubs.Tag:
        #n += 
        extractData(tag)
    print(f'Extracted and appended data from {n} PDFs.')

# extract first page (or first 4000 chars) from a PDF file   
# NOTE: file must exist, no error handling implemented      
def extractData(file):
    pageNum = 0
    pdfObj = open(DIR_PATH + '/' + file + '.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(pdfObj)
    extractedFromPDF = (reader.getPage(pageNum).extractText())
    while (len(extractedFromPDF) < 4000):
        if (pageNum == reader.getNumPages()-1): #avoid retrieving data beyond the last page
            return 0
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