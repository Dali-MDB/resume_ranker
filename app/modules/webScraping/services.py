from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebScrapingService:
    def __init__(self):
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def _force_english(self, url: str) -> str:
        if "?" in url:
            return url + "&language=en_US"
        return url + "?language=en_US"

    def scrape_job(self, url: str) -> str | None:
        if "linkedin.com" in url:
            return self.scrape_linkedin(url)
        if "indeed.com" in url:
            return self.scrape_indeed(url)
        raise ValueError(f"Unsupported job URL: {url}")

    def scrape_linkedin(self, url: str) -> str:
        url = self._force_english(url)
        self.driver.get(url)

        try:
            btns = self.driver.find_elements(
                By.XPATH,
                '//button[contains(@data-tracking-control-name, "modal_dismiss")]',
            )
            if btns:
                self.driver.execute_script("arguments[0].click();", btns[0])
            else:
                self.driver.execute_script("document.elementFromPoint(100, 100).click();")
        except Exception:
            pass

        try:
            show_more = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@aria-label, "Show more")]')
                )
            )
            self.driver.execute_script("arguments[0].click();", show_more)
        except Exception:
            pass

        description = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "description__text"))
        )
        return description.text

    def scrape_indeed(self, url: str) -> str | None:
        url = self._force_english(url)
        self.driver.get(url)

        try:
            popups = self.driver.find_elements(
                By.XPATH,
                '//button[contains(@aria-label, "close") or contains(@class, "icl-CloseButton")]',
            )
            if popups:
                self.driver.execute_script("arguments[0].click();", popups[0])
        except Exception:
            pass

        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            job_text = self.driver.execute_script("return arguments[0].innerText;", element)
            return "\n".join(
                line.strip() for line in job_text.split("\n") if line.strip()
            )
        except Exception:
            return None

    def close(self):
        self.driver.quit()
