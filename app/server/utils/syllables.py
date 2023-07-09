import json
import openai
import re
from NLP import completeTag, login
from inspect import Traceback
from time import sleep
import traceback
from deta import Deta
import requests
import dotenv
import os

config = dotenv.dotenv_values(".env")
# set up openai client
openai.api_key = config['OPENAI_API_KEY']

# tmp data storage
stored = []
syllabus_storage = []
topic_storage =[]

#deta = Deta(config['DETA'])
deta = Deta("a0aqwqju_iuD4K1vhN1kYK7yvxNL3p8JJyT5HeoJR")
# print(f"deta info : {deta}")
db = deta.Base("MatchedByTopicsDB") # set db name matchedTagsDB
# print(f"db: {db}")


# define function to generate syllables for a given prompt

def gen_syllabusBySubject(subject):
    # deefine prompt
    prompt = (f"Generate a Nigerian senior secondary school  syllabus for {subject}.\n")
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



def extractTopicsAndSubtopics(syllabus):

    prompt = (f"Generate a list of topics and subtopics from the following syllabus: \n{syllabus}\n"
              "Topic:   \n"
              "Subtopic:")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # extract topics and subtopics from response using reqular expression
    result = response.choices[0].text.strip().split("\n")
    topic_storage.append(result)
    
    # print(result)
    return result


def getQuestion():
    try:
        token = login("teslasdeveloper@gmail.com", "aD@vin33")   # ,
        print('token ', token)
        keyToExtract = "text"
        foundQuestions = []
        url = "http://afternoonprep.com/api/v1/questions?year=2003&exam=JAMB&subject=Pyhsics"
        headers = {"Authorization": "Bearer " + token}
        response = requests.request("GET", url, headers=headers)
        questions = response.json()["data"]["questions"]
        if (questions):
            for question in questions:
                if keyToExtract in question:
                    _question = question[keyToExtract]

                    # num = question.get('number')
                    foundQuestions.append(f"{_question}\n")
                else:
                    print("No question found")
                    continue
        return foundQuestions
    except Exception as e:
        print(e.with_traceback())


def matchQuestionToSyllables(question, topics):
    prompt= f"Match the following question to a topic from the list:\n\nQuestion: {question}\n\nTopics:\n{json.dumps(topics)}\n\nTopic:"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10,
    )
    topic = response.choices[0].text.strip()

    return topic


# grade10_12 = "senior secondary school students"

# Function to predict the difficulty level of a question
def predict_difficulty(question):
    prompt = f'''Instruction: Provide a question and tag it with the appropriate difficulty level for an average senior secondary school student: easy, medium, difficult.
    Question: What is the capital of France?
    Difficulty: easy

    Question: Solve the equation 3x + 5 = 20. 
    Difficulty: medium

    Question: Explain the theory of relativity.
    Difficulty: difficult

    Question: {question}
    Difficulty:  '''
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0.0,
        )

        predictedDifficulty = response["choices"][0]["text"].strip()
        return predictedDifficulty
    except Exception as e:
        print("An error occurred during prediction:")
        print(str(e))
        return None


def tagMultiQuestions(start_year, end_year, step=1):
    try:
        token = login(config['MAIL'], config['PSWD'])
        print('token ', token)
        base_url = "http://afternoonprep.com/api/v1/questions"
        headers = {"Authorization": "Bearer " + token}
        
        getQuestionstoTag = ""
        syllabus = gen_syllabusBySubject(subject)
        print(f"generating syllabus for {subject}")
        syllabus_topics = extractTopicsAndSubtopics(syllabus)
        print(f"generating topic for {syllabus}")
        for year in range(start_year, end_year+1):
            url = f"{base_url}?year={year}&exam=JAMB&subject={subject}" 
            response = requests.request("GET", url, headers=headers)
            #response = request.get(url)
            data = response.json()["data"]["questions"]
            #print(data)
            if (data):
                for question in data:
                    examtype = "obj"
                    exam = question.get('type')
                    _year = question.get('year')
                    # _subject = question.get('subject')
                    num = question.get('number')
                    _question = question.get('text')
                    match = matchQuestionToSyllables(_question, syllabus_topics)
                    predicted_difficulty = predict_difficulty(_question)
                    stored.append({f"key: {subject}{exam}{examtype}{_year}, num: {num}, Matched_topic: {match}, difficulty: {predicted_difficulty}"})
            #print(stored)
            print('Match completed...')
            file_to_json = set_to_json(stored)
            with open(file_to_json,"r") as f:
                if file_to_json == []:
                    print("Null result")
                    return
                print("dumping to deta")
                deta_dump = json.dumps(file_to_json, f)
                print("saving to deta.......")
                db.put(key=subject+exam+examtype+str(_year), data=deta_dump)
                print(f"{subject}{exam}{examtype}{str(_year)} \n saved! sucessfully")
            #saveToFile(stored)
            # print('saving to db...')
            # saveToDb(inMemDb)
    except Exception as e:
        print(e.with_traceback())




def saveToFile(text):
    print("saving to file....")
    file_to_json = set_to_json(text)
    with open(subject+exam+year+".json","w") as db:
        if file_to_json == []:
            return
        json.dump(file_to_json,db)

# function to allow json serialization of a set
def set_to_json(text):
    json_serilized = [str(elem) for elem in text]
    return json_serilized

def save_to_deta(text):
    print("saving to deta....")
    file_to_json = set_to_json(text)
    with open(subject+exam+year+examtype+".json","w") as db:
        if file_to_json == []:
            return
        deta_dump = json.dump(file_to_json,db)
        print("saving to deta.......")
        db.put(key=subject+exam+year+examtype, data=deta_dump)
        print("saved!")


def saveToDb2():
    with open("BiologyJAMBobj1979.json","r") as file:
        print("saving to db................................")
        items = json.load(file)
        year = "1979"
        #print(items)
        saveToDB = db.put(key=subject+exam+year, data=items)
        print(saveToDB)


subject = "Biology"
# questions = getQuestion()
# syllabus = gen_syllabusBySubject(subject)
# topics = extractTopicsAndSubtopics(syllabus)

# year = "2012"
exam = "JAMB"
tagMultiQuestions(1980, 2018)
# print(getQuestion())



# for question in questions:
#     match = matchQuestionToSyllables(question, topics)
#     predicted_difficulty = predict_difficulty(question)
#     stored.append({f"key: {subject}{exam}{year}, Matched_topic: {match}, difficulty: {predicted_difficulty}"})
#     # stored[question] = {" Matched_topic": match, "difficulty": predicted_difficulty }
  
# print(stored)
# saveToFile(stored)
# saveToDb2()
    # getMatch = print(f"Question: {question}\nMatch: {match}\n")
    # stored.append(f"Question: {question}, Matched to {match}")
    
# saveToFile(stored)
# print(stored)
    # print("Done")
# print(stored)
# saveToDb2()
print("Done")
# print(db.get("leiffqp9mc21"))
# January27@
# afternoonprep1