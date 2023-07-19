# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 21:28:03 2021

@author: sshobowale
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome('C:\Python36\chromedriver.exe')


login_url = "https://afternoonprep.com/user/login"
admin_url = "https://afternoonprep.com/admin/questions"

driver.get(login_url)

login_form = driver.find_element_by_xpath("//form[1]")

username = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='login']/form/section/div[@class='input-field'][1]/input[@type='email']")
password = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='login']/form/section/div[@class='input-field'][2]/input[@type='password']")
login_button = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='login']/form/section/button[@class='button']")

username.send_keys("samboske93@yahoo.com")
password.send_keys("ilmwies'")
login_button.click()
time.sleep(3)


#driver.get(admin_url)
expand_menu = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/main/header/span[@class='mdi mdi-menu menu-icon sidenav-trigger']")
admin_toggle = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/section[@class='sidenav']/div[@class='switch admin-switch']/label/span[@class='lever']")  

expand_menu.click()
time.sleep(1)
admin_toggle.click()



edit_questions = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/section[@class='sidenav']/ul/li[3]/a")



edit_questions.click()
time.sleep(3)


upload_options_button = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/main/section/div[@class='fixed-action-btn direction-top']/button[@class='btn-floating btn-large manage-questions-fab']")
upload_json = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/main/section/div[@class='fixed-action-btn direction-top']/ul/li[1]/button[@class='btn-floating uploadJSON-fab tooltipped modal-trigger']")

hover = ActionChains(driver).move_to_element(upload_options_button)
try:
    hover.perform()
    time.sleep(2)
    
    #upload_options_button.click()
    upload_json.click()
except:
    hover.perform()
    time.sleep(5)
    
    #upload_options_button.click()
    upload_json.click()


select_file_button = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/div[@id='add-exam-modal']/div[@class='modal-content']/form/div[@class='file-field input-field']/div[@class='button select-file']/input")
upload_button = driver.find_element_by_xpath("/html/body/div[@id='root']/section[@class='dashboard']/div[@id='add-exam-modal']/div[@class='modal-content']/form/div[@class='button-container']/button[@class='button']")

file_path = ["C:/Users/sshobowale/Documents/Scripts/afternoon-prep/raw_outputs/MAY-JUNE/output_WASSCE_JUNE_2010_Christian_Religious_Studies.json", "C:/Users/sshobowale/Documents/Scripts/afternoon-prep/raw_outputs/MAY-JUNE/output_WASSCE_June_2010_Economics.json"]

for file in file_path:
    select_file_button.send_keys(file)
    upload_button.click()
    print(file)
    time.sleep(2)
    
    
print(login_form)
print(username)
print(password)
