from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
import openai
import json
from langchain.llms import OpenAI
# from secret import test_key

def TopicGen(topic, difficulty, apiKey, max_tokens_limit=1000):
    template="""create a JSON object containing a list of sub-topics based on {topic} for {difficulty}. It should have the following structure:
        -"Topic": (name of the topic)
        -"Sub_Topics":(containing list of sub topics)
        Ensure that the sub-topics cover various aspects of {topic} based on {difficulty}. Return the JSON structure with the key "sub_topics."""
    prompt = PromptTemplate(template=template, input_variables=["topic", "difficulty"])
    llm = OpenAI(openai_api_key=apiKey, temperature=0.6, max_tokens=max_tokens_limit,model='gpt-3.5-turbo-instruct')
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    # Run the initial request
    response = llm_chain.run({"topic": topic, "difficulty": difficulty})
    
    # Check the length of the response
    response_length = len(response.split())  # Assuming tokens are separated by spaces

    # Dynamically adjust max_tokens if needed
    if response_length > max_tokens_limit:
        max_tokens_adjusted = max_tokens_limit + (response_length - max_tokens_limit)
        llm = OpenAI(openai_api_key=apiKey, temperature=0.6, max_tokens=max_tokens_adjusted,model='gpt-3.5-turbo-instruct')
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run({"topic": topic, "difficulty": difficulty})
    # print("Raw response:", response)  # Add this line to print the raw response
    try:
        responseret = json.loads(response)
        return responseret
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"topic": "ERROR", "sub_topics": ["ERROR"]}
