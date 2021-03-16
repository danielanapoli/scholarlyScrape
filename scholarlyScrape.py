from scholarly import scholarly, ProxyGenerator
from methods import *
from constants import *

# get proxy going
#TODO: sub out Luminati proxy for other VPN service
pg = ProxyGenerator()
pg.Luminati(usr=os.getenv("USERNAME"), passwd=os.getenv("PASSWORD"), proxy_port=os.getenv("PORT"))
scholarly.use_proxy(pg)

# query google scholar
search_query = scholarly.search_pubs(SEARCH_QUERY, patents=False, citations=False, year_low=2000, year_high=2021)

#store results in .csv file
print(f'Scraping search queries...')
saveQuery(search_query, PUBS_FILE)

# scrape downloaded PDFs for relevancy grading data
if (PDF_SCRAPE):
    print(f'Scraping corresponding PDF data...')
    handlePDF(PUBS_FILE)
else:
    print(f'PDF scraping not enabled.')

print(f'Process completed. See {PUBS_FILE} for results.')