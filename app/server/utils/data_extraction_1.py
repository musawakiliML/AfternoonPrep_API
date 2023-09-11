import re
import string
import json
import os

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9_,'`:;%=$^<>!/\"\?\.\-\+\(\)\[\]\{\}\*\s]", '', text)

def check_sub_type(month):
    sub_type = ''
    if month.capitalize() == 'June':
        sub_type = "MAY/JUNE"
    else:
        sub_type = "NOVEMBER/DECEMBER"
    return sub_type

def extract_data(file_path):
    entire_list = []
    question_dict = {}
    question_id = 0
    in_question_25 = False  # Flag to indicate if we are inside question 25
    question_text = ""  # To store the text of the current question

    file_name = os.path.basename(file_path).split('.')[0]
    exam_type = file_name.split('_')[0]
    exam_sub_type = file_name.split('_')[1]
    exam_year = file_name.split('_')[2]
    exam_subject = ' '.join(file_name.split('_')[3:])

    with open(file_path, "r") as input_data:
        count = 0
        read_data = input_data.readlines()

        for line in read_data:
            try:
                # Use regular expressions to identify question numbers and text
                question_match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
                if question_match:
                    question_num = question_match.group(1)
                    question_text = clean_text(question_match.group(2))
                    in_question_25 = question_num == '25'
                    question_dict = {
                        'imageUrl': "",
                        'sectionId': "",
                        'year': int(exam_year),
                        'type': exam_type.upper(),
                        'subType': check_sub_type(exam_sub_type),
                        'subject': exam_subject.upper(),
                        'text': question_text,
                        'number': int(question_num),
                        'correctOption': "A",
                        'options': {}
                    }
                elif in_question_25:
                    # Use regular expressions to extract options and correct option
                    option_match = re.match(r'^([A-D])\.\s+(.+)$', line.strip())
                    if option_match:
                        choice_key = option_match.group(1)
                        choice_value = clean_text(option_match.group(2))
                        question_dict['options'][choice_key] = choice_value
                    elif re.match(r'^\d+$', line.strip()):
                        # If we encounter a new question number, add the previous question to the list
                        entire_list.append(question_dict)
                        question_dict = {}  # Reset the question_dict
            except Exception as e:
                print(f"Error processing line {count + 1}: {e}")

    output_file_name = f"output_{file_name}.json"
    with open(output_file_name, 'w') as json_file:
        json.dump(entire_list, json_file, indent=2)

    return entire_list

def main():
    file_path = "/Users/musaml/Documents/GitHub/AfternoonPrep_API/app/server/utils/raw_outputs/WASSCE_November_2011_Physics"
    extract_data(file_path)

# Main execution

if __name__ == "__main__":
    main()