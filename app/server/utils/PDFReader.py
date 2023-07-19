# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 08:21:30 2020

@author: sshobowale
"""
#!/bin/python
import PyPDF2


pdfFileObj = open('Job Application Form_FILLEDDD3.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

print(pdfReader.numPages) 

for page in range(pdfReader.numPages):    
    pageObj = pdfReader.getPage(page) 
    print(pageObj.extractText()) 

pdfFileObj.close() 