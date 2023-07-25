from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime


class QuestionsSchema(BaseModel):
    _id: str = Field(...)
    generated_questions: dict = Field(...)
    created_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "_id":"789141jd4121d41414d",
                "generated_questions":"Content",
                "created_at":"2023-01-16 10:42:45.788000"
            }
        }