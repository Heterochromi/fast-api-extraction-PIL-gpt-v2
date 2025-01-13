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


PIL_system = """
Extract the information provided in the schema.

format:
Package leaflet: Information for the patient
{(Invented name) (Strength(s)) (Pharmaceutical form)}
{Active substance(s)}

Notes:
1.Pharmacutical form can include a medical device such as a syringe, inhaler, pre-filled pen , patches, etc..., and Strength(s) will include measurement unit.
2.Full name will include the Invented name, Strength(s) and Pharmaceutical(s) form but the Invented name will not include the Strength(s) and Pharmaceutical form(s).
3.Invented name is usually the very first word or two words following the statement package information: for the patient and its just a brand name.

"""


spmc_system_prompt = """
Extract the information provided in the schema.

format:
PACKAGE INSERT
{(invented_name)}
{Active substance(s) (Pharmaceutical form)} 

NAME OF THE MEDICINAL PRODUCT

<user>note :if there is multiple dosages the full name will be repeated for each dosage</user>

{(Full name)}

{(Full name)}

DOSAGE FORMS AND STRENGTHS
{(Pharmaceutical form) (Strength(s))} 

COMPOSITION
{(invented_name) (Strength)}

<user>remaining content is about the what the medicine is made up of</user>
"""
def get_header_LLM(header_chunk , smpc = False):
    if smpc:
        system = spmc_system_prompt
    else:
        system = PIL_system
    prompt = ""
    for line in header_chunk:
        prompt += line + "\n"
    response = generate_schema_strict(prompt , system , Schema)
    return response
