# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 23:13:32 2020

@author: sshobowale
"""
#!/bin/python

import re
import string
import json
import os

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9_,'`:;%=$^<>!/\"\?\.\-\+\(\)\[\]\{\}\*\s]", '', text)

#def extract_sections(file_path):
    #section_regex = re.search(r"below")
    #with open
def check_sections_regex(line):
    section_dict = {}
    section_id = 0
    section_regex = re.compile(r'([\d]+) (and|-) ([\d]+)')
    sections = re.findall(section_regex, line)
    if sections: 
        print(sections)
        for section in sections:
            print(list(range(int(section[0]), int(section[2]) + 1)))
            section_dict
    #output_file_name = file_base_path + "/output_" + file_name        
    #with open(output_file_name, 'w') as json_file:
      #  json.dump(entire_dict, json_file, indent=2)
            
        
def check_sub_type(month):
    sub_type = ''
    if month.capitalize() == 'June':
        sub_type = "MAY/JUNE"
        return  sub_type
    else: 
        sub_type = "NOVEMBER/DECEMBER"
        return sub_type         
        

def extract_data(file_path):
    
    question_regex = re.compile(r"##((\d{1,2}).*)(@@A.*)(@@B.*)(@@C.*)(@@D.*)")
    #TODO: Explain the grouping done with the regex above
                                
    # Defining core variables 
    entire_list = []
    question_dict = {}
    choice_dict = {}
    question_id = 0
    
    file_name = os.path.basename(file_path).split('.')[0]
    exam_type = file_name.split('_')[0]
    exam_sub_type = file_name.split('_')[1]
    exam_year = file_name.split('_')[2]
    exam_subject = ' '.join(file_name.split('_')[3:])
    print(exam_subject)
    file_base_path = os.path.dirname(file_path)
    #print("File name is " + file_name) 
    #print("Dir name is " + file_base_path)
    
    with open(file_path, "r") as input_data:
        count = 0
        read_data = input_data.readlines() 
        #check_sections_regex(read_data)
        
        for line in read_data:
            #print(line)
            for question in re.finditer(question_regex, line):
                question_dict = {}
                question_dict['imageUrl'] = ""
                question_dict['sectionId'] = ""
                question_num = question.group(2)
                #entire_dict.update({ question_num : {} })
                question_dict['year'] = int(exam_year)
                question_dict['type'] = exam_type.upper()
                question_dict['subType'] = check_sub_type(exam_sub_type)
                question_dict['subject'] = exam_subject.upper()
                question_dict['text'] = clean_text(question.group(1)[question.group(1).find(".")+1:].strip())
                question_dict['number'] = int(question_num)
                question_dict['correctOption'] = "A"
                question_dict['options'] = {}
                for option_index in range(3,7):
                    choice_key = question.group(option_index)[2]
                    choice_value = clean_text(question.group(option_index)[3:].strip('.').strip().split('.')[0])
                    question_dict['options'].update({choice_key: choice_value})
                entire_list.append(question_dict)
                #print(question.group(0) + "\n")
                count = count + 1


            
        #print(re.findall(question_regex, read_data))
        print(count)
        #print(read_data)
        #print(entire_dict) 
        
        #Return output file as JSON
        output_file_name = file_base_path + "/output_" + file_name + ".json"
    with open(output_file_name, 'w') as json_file:
        json.dump(entire_list, json_file, indent=2)
        
        
def main():
    file_path = "./raw_outputs/WASSCE_June_2011_Economics"
    extract_data(file_path)
    

#Main execution
if __name__ == "__main__":
    main()