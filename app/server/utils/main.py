# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:20:15 2020

@author: sshobowale
"""

import ocr_generation
import data_extraction


def main():
    s3_prefix = 'WASSCE_JUNE/Physics_November_WASSCE/Physics_November_WASSCE_2011/'
    print("Detecting text from OCR..")
    try: 
        ocr_output = detect_raw_text(s3_prefix)
    except:
        ocr_output = ''
        print("Error detecting text from OCR!")
        
    print("Extracting data from OCR output..")
    
    print(ocr_output)
    try: 
        extract_data(ocr_output)
    except: 
        print("Error with text extraction")
    

if __name__ == "__main__":
    main()