from fastapi import UploadFile, File, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_bytes
import boto3
import os
from io import BytesIO

router = APIRouter()

@router.post("/")
async def convert_pdf_to_images(pdf_file: UploadFile = File(...)):
    try:
        # Read the uploaded PDF file
        pdf_content = await pdf_file.read()
        pdf_filename = pdf_file.filename

        # Convert PDF to images
        pdf_reader = PdfFileReader(BytesIO(pdf_content))
        pdf_images = convert_from_bytes(pdf_reader)

        # Upload images to S3 bucket
        s3_client = boto3.client("s3", aws_access_key_id=os.environ["AWS_ACCESS_KEY"], aws_secret_access_key=os.environ["AWS_SECRET_KEY"])
        s3_prefix = "pdf_images/"

        for index, image in enumerate(pdf_images):
            image_bytes = image.convert("RGB").tobytes()
            image_filename = f"{pdf_filename}_page_{index + 1}.jpg"

            s3_key = os.path.join(s3_prefix, image_filename)
            s3_client.upload_fileobj(BytesIO(image_bytes), os.environ["S3_BUCKET_NAME"], s3_key)

        message = {"message": "PDF pages converted and uploaded to S3"}
        return JSONResponse(content=message, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing PDF and uploading images")