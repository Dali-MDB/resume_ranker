from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

import os
from pathlib import Path

UTILS_DIR = Path(__file__).parent


options = Options()
options.add_argument('--log-level=3')  
#options.add_argument("--headless=new") 
options.add_argument('--disable-gpu')  # Optional on Windows
options.add_argument('--window-size=1920,1080')  # Needed by some sites
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)
wait = WebDriverWait(driver, 10)


def force_english(url):
    if "?" in url:
        return url + "&language=en_US"
    else:
        return url + "?language=en_US"

def scrape_linkedin(driver: webdriver, url:str):
    # Force English via URL parameter
    url = force_english(url)
        
    driver.get(url)
    wait = WebDriverWait(driver, 10)

  
    try:
        btns = driver.find_elements(By.XPATH, '//button[contains(@data-tracking-control-name, "modal_dismiss")]')

        #If the list isn't empty, force click the first element
        if btns:
            driver.execute_script("arguments[0].click();", btns[0])
            print("Force clicked the X.")
        else:
            #click randomly on the screen
            driver.execute_script("document.elementFromPoint(100, 100).click();")
            print("Clicked screen at (100, 100).")
    except:
        print("No modal found, moving on...")

    #click show more if applicable
    try:
        show_more = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Show more")]')))
        driver.execute_script("arguments[0].click();", show_more) # JS click is more reliable
    except Exception as e:
        print(f"Could not click show more: {e}")

    #scrape job description

    description = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "description__text")))
    print(description.text)
    return description.text


def scrape_indeed(driver: webdriver, url:str):
    # Force English
    url = force_english(url)
        
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Indeed often has a popup for 'Post your resume' or 'Sign in'
    try:
        # Look for the close "X" on common popups
        popups = driver.find_elements(By.XPATH, '//button[contains(@aria-label, "close") or contains(@class, "icl-CloseButton")]')
        if popups:
            driver.execute_script("arguments[0].click();", popups[0])
            print("Indeed popup dismissed.")
    except:
        pass

    # Indeed job descriptions are usually inside a specific ID
    try:
        element = wait.until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
        # hidden/dynamic divs
        job_text = driver.execute_script("return arguments[0].innerText;", element)
        clean_text = "\n".join([line.strip() for line in job_text.split('\n') if line.strip()])
        
        print("Success! Scraped Indeed Description.")
        return clean_text
        
    except Exception as e:
        print(f"Indeed scrape failed: {e}")
        return None


