from bson.objectid import ObjectId
from app.server.database.db_connection import question_collections

from app.server.serializers.questions_serializer import questions_helper

# Database Crud Operation functions

# ================= Questions ==================
# Retrieve all Question entries

async def retrieve_question_contents():
    question_contents = []
    async for content in question_collections.find():
        question_contents.append(questions_helper(content))
    return question_contents

# Retrieve a single entry with matching ID

async def retrieve_question_content(id: str) -> dict:  # type: ignore
    question_content = await question_collections.find_one({"_id": ObjectId(id)})
    if question_content:
        return questions_helper(question_content)

# Add a new question entry

async def add_questions_content(questions_content_data: dict) -> dict:
    question_content = await question_collections.insert_one(questions_content_data)
    new_question_content = await question_collections.find_one({"_id": question_content.inserted_id})
    return questions_helper(new_question_content)