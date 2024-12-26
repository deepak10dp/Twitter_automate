from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import time
import sys

load_dotenv()

class TwitterScraper:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.mongo_client['twitter_trends']
        self.collection = self.db['trends']
        self.username = os.getenv('TWITTER_USERNAME').replace('@', '')  # Remove @ if present
        self.password = os.getenv('TWITTER_PASSWORD')
        
    def setup_driver(self, proxy=None):
        chrome_options = Options()
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        # Basic options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Create and return the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver

    def login_twitter(self, driver):
        try:
            print("Logging in to Twitter...")
            driver.get('https://x.com/login')
            time.sleep(3)

            # Enter username
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_input.send_keys(self.username)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Enter password
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)

            return True
        except Exception as e:
            print(f"Error in login: {str(e)}")
            return False

    def get_trending_topics(self, proxy=None):
        driver = None
        try:
            driver = self.setup_driver(proxy)
            if not self.login_twitter(driver):
                return None

            print("Navigating to home page...")
            driver.get('https://x.com/home')
            time.sleep(5)
            
            print("Looking for trending section...")
            try:
                # Find all trend elements
                trend_elements = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((
                        By.CSS_SELECTOR, 
                        'div[data-testid="trend"] div[style*="color: rgb(231, 233, 234)"] span'
                    ))
                )
                
                print(f"Found {len(trend_elements)} trend elements")
                
                # Get text from trends
                trend_texts = []
                for element in trend_elements:
                    try:
                        text = element.text.strip()
                        if text:
                            print(f"Found trend: {text}")
                            trend_texts.append(text)
                    except Exception as e:
                        print(f"Error getting trend text: {str(e)}")
                        continue

                # Take first 5 trends
                trend_texts = trend_texts[:5]
                
                # Ensure we have exactly 5 trends
                while len(trend_texts) < 5:
                    trend_texts.append("")
                
                print(f"Final trends: {trend_texts}")
                
                record = {
                    "_id": str(uuid.uuid4()),
                    "nameoftrend1": trend_texts[0],
                    "nameoftrend2": trend_texts[1],
                    "nameoftrend3": trend_texts[2],
                    "nameoftrend4": trend_texts[3],
                    "nameoftrend5": trend_texts[4],
                    "datetime": datetime.now().isoformat(),
                    "ip_address": proxy if proxy else "direct"
                }
                
                self.collection.insert_one(record)
                print("Successfully saved trends to database!")
                return record
                
            except Exception as e:
                print(f"Error in trends extraction: {str(e)}")
                if driver:
                    driver.save_screenshot("error_screenshot.png")
                    print("Saved error screenshot")
                return None
            
        except Exception as e:
            print(f"Error: {str(e)}")
            if driver:
                driver.save_screenshot("error_screenshot.png")
                print("Saved error screenshot")
            return None
        finally:
            if driver:
                driver.quit()

    def get_latest_record(self):
        return self.collection.find_one(sort=[('datetime', -1)])
