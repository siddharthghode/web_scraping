from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

logger = logging.getLogger(__name__)

class SeleniumScraper:
    def __init__(self, site_config):
        self.base_url = site_config["url"]
        self.source = site_config["name"]
        self.selectors = site_config["selectors"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            logger.info("Selenium WebDriver initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium WebDriver: {e}")
            self.driver = None

    def scrape_books(self):
        if not self.driver:
            return []

        logger.info(f"Starting selenium scrape on {self.base_url}")
        books = []
        s = self.selectors
        try:
            self.driver.get(self.base_url)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, s["book_container"])))

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            articles = self.driver.find_elements(By.CSS_SELECTOR, s["book_container"])

            for article in articles:
                try:
                    title_el = article.find_element(By.CSS_SELECTOR, s["title"])
                    title = title_el.get_attribute("title") or title_el.text.strip()
                    price_el = article.find_element(By.CSS_SELECTOR, s["price"])
                    rating_el = article.find_element(By.CSS_SELECTOR, s["rating"])
                    avail_el = article.find_element(By.CSS_SELECTOR, s["availability"])
                    link_el = article.find_element(By.CSS_SELECTOR, s["link"])

                    books.append({
                        "title": title,
                        "price": price_el.text.strip(),
                        "rating": rating_el.get_attribute("class").split()[-1],
                        "availability": avail_el.text.strip(),
                        "url": link_el.get_attribute("href"),
                        "source": self.source
                    })
                except Exception as e:
                    logger.error(f"Error parsing book in Selenium: {e}")

            logger.info(f"Scraped {len(books)} books from {self.source}.")
        except Exception as e:
            logger.error(f"Selenium scraping failed: {e}")
        finally:
            self.driver.quit()

        return books
