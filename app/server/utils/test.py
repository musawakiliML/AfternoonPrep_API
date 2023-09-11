import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
syllabus_storage = []
def gen_syllabusBySubject(subject):
    # deefine prompt
    prompt = (f"Generate tagging for this question: “The earliest form of agriculture started with” based on the format using Waec Standard.
Difficulty Level:
Grade Level:
Topics: {subject}.\n")
            #   "Topic:   \n"
            #   "Subtopic:")
    
    # Generate syllabus
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    result = response.choices[0].text.strip()
    syllabus_storage.append(result)
    return result

test = gen_syllabusBySubject("English")

print(test)