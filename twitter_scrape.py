from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from twitter_config import credentials
import time  
import pandas as pd

#set path for chromedriver extension
chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path=chrome_path)
driver.get('https://twitter.com/explore')
driver.implicitly_wait(60)

#click on search icon
search_input = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div/form/div[1]/div/div/div[2]/input')
search_input.send_keys('#brooklyn')
search_input.submit()
time.sleep(3)
#click on the latest to start collecting the most recent tweets
latest_btn = driver.find_element_by_xpath("//div[@class='css-1dbjc4n r-16y2uox r-6b64d0'][2]")
latest_btn.click()
#empty list to add tweets to
data_bucket = []
#counter to keep track of how many tweets I've collected
counter = 0

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    tweets = driver.find_elements_by_xpath("//div[@class='css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll']")
    for tweet in tweets:
        try:
            username = tweet.find_element_by_xpath("//div[@class='css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd']").text
            text = tweet.text
            tweet_tuple = (username, text)
            data_bucket.append(tweet_tuple)
            counter += 1
            print(counter)
        except (StaleElementReferenceException, NoSuchElementException) as Exception:
            continue
        
    driver.execute_script("window.scrollTo(0, {})".format(last_height+500))
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        break
df = pd.DataFrame(data_bucket, columns=['username', 'tweet'])
df



