import re

from selenium.webdriver.common.by import By

from parser.checks import coauthor_scraped

def citation_search(page):
    citations = page.find_all("a", 'gsc_a_ac gs_ibl')
    result = []

    for citation in citations:
        if citation.get_text()=="":
            result.append(0)

        else:
            result.append(int(citation.get_text()))

    return result

def coauthor_search(driver, scholar, coauthors, scholars, network, *, xpath="//h3[@class='gs_ai_name']/a", timeout=5):
    driver.implicitly_wait(timeout)

    for element in driver.find_elements(By.XPATH, xpath):
        coauthor_link = re.search("user=.{12}", element.get_attribute('href'))
        coauthor = re.sub("user=", '', coauthor_link.group(0))

        if coauthor_link is not None:

            if not coauthor_scraped(coauthor, scholars):
                print(f'add {coauthor} to coauthors set...') #for search level {level+2}...')
                coauthors.add(coauthor)# re.sub("user=", '', user_link.group(0)))

                network.append((scholar, coauthor))
