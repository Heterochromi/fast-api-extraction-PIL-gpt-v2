from extractUtils import check_similarity
from clientgpt import generate_schema_strict
from pydantic import BaseModel

class Schema(BaseModel):
    marketing_authorisation_holder: list[str]
    manufacturer: list[str]
    address: list[str]
    city: list[str]
    country: list[str]


system = """
User will provide information about the Marketing Authorisation Holder and Manufacturer of a specific medication.
Find the following information in the text:
<information>
1.Marketing Authorisation Holder(MAH)
2.Manafacturer
3.Address
4.City
5.Country
</information>
Only respond with the provided format:
"""


def get_MAH_Details_LLM(last_section):
    prompt = ""
    for i , line in enumerate(last_section):
      prompt += line + "\n"
    response = generate_schema_strict(prompt , system , schema=Schema)
    return response

