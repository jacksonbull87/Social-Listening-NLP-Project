from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path=chrome_path)
driver.get('https://twitter.com/login')

user_input = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input')
password_input = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input')
login_button = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/form/div/div[3]/div/div/span/span')
user_input.send_keys("jacksonabull")
password_input.send_keys("Brooklyn6$")
login_button.click()