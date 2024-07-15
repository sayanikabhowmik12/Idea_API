from typing import Union
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, ValidationError, root_validator
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from questions import questionGen
from topics import TopicGen

class Questions(BaseModel):
    Topic: str
    APIkey: str
    @root_validator (pre=True,skip_on_failure=True)
    def change_input_data(cls, v):
        if len(v) < 2:
            raise ValueError("Both the fields are required")
        return v

class Topics(BaseModel):
    Topic: str
    difficulty: str
    APIkey: str
    @root_validator (pre=True,skip_on_failure=True)
    def change_input_data(cls, v):
        if len(v) < 3:
            raise ValueError("3 fields are required")
        return v

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update as needed
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],  # Update as needed
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = '.'.join(error['loc'])
        message = error['msg']
        errors.append({'field': field, 'message': message})

    return JSONResponse(
        status_code=422,
        content={'detail': 'Validation error', 'errors': errors},
        headers={"Access-Control-Allow-Origin": "*"},  # Adjust as needed
    )
@app.get("/", status_code=200)
def status():
    return {"status": 200}

@app.post("/questions")

async def requested_data(item: Questions):
    # No need to convert to dict, FastAPI will handle it
    topic = item.Topic
    apikey = item.APIkey
    # print(item)
    response = questionGen(topic=topic, apikey=apikey)
    if response != '':
        return response

@app.post("/questions/subtopics")
async def requested_topic(topics: Topics):
    # No need to convert to dict, FastAPI will handle it
    topicsloc = topics.Topic
    difficulty = topics.difficulty
    apikey = topics.APIkey
    response = TopicGen(topic=topicsloc, difficulty=difficulty, apiKey=apikey)
    if response != '':
        return response
