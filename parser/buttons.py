from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def click_more(driver, wait, *, button_id="gsc_bpf_more"):
    more_button = driver.find_element(By.XPATH, f"//button[@id='{button_id}']")
    # wait = WebDriverWait(driver, timeout=5, poll_frequency=0.5)
    
    while more_button.is_enabled():
        more_button.click()
        
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@id='button_id']")))
        except TimeoutException:
            print(f"element is not clickable. proceeding to next phase of program execution")

def click_coauthors(driver, *, button_id="gsc_coauth_opn"):
    coauthors_button = driver.find_element(By.XPATH, f"//button[@id='{button_id}']")

    coauthors_button.click()

# def check_existance_coauthors_button(*, button_id='gsc_coauth_opn'):
def coauthors_exist(driver, *, button_id='gsc_coauth_opn'):
    try:
        coauthors_button = driver.find_element(By.XPATH, f"//button[@id='{button_id}']")
        return True
    except NoSuchElementException:
        return False
