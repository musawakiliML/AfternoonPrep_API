from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
import os, json

from app.server.database.db_connection import question_collections

from app.server.database.crud import (
    add_questions_content,
    retrieve_question_content,
    retrieve_question_contents
)

from app.server.models.questions import QuestionsSchema

from app.server.utils import ocr_generation
from app.server.utils import data_extraction


router = APIRouter()

@router.post("/")
async def process_document(document: UploadFile = File(...)):
    # Step 1: Save the uploaded document locally
    with open(f"temp_{document.filename}", "wb") as temp_file:
        temp_file.write(await document.read())

    # Step 2: Perform OCR on the uploaded document
    s3_prefix = 'WASSCE_JUNE/Physics_November_WASSCE/Physics_November_WASSCE_2011/'
    try:
        ocr_output = ocr_generation.detect_raw_text(s3_prefix)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in OCR processing")

    # Step 3: Extract data from OCR output
    try:
        json_output_path = data_extraction.extract_data(ocr_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in data extraction")

    # Step 4: Read the generated JSON file
    try:
        with open(json_output_path, "r") as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading JSON file")

    # Step 5: Clean up temporary files
    os.remove(f"temp_{document.filename}")
    os.remove(ocr_output)
    os.remove(json_output_path)

    # Step 6: Return the JSON data as a response
    return JSONResponse(content=json_data)