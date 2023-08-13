import re
import os
import json
import boto3
import urllib
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import time

load_dotenv()  # Load environment variables from .env

# ... (Existing code up to the clean_text function)

# Utility function to perform OCR on an image with retries
def perform_ocr(image_path, textract_client):
    max_retries = 3
    retry_delay = 5  # seconds

    for retry in range(max_retries):
        try:
            document_block = textract_client.detect_document_text(
                Document={
                    'Bytes': open(image_path, 'rb').read()
                }
            )
            return document_block
        except Exception as e:
            print(f"OCR failed for {image_path}. Retrying ({retry+1}/{max_retries})...")
            time.sleep(retry_delay)

    raise Exception(f"Failed to perform OCR on {image_path} after {max_retries} retries")

# OCR text extraction function
def detect_raw_text(s3_prefix):
    # ... (Existing code up to textract_client initialization)

    s3_bucket = 'afternoon-prep-question-files'
    
    # ... (Existing code up to the loop over s3Keys)
    
        for s3Key in s3Keys[1:]:
            try:
                document_block = perform_ocr(image_path=s3Key, textract_client=textract_client)

                choice_index = 4
                final_choice = True

                for item in document_block["Blocks"]:
                    if choice_index > 4:     # Keep index in check
                        choice_index = 4

                    if item["BlockType"] == 'LINE':
                        line = clean_text(item['Text'])
                        banned_item = line in banned_set
                        question_num = re.findall(question_number_regex, line)
                        choice = check_choice_regex(line)

                        if (question_num) and (question_num[0] == str(num_index)) and (choice_index == 4) and not banned_item:
                            line = '\n##' + line
                            num_index = num_index + 1
                            choice_index = 0
                            valid_options = 1
                        elif (choice) and (valid_options):
                            line = '@@' + line
                            choice_index = choice_index + 1
                        elif banned_item:
                            continue

                        file.write(line + ' ')
                        print(line)

            except Exception as e:
                print(f"Error processing {s3Key}: {str(e)}")

    file.close()
    return file_name