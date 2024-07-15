# from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# import openai
from langchain.llms import OpenAI
import json
import os

def questionGen(topic,apikey,max_tokens_limit=1000):
  template="""
   Create a JSON object containing a list of 5 multiple-choice questions on {topic}. Each question should have the following structure:
- "question": (The text of the question)
- "options": (A list of four options)
- "correctAnswer": (The correct option from the list)
- "difficultyLevel": (A difficulty level on a scale of 0 to 3000, where 0 is the easiest, 1500 is medium, and 3000 is the hardest)

Ensure that the questions cover various aspects of {topic} and provide meaningful options for each question. Return the JSON structure with the key "questions."
  """
  prompt = PromptTemplate(template=template, input_variables=["topic"])

  llm=OpenAI(openai_api_key=apikey,temperature=0.5,max_tokens=max_tokens_limit,model='gpt-3.5-turbo-instruct')
  llm_chain=LLMChain(prompt=prompt, llm=llm)
  response=llm_chain.run({"topic":topic})
  response_length = len(response.split())

  if response_length>max_tokens_limit:
    max_tokens_adjusted=max_tokens_limit+(response_length - max_tokens_limit)
    llm=OpenAI(openai_api_key=apikey,temperature=0.5,max_tokens=max_tokens_adjusted,model='gpt-3.5-turbo-instruct')
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response=llm_chain.run({"topic":topic})

  try:
    responseret=json.loads(response)
    return responseret
  except:
    return {"Question1":{
        'Question': 'Error in making questions from OpenAI',
        'Options': ['Error',
        'Error',
        'Error',
        'Error'],
        'CorrectAnswer': 'Error',
        'DifficultyLevel': 0}}