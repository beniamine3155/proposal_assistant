# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time

# def scrape_website(url: str) -> str:
#     # Set up Selenium WebDriver with Chrome
#     options = Options()
#     options.headless = True  # Run in headless mode (no GUI)
#     service = Service(executable_path='path/to/chromedriver')  # Path to your chromedriver

#     # Initialize WebDriver
#     driver = webdriver.Chrome(service=service, options=options)
    
#     try:
#         driver.get(url)  # Open the webpage
#         time.sleep(3)  # Wait for content to load (adjust time as necessary)
        
#         # Extract the text content from all paragraph tags (<p>)
#         paragraphs = driver.find_elements(By.TAG_NAME, 'p')
#         text = ' '.join([p.text for p in paragraphs])

#         return text

#     except Exception as e:
#         print(f"Error during scraping: {e}")
#         return ""
#     finally:
#         driver.quit()  # Close the browser





import requests
from bs4 import BeautifulSoup

def scrape_website(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    else:
        return ""
