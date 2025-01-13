import os
from dotenv import load_dotenv
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from extractUtils import getValidJson

import ollama
load_dotenv()


# client = ollama.Client("localhost")


    
# def generate_gpt(prompt, system):
#     response = client.generate(model=os.getenv("model"),prompt=prompt, system=system , options={"num_ctx": int(os.getenv("num_ctx"))})
#     return response["response"]


# def generate_gpt_max_token(prompt, system, max_tokens):
#     response = client.generate(model=os.getenv("model"),prompt=prompt, system=system , options={"num_ctx":  int(os.getenv("num_ctx")), "num_predict": max_tokens})
#     return response["response"]


# def generate_schema_strict(prompt, system,schema):
#     response = client.generate(model=os.getenv("model"),prompt=prompt, system=system , options={"num_ctx":  int(os.getenv("num_ctx")), "temperature" :0} , format=schema.model_json_schema())
#     return getValidJson(response["response"])


# openAI API 


client = OpenAI(api_key=os.getenv("gpt_key"))
def generate_gpt(prompt, system):
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
        )
    return response.choices[0].message.content

#openAI API 
def generate_gpt_max_token(prompt, system, max_tokens):
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
        )
    return response.choices[0].message.content




def generate_schema_strict(prompt, system,schema):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
           messages=[
                {"role": "system", "content": system},
                 {"role": "user", "content": prompt}
             ],        
        response_format=schema,
    )
    response = response.choices[0].message.parsed
    return response.dict()




