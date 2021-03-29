import time

from methods import *
from constants import *
from scholarly import scholarly, ProxyGenerator
from nordvpn_switcher import initialize_VPN, rotate_VPN, terminate_VPN

# set up VPN
initialize_VPN(save=1, area_input=['complete rotation'])

# rotate ip when needed
for i in range(3):
    rotate_VPN()
    # query google scholar
    search_query = scholarly.search_pubs(SEARCH_QUERY, patents=False, citations=False, year_low=2000, year_high=2021)
    saveQuery(search_query, PUBS_FILE)
    time.sleep(10)

# disconnect from VPN
terminate_VPN(instructions=None)

