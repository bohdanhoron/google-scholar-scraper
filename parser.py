import os
import time
import logging
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def citation_search(page):
    citations = page.find_all("a", 'gsc_a_ac gs_ibl')
    result = []

    for citation in citations:
        if citation.get_text()=="":
            result.append(0)

        else:
            result.append(int(citation.get_text()))

    return result

def save_citations(scholar, citations):
    with open(f"{os.getcwd()}/data/{scholar}.csv", "w") as file:
        for cit in citations:
            file.write(f"{cit}\n")

def save_network(network):
    with open(f"{os.getcwd()}/data/network.dat", "w") as file:
        for pair in network:
            file.write(f"{pair[0]} {pair[1]}\n")

def clicking_on_button_more(*, button_id="gsc_bpf_more"):
    more_button = driver.find_element(By.XPATH, f"//button[@id='{button_id}']")
    
    while more_button.is_enabled():
        more_button.click()
        
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@id='button_id']")))
        except TimeoutException:
            print(f"element is not clickable. proceeding to next phase of program execution")

def check_existance_coauthors_button(*, button_id='gsc_coauth_opn'):
    try:
        coauthors_button = driver.find_element(By.XPATH, f"//button[@id='{button_id}']")
        return True
    except NoSuchElementException:
        return False

def logging_config():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='gs-parser.log', level=logging.INFO)

def scholar_loop(scholar, coauthors):
    print(f"getting {domain_name}{prefix}{scholar}")
    driver.get(f"{domain_name}{prefix}{scholar}")

    clicking_on_button_more()

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

    coauthors_button_exists = check_existance_coauthors_button()

    if coauthors_button_exists:
        
        coauthors_button = driver.find_element(By.XPATH, "//button[@id='gsc_coauth_opn']")

        coauthors_button.click()

        driver.implicitly_wait(5)

        for element in driver.find_elements(By.XPATH, "//h3[@class='gs_ai_name']/a"):
            coauthor_link = re.search("user=.{12}", element.get_attribute('href'))
            coauthor = re.sub("user=", '', coauthor_link.group(0))
            coauthor_already_exists = False

            if coauthor_link is not None:
                for i in range(len(scholars)):
                    if coauthor in scholars[i]:
                        print(f'user {coauthor} already exists in set on level {i}')
                        coauthor_already_exists = True
                        break

                if not coauthor_already_exists:
                    print(f'add {coauthor} to coauthors set...') #for search level {level+2}...')
                    coauthors.add(coauthor)# re.sub("user=", '', user_link.group(0)))

                    network.append((scholar, coauthor))

    else:
        print("this page does not have co-authors list")

def main(*, search_deepness=1):
    for level in range(search_deepness):
        print(f'START: starting LEVEL {level+1}')
        print(f'size of the level in number of authors is: {len(scholars[level])}')

        coauthors = set()

        for scholar in scholars[level]:
            scholar_loop(scholar, coauthors)

        print('appending coauthors')
        scholars.append(coauthors)

    save_network(network)


if __name__=="__main__":
    domain_name = "https://scholar.google.com/"
    prefix = "citations?user="
    initial_user_name = "sIhCXI4AAAAj"
    user_names = {initial_user_name}

    options = webdriver.chrome.options.Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, timeout=5, poll_frequency=0.5)

    network = []

    scholars = []
    
    scholars.append(user_names)

    main(search_deepness=1)
