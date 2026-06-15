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
    def __init__(self, base_url):
        self.base_url = base_url
        self.source = "BooksToScrape_Selenium"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Run in headless mode
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
        try:
            self.driver.get(self.base_url)
            
            # Wait for products to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_pod")))
            
            # Simulate scrolling
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            articles = self.driver.find_elements(By.CLASS_NAME, "product_pod")
            
            for article in articles:
                try:
                    title_elem = article.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")
                    title = title_elem.get_attribute("title")
                    price = article.find_element(By.CLASS_NAME, "price_color").text
                    # Rating is in class attribute of the <p> tag
                    rating_elem = article.find_element(By.CSS_SELECTOR, "p[class^='star-rating']")
                    rating = rating_elem.get_attribute("class").split()[-1]
                    availability = article.find_element(By.CLASS_NAME, "instock").text.strip()
                    link = title_elem.get_attribute("href")
                    
                    books.append({
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "availability": availability,
                        "url": link,
                        "source": self.source
                    })
                except Exception as e:
                    logger.error(f"Error parsing book in Selenium: {e}")
            
            logger.info(f"Successfully scraped {len(books)} books from selenium source.")
        except Exception as e:
            logger.error(f"Selenium scraping failed: {e}")
        finally:
            self.driver.quit()
        
        return books
