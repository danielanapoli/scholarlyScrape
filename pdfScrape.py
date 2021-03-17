from methods import *
from constants import *

# scrape downloaded articles
print('Scraping corresponding article data...')
handlePDF(PUBS_FILE)

print(f'Process completed. See {PUBS_FILE} for results.')