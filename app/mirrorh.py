import logging
from database import insert_data
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_data_leaks():
    url = "https://mirror-h.org/"
    done = False  
    try:
        while not done:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info("200 OK")
                soup = BeautifulSoup(response.content, 'html.parser')
                datas = soup.select("table.table tbody tr")
                logger.info("Fetching data")

                for data in datas:
                    attacker = data.select_one('td:nth-child(1) a').text.strip()
                    country = data.select_one('td:nth-child(2)').text.strip()
                    url = data.select_one('td:nth-child(3) a').text.strip()
                    leak_url = data.select_one('td:nth-child(3) a').get('href')  
                    
                    ip = data.select_one('td:nth-child(4) a').text.strip()
                    date = data.select_one('td:nth-child(5)').text.strip()
                    leak_url = data.select_one('td:nth-child(3) a').get('href')  
                    if insert_data(attacker, country, url,ip, date, leak_url):
                        await save_iframe_html_with_timestamp(leak_url)

                done = True
            else:
                logger.warning("Request failed. Retrying after 10 seconds.")
                await asyncio.sleep(10)
    except Exception as e:
        logger.error("An error occurred: %s", e)

 
    logger.info("Data fetching completed. Will check again shortly.")


async def save_iframe_html_with_timestamp(leak_url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
     
        driver.get(leak_url)
        iframe_element = driver.find_element(By.CSS_SELECTOR, 'iframe')

        iframe_src = iframe_element.get_attribute('src')
   
        driver.get(iframe_src)
     
        iframe_html = driver.page_source
     
        soup = BeautifulSoup(iframe_html, 'html.parser')
        
        iframe_content = soup.find('html').prettify()  # Get the prettified HTML
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
      
        file_name = f"iframe_content_{timestamp}.html"
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(iframe_content)
        
        driver.quit()
        
        logger.info("HTML content of the iframe saved successfully with timestamp.")
    except Exception as e:
        logger.error("An error occurred while saving iframe HTML content with timestamp for URL %s: %s", leak_url, e)