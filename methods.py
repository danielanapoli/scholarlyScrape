import sys
import csv
import os
import PyPDF2
import pdfplumber
import pandas
import time
import uuid

from scholarly import scholarly
from constants import *

# generate a tag per publication based query + a randomly generated UUID
def genTag(pub):
    u = uuid.uuid1()
    u = str(u)
    return(pub["bib"]["pub_year"] + '_' + u[0:6]) 

# create a .csv file containing selected data from google scholar queries 
def saveQuery(search_query, file):
    print('Scraping search queries...')
    n = 0
    pub = (next(search_query))
    with open(file, 'w', encoding='utf-8') as pubsFile:
        w = csv.writer(pubsFile)
        w.writerow(["Tag", "Author", "Year", "Title", "Venue", "URL", "GS_Rank", "Citations", "PDF_Available", "Excerpt"])
        while(next(search_query)):
            n += 1
            w.writerow([genTag(pub), #Output from genTag()
                        pub["bib"]["author"], pub["bib"]["pub_year"], pub["bib"]["title"], pub["bib"]["venue"], #Data in bib object
                        pub["pub_url"], pub["gsrank"], pub["num_citations"], #Data not in bib object
                        False, 'N/A']) #Placeholders which will change after running PDFscrape.py
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

# using PythonPDF 
# extract first page (or first 4000 chars) from the article's PDF file       
def extractData(tag):
    pageNum = 0
    filePath = (DIR_PATH + '/' + tag + '.pdf')
    if (os.path.exists(filePath)): #check if a file with the tag exists
        pdfObj = open(filePath, 'rb')
        reader = PyPDF2.PdfFileReader(pdfObj)
        extractedFromPDF = (reader.getPage(pageNum).extractText())
        while (len(extractedFromPDF) < 4000):
            if (pageNum == reader.getNumPages()-1): #avoid retrieving data beyond the last page
                return 0
            extractedFromPDF += (' ' + reader.getPage(pageNum).extractText())
            pageNum += 1
        updatePubs(extractedFromPDF, tag)
        return 1      
    else:
        return 0

# append extracted data to corresponding publication rows based on tag; overwrite .csv file with updated dataframe 
def updatePubs(excerpt, article):
    pubs = pandas.read_csv(PUBS_FILE)
    pubs = pubs.set_index('Tag', inplace = False) 
    pubs.loc[article, 'PDF_Available'] = True
    pubs.loc[article, 'Excerpt'] = excerpt
    pubs.to_csv(PUBS_FILE)