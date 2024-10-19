import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

price_class = os.getenv("PRICE_CLASS")
product_name_class = os.getenv("PRODUCT_NAME_CLASS")


async def scrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        price = await scrape_price(soup)
        product_name = await scrape_name(soup)
        
        if price is None or product_name is None:
            raise ValueError("Failed to scrape price or product name from the response")
        
        return product_name, price
    except Exception as e:
        print(f"Error in scraping process: {e}")
        return None, None


async def scrape_price(soup):
    try:
        price_element = soup.find("div", {"class": price_class})
        if not price_element:
            raise ValueError(f"Price element with class '{price_class}' not found in the response")
        
        price = float(price_element.text.replace("₹", "").replace(",", "").strip())
        return price
    except Exception as e:
        print(f"Error scraping price: {str(e)}")
    return None


async def scrape_name(soup):
    try:
        name_element = soup.find("span", {"class": product_name_class})
        if not name_element:
            raise ValueError(f"Product name element with class '{product_name_class}' not found in the response")
        
        return name_element.text.strip()
    except Exception as e:
        print(f"Error scraping name: {str(e)}")
    return None
