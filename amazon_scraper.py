from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_amazon_reviews(product_url, chrome_driver_path):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(product_url)

    reviews = []
    try:
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".review-text-content span"))
            )
            review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-text-content span")
            reviews.extend([review.text for review in review_elements])

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                if 'a-disabled' in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(2)
            except:
                break
    finally:
        driver.quit()
    return reviews
