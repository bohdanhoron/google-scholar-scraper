from bs4 import BeautifulSoup

from .buttons import click_more, click_coauthors, coauthors_exist
from .searches import citation_search, coauthor_search
from .io import save_citations

def scholar_loop(scholar,
                 coauthors,
                 scholars,
                 network,
                 driver,
                 wait):

    page = BeautifulSoup(driver.page_source, 'html.parser')

    #### CITATIONS SEARCH ##########

    print("CITATIONS SEARCH")
    print("looking for citations...")
    
    result = citation_search(page)

    print(f"we found {sum(result)} citations.")
    print(f"writing citations to {scholar}.csv...")

    save_citations(scholar, result)

    print("writing to file is DONE.")
    
    ### CO-AUTHORS SEARCH ###

    print("CO-AUTHORS SEARCH")
    print("looking for co-authors...")

    if coauthors_exist(driver):
        
        click_coauthors(driver)

        coauthor_search(driver, scholar, coauthors, scholars, network)

    else:
        print("this page does not have co-authors list")
