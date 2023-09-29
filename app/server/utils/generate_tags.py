import os
import json
import openai
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException

load_dotenv()

# Initialize your OpenAI GPT-3 API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def extract_tags_info(generated_tags):

    # Initialize variables to store extracted information
    difficulty_level = ""
    grade_level = ""
    topics = ""
    tags = ""
    explanations = ""

    # Split the generated tags into lines and iterate through them
    for line in generated_tags:
        line = line.strip()  # Remove leading/trailing whitespace

        if line.startswith("Difficulty Level:"):
            difficulty_level = line.replace("Difficulty Level:", "").strip()
        elif line.startswith("Grade Level:"):
            grade_level = line.replace("Grade Level:", "").strip()
        elif line.startswith("Topics:"):
            topics = line.replace("Topics:", "").strip()
        elif line.startswith("Tags:"):
            tags = line.replace("Tags:", "").strip()
        elif line.startswith("Explain Question and Answer:"):
            explanations = line.replace("Explain Question and Answer:", "").strip()

    # Return the extracted information as a dictionary

    return {
        "Difficulty Level": difficulty_level,
        "Grade Level": grade_level,
        "Topics": topics,
        "Tags": tags,
        "Explanations": explanations
    }

def generate_tags(question):
    try:
        # tags_info = []
        # for question in questions:
        #     question_text = question['text']
        #     # print(question_text)

        # Use OpenAI's GPT-3 to generate tags
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate tagging for this Question:'{question}'.\nStrictly based on Waec Standard.\nJust respond with only the following format below: \n\nDifficulty Level:\n\nGrade Level:\n\nTopics: \n\nTags:\n\nExplain Question and Answer:",
            max_tokens=2000,
            temperature=1,
            top_p=1,
            frequency_penalty=0.43,
            presence_penalty=0.39
        )
        # print(response.choices[0])

        # Extract the generated tags from the response
        if "choices" in response:
            if len(response["choices"]) > 0:
                generated_tags = response["choices"][0]["text"].split("\n")
                for i in range(generated_tags.count('')):
                    generated_tags.remove('')
                # print("Generated tags:",generated_tags)

                # Convert the generated tags to a list of dictionary
                # tags_info.append(extract_tags_info(generated_tags))
                result = extract_tags_info(generated_tags)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # print(str(e))

def generate_tags_for_questions(questions):
    try:
        # # Load the existing JSON file
        # with open(r"C:\Users\musaw\Documents\GitHub\AfternoonPrep_API\app\server\utils\test_tags.json", "r") as json_file:
        #     questions = json.load(json_file)
        #     # print(questions)
        
        # Generate tags for each question and update the JSON
        for question_data in questions:
            # print(question_data)
            question = question_data["text"]
            tags = generate_tags(question)
            # print(tags)
            question_data["difficulty_level"] = tags.get("Difficulty Level", "")
            question_data["grade_level"] = tags.get("Grade Level", "")
            question_data["topics"] = tags.get("Topics", "")
            question_data["tags"] = tags.get("Tags", "")
            question_data["explanations"] = tags.get("Explanations", "")

        # Write the updated JSON back to the file
        # with open("questions.json", "w") as json_file:
        #     json.dump(questions, json_file, indent=4)
        
        return {"message": "Tags generated and updated successfully!", "result": questions}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # print(str(e))


# result = generate_tags_for_questions()

# print(result)
# test_dict = [
#   {
#     "imageUrl": "",
#     "sectionId": "",
#     "year": 2011,
#     "type": "WASSCE",
#     "subType": "NOVEMBER/DECEMBER",
#     "subject": "PHYSICS",
#     "text": "The mass of an object can be measured using the following instruments except",
#     "number": 1,
#     "correctOption": "A",
#     "options": {
#       "A": "spring balance",
#       "B": "lever",
#       "C": "metre rule",
#       "D": "beam balance"
#     }
#   },
#   {
#     "imageUrl": "",
#     "sectionId": "",
#     "year": 2011,
#     "type": "WASSCE",
#     "subType": "NOVEMBER/DECEMBER",
#     "subject": "PHYSICS",
#     "text": "A load of 80 N extends a spring by 8 cm. When the load is replaced by a copper block, the extension produced is 10 cm. Calculate the weight of the copper block, assuming that the elastic limit of the spring is not exceeded.",
#     "number": 2,
#     "correctOption": "A",
#     "options": {
#       "A": "40 N",
#       "B": "64 N",
#       "C": "100 N",
#       "D": "160 N"
#     }
#   }
# ]
# response = generate_tags(test_dict)

# print(response)