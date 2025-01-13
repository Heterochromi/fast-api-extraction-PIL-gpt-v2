import ollama
from extractUtils import getValidJson
import os
from dotenv import load_dotenv
from clientgpt import generate_gpt_max_token
from clientgpt import generate_schema_strict
from pydantic import BaseModel

class Schema(BaseModel):
    full_name: str
    invented_name: str
    strengths: list[str]
    measurement_unit: str
    pharmaceutical_forms: list[str]
    active_substances: list[str]
    medical_device: str


system = """
format:
Package leaflet: Information for the patient
{(Invented name) (Strength(s)) (Pharmaceutical form)}
{Active substance(s)}

Notes:
1.Pharmacutical form can include a medical device such as a syringe, inhaler, pre-filled pen , patches, etc..., and Strength(s) will include measurement unit.
2.Full name will include the Invented name, Strength(s) and Pharmaceutical(s) form but the Invented name will not include the Strength(s) and Pharmaceutical form(s).
3.Invented name is usually the very first word or two words following the statement package information: for the patient and its just a brand name.

Extract the information provided in the schema.
"""
def get_header_LLM(header_chunk):
    prompt = ""
    for line in header_chunk:
        prompt += line + "\n"
    response = generate_schema_strict(prompt , system , Schema)
    return response
