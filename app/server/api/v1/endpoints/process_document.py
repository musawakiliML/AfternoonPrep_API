from fastapi import APIRouter,status, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime
import os, json
import openai

from app.server.database.db_connection import question_collections

from app.server.database.crud import (
    add_questions_content,
    retrieve_question_content,
    retrieve_question_contents
)

from app.server.models.questions import QuestionsSchema

from app.server.utils.ocr_generation import detect_raw_text
from app.server.utils.data_extraction import extract_data
from app.server.utils.generate_tags import generate_tags_for_questions



# Initialize your OpenAI GPT-3 API key
openai.api_key = os.environ["OPENAI_API_KEY"]

router = APIRouter()

@router.post("/", response_description="Generated Questions Json File Has been created", response_model=QuestionsSchema)
async def process_document(exam_subject: str = Form(default="Physics"), exam_year: str = Form(default="2011"), exam_type: str = Form(default="WASSCE"), exam_sub_type: str = Form(default="November")):
    # Step 1: Extract The user given information to create the prefix
    
    if exam_type == "WASSCE" and exam_sub_type == "November":
        first_prefix = f"{exam_type}_JUNE/"
        s3_prefix = first_prefix + f"{exam_subject}_{exam_sub_type}_{exam_type}/" + f"{exam_subject}_{exam_sub_type}_{exam_type}_{exam_year}/"
    elif exam_type == "WASSCE" and exam_sub_type == "June":
        first_prefix = f"{exam_type}_JUNE/"
        s3_prefix = first_prefix + f"{exam_subject}_{exam_sub_type}_{exam_type}/" + f"{exam_subject}_{exam_sub_type}_{exam_type}_{exam_year}/"
    
    # Step 2: Perform OCR on the uploaded document
    try:
        ocr_output = detect_raw_text(s3_prefix)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in OCR processing")
    
    # Step 3: Extract data from OCR output
    try:
        data_output = extract_data(ocr_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in data extraction")
    
    # Step 4: Add tags to each question like difficulty level, grade level etc..
    try:
        updated_questions = generate_tags_for_questions(data_output)
        if updated_questions:
            result = updated_questions['result']
            response = updated_questions['message']
            print(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in Question Tagging")
    
    # Step 4: Save the generated file to database.
    try:
        data_output = jsonable_encoder(result)
        created_at = datetime.utcnow()
        schema = {
            "generated_questions":data_output,
            "created_at": created_at
        }

        new_questions = await add_questions_content(schema)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Saving Data to Database")
    
    os.remove(ocr_output) # remove ocr generated file.

    # Step 5: Return the JSON data as a response
    return JSONResponse(content=new_questions)


# GET all Questions Route

@router.get("/", response_description="Get List of Questions", response_model=List[QuestionsSchema])
async def get_questions_data():

    try:
        all_questions_data = await retrieve_question_contents()
        data_model = []
        if all_questions_data:
            for data in all_questions_data:
                response_model = {
                    "id": data["id"],
                    "generated_questions": data["generated_questions"],
                    "created_at": data["created_at"],
                }
                data_model.append(response_model)

            data_model = jsonable_encoder(data_model)

            return JSONResponse(status_code=status.HTTP_200_OK, content=data_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Retrieving Data from Database")


# GET a single Question Route

@router.get("/{id}", response_description="Get a Single Question data", response_model=QuestionsSchema)
async def get_question_data(id):

    try:
        question_data = await retrieve_question_content(id)
        if question_data:
            response_model = {
                    "id": question_data["id"],
                    "generated_questions": question_data["generated_questions"],
                    "created_at": question_data["created_at"],
                }
            
            return JSONResponse(status_code=status.HTTP_200_OK, content=response_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Retrieving Data from Database")