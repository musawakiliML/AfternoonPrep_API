
"""
Created on Sat May 30 19:48:50 2020
OCR collection from Amazon textract and sent to S3

@author: samuel shobowale
"""

#!/bin/python3

import re
import os
import json
import boto3
import urllib
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Removes strange characters returned from OCR output, these characters are not suitable for proper regex search in... 
#...future regex functions

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9_,'`:;%=$^<>!/\"\?\.\-\+\(\)\[\]\{\}\*\s]", '', text)

def atoi(text):
    return int(text) if text.isdigit() else text

# To be able to sort the files in S3 alphanumerically
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def check_choice_regex(line):
    regexp = {
            'single_char': re.compile(r'^[A-D]$'), #regex for single line with single character A, B, C., or D
            'space_char': re.compile(r'^[A-D][\s][\w]'), #regex for single line with space between character A, B, C., or D and rest of words
            'colon_char': re.compile(r'^[A-D]:'), #regex for choices that come like C:, D:
            'comma_char': re.compile(r'^[A-D],'), #regex for choices that come like C, or B,
            'typical': re.compile(r'^[A-D][\.]') #regex for each choice
            }
        
    for key, pattern in regexp.items():
        m = pattern.findall(line)
        if m: 
            return m
            break

        

    #return
        

def detect_raw_text(s3_prefix):
    access_key = os.environ["AWS_ACCESS_KEY"]   #insert AWS Access key
    secret_access_key = os.environ["AWS_SECRET_KEY"]   #insert AWS secret access key
    region = 'us-east-1'
    
    question_number_regex = re.compile(r'^\d{1,2}')
    choice_regex = re.compile(r'^[A-D][,\.\n\s\r]?') #regex for each choice
    choice_regex_single = re.compile(r'^[A-D]$') #regex for single line with single character A, B, C., or D
    choice_regex_space = re.compile(r'^[A-D][\s][\w]') #regex for single line with space between character A, B, C., or D and rest of words
    
    #file = open("textract_output.json", "w")
    
    textract_client = boto3.client('textract',
                                   aws_access_key_id = access_key,
                                   aws_secret_access_key = secret_access_key,
                                   region_name = region
    
                                   )    
    s3_client = boto3.client('s3',
                             aws_access_key_id = access_key,
                             aws_secret_access_key = secret_access_key,
                             region_name = region
                             )
    
    s3_bucket = 'afternoon-prep-question-files' 
    #s3Key = 'WASSCE_JUNE/Agricultural Science_June_WASSCE/Agricultural_Science_2010/Agricultural_Science_S55022_June_Wassce_2010/OCR_READY/Agricultural_Science_S55022_June_Wassce_2010_pg2 001.jpg'
    #s3_prefix = 'WASSCE_JUNE/Biology_June_WASSCE/Biology_June_WASSCE_2010/Biology_June_WASSCE_2010/'
    
    
    ##Parsing subject information from S3 file/prefix name, allowing for cases where subjects have multiple words e.g Agricultural Science
    if s3_prefix.split('/')[-2].count('_') == 2:
        exam_type = s3_prefix.split('/')[-2].split('_')[-2]
        exam_sub_type = s3_prefix.split('/')[-2].split('_')[-3]
        exam_year = s3_prefix.split('/')[-2].split('_')[-1]
        exam_subject = '_'.join(s3_prefix.split('/')[2].split('_')[:-3])
    elif s3_prefix.split('/')[-2].count('_') >= 3:
        exam_type = s3_prefix.split('/')[-2].split('_')[-2]
        exam_year = s3_prefix.split('/')[-2].split('_')[-1]
        exam_sub_type = s3_prefix.split('/')[-2].split('_')[-3]
        exam_subject = '_'.join(s3_prefix.split('/')[2].split('_')[:-3])


    print(exam_subject)
    print(exam_year)
    print(exam_type)
    print(exam_sub_type)

    s3Keys = []
    resp = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix, Delimiter='/')


    for obj in resp['Contents']:
        s3Keys.append(obj['Key'])
    s3Keys.sort(key=natural_keys)   
    print(s3Keys)


    num_index = 1
    file_name = str("app/server/utils/raw_outputs/" + exam_type + "_" + exam_sub_type + "_" + exam_year + "_" + exam_subject)
    file = open(file_name, "w+")
    valid_options = 0  #Helps to skip the options that appear before the test begins
    
    for s3Key in s3Keys[1:]:               
        document_block = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3Key
                }
        }) 

        
        #choice_list = ['A', 'B', 'C', 'D'] Decided not to use
        banned_set = {'Turn over',
                       'DO NOT TURN OVER THIS PAGE UNTIL', 'YOU ARE TOLD TO DO SO.', 'YOU WILL BE PENALIZED SEVERELY IF YOU ARE', 'FOUND LOOKING AT THE NEXT PAGE BEFORE', 'YOU ARE TOLD TO DO SO.',
                       '1016', 
                       '1012',
                       '2059','2059)', '20159', '205n',
                        '3009',
                        '3015 WAEC Past Questions - Uploaded on https://www',
                        'L01411', 'FROM: EduNgr.com', '">>>>> FROM: EduNgr.com',
                        '19999'}  #Remove junk items, add to list to remove unwanted words
        
        choice_index = 4
        final_choice = True
        #valid_options = 0
        for item in document_block["Blocks"]:
                    if choice_index > 4:     #Keep index in check
                        choice_index = 4
                        
                    if item["BlockType"] == 'LINE':
                        #print(item)
                        #print (item['Text'] + '\n')
                        line = clean_text(item['Text'])
                        #print(line)
                        banned_item = line in banned_set
                        question_num = re.findall(question_number_regex, line)
                        choice = check_choice_regex(line)
                        #check_sections_regex(line)
                        #if (line.find("below") != -1 ):
                            #print(str(num_index) + ' ' + line)                
                        if (question_num) and (question_num[0] == str(num_index)) and (choice_index == 4) and not banned_item:  
                            #print(str(choice_index) + ' is choice index')
                            line =  '\n##'+ line
                            num_index = num_index + 1
                            choice_index = 0
                            valid_options = 1
                        elif (choice) and (valid_options) :
                            line = '@@'+ line
                            #print(line)
                            choice_index = choice_index + 1
                            #print(choice[0])
                        elif banned_item:
                            continue
                        #else: 
                        #    print("question num is " + str(question_num))
                        #    print("num_index is " + str(num_index))
                        file.write(line + ' ')
                        # print(line)
        
        #file.write(str(document_block))
            
    file.close() 
    
    print(file_name)
    return str(file_name)   
         
            
def main():
    s3_prefix = 'WASSCE_JUNE/Physics_November_WASSCE/Physics_November_WASSCE_2011/'
    detect_raw_text(s3_prefix)

#Main execution
if __name__ == "__main__":
    main()