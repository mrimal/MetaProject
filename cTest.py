# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 11:39:34 2017

@author: mpr
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait as wait
#from selenium.webdriver.support import expected_conditions as EC
import os
from bs4 import BeautifulSoup
import config


chromedriver = config.cdriverPath
os.environ["webdriver.chrome.driver"] = chromedriver
driver =  webdriver.Chrome(chromedriver)
#driver = webdriver.Ie(iedriver)
driver.get(config.url)
wait(driver, 20)
html = driver.get_screenshot_as_png
html2 = driver.page_source
type(html2)
encodedHtml = html2.encode('ascii', 'ignore')
text_file = open("Output.txt", "w")
text_file.write("%s" % encodedHtml)
text_file.close()
soup = BeautifulSoup(html2)
print(soup) 

#continue_link = driver.find_element_by_link_text('Continue')
#print(continue_link)

'''
wait(driver, 10)
#wait.until(EC.alert_is_present())
#alert = driver.switch_to_alert()
#alert.authenticate


#wait(driver, 5).until(EC.alert_is_present())
#alert = driver.switch_to_alert()
#alert.accept()

assert "Ope" in driver.title
elem = driver.find_element_by_name("media-heading pull-left name-title")
elem.clear()
elem.send_keys("Mrijan")
elem.send_keys(Keys.RETURN)
assert "No results found" not in driver.page_source
assert "Operations" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("Mrijan")
elem.send_keys(Keys.RETURN)
assert "No results found" not in driver.page_source
'''
driver.close()    
