from methods import *
from constants import *

# scrape downloaded articles
handlePDF(PUBS_FILE)

print(f'Process completed. See {PUBS_FILE} for results.')