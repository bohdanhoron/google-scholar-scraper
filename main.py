from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from parser.buttons import click_more
from parser.io import save_network
from parser.loops import scholar_loop

def main(*, search_deepness=1):

    options = webdriver.chrome.options.Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, timeout=5, poll_frequency=0.5)

    initial_user_name = "sIhCXI4AAAAj"
    user_names = {initial_user_name}
    
    network = []

    scholars = [user_names,]

    for level in range(search_deepness):
        print(f'START: starting LEVEL {level+1}')
        print(f'size of the level in number of authors is: {len(scholars[level])}')

        coauthors = set()

        for scholar in scholars[level]:
            print(f"getting https://scholar.google.com/citations?user={scholar}")
            driver.get(f"https://scholar.google.com/citations?user={scholar}")
            click_more(driver, wait)
            
            scholar_loop(scholar, coauthors, scholars, network, driver, wait)

        print('appending coauthors')
        scholars.append(coauthors)

    save_network(network)


if __name__=="__main__":
    main(search_deepness=1)
