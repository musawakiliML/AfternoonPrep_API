# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 01:41:45 2021

@author: sshobowale
"""

import requests
from bs4 import BeautifulSoup

base_url = "https://afternoonprep.com/user/test/exam"
available_subjects = ['accounts']
page = requests.get(base_url)

soup = BeautifulSoup(page.content, 'html.parser')

print(soup)
#print(page.content)
