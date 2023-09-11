from fastapi import APIRouter, HTTPException
import openai
import json
import os

# Initialize your OpenAI GPT-3 API key
openai.api_key = os.environ["OPENAI_API_KEY"]

router = APIRouter()

def generate_tags(question):
    try:
        # Use OpenAI's GPT-3 to generate tags
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate tagging for this question: {question} based on the format using Waec Standard.\nDifficulty Level:\nGrade Level:\nTopics:",
            max_tokens=100
        )
        
        # Extract the generated tags from the response
        generated_tags = response.choices[0].text.strip()

        # Convert the generated tags to a dictionary
        tags_dict = {}
        for line in generated_tags.split('\n'):
            key, value = line.strip().split(':')
            tags_dict[key.strip()] = value.strip()

        return tags_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def generate_tags_for_questions():
    try:
        # Load the existing JSON file
        with open("app\server\utils\raw_outputs\output_WASSCE_November_2011_Physics.json", "r") as json_file:
            questions = json.load(json_file)
        
        # Generate tags for each question and update the JSON
        for question_data in questions:
            question = question_data.get("text", "")
            tags = generate_tags(question)
            question_data["difficulty_level"] = tags.get("Difficulty Level", "")
            question_data["grade_level"] = tags.get("Grade Level", "")
            question_data["topics"] = tags.get("Topics", "")

        # Write the updated JSON back to the file
        with open("questions.json", "w") as json_file:
            json.dump(questions, json_file, indent=4)

        return {"message": "Tags generated and updated successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))