# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 02:14:59 2021

@author: sshobowale
"""

import time
from selenium import webdriver

driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
driver.get('https://afternoonprep.com/')
time.sleep(5)

element = driver.find_element_by_class_name('col-xs-12.col-sm-6')
select_element = Select(element)
select_element.select_by_index(1)
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
driver.quit()

