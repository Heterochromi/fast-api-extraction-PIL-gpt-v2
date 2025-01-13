import ast
import ollama
import os
from clientgpt import generate_gpt_max_token
model = os.getenv("MODEL")
from dotenv import load_dotenv
load_dotenv()
system_prompt_intended_uses = """
User will provide information about what is a medical product and what it is used for. You will determine the intended uses of the medication and only respond with the correct intended uses.

only respond with this format and do not include anything else in your response:
["1.use 1" , "2.use 2" , "3.use 3", "etc..."]
"""

system_prompt_target_populations = """
User will provide information about a medical product, you will determine the target populations for the medical product

only respond with this format and do not include anything else in your response:
["1.target population 1" , "2.target population 2" , "3.target population 3", "etc..."]
"""

system_pormpt_flavor = """
User will provide information about a medical product, occasionally the medication will have a flavour . You will determine the flavour  of the medication and only respond with the correct flavor.

some medicications have color, make sure to only answer with the flavour of the mediciation that refers to the taste not the color of the medication.
leave empty if there is no flavor mentioned in the text.

only respond with this format and do not include anything else in your response:
["flavour"]
"""

def get_intended_uses(section_1):
    counter = 0
    while True:
        intended_uses_array = []
        prompt = "" 
        for i , line in enumerate(section_1):
            prompt += line + "\n"
            if i == (len(section_1) - (counter * 2)):
                break
        # response = ollama.generate(model=model , system=system_prompt_intended_uses, prompt=prompt, options = {"num_predict": 250})
        response = generate_gpt_max_token(prompt , system_prompt_intended_uses , 250)
        try:
          intended_uses_array = ast.literal_eval(response)
          break
        except:
            if counter == 10:
                print("Error in getting intended uses")
                intended_uses_array = []
                break
            counter += 1
            print("Error in getting intended uses trying with smaller context")
    return intended_uses_array

    
def get_target_populations(section_1 , section_2):
    counter = 0
    while True:
        target_populations_array = []
        prompt = ""
        for i , line in enumerate(section_1):
            prompt += line + "\n"
            if i == (len(section_1) - (counter * 2)):
                break
        for i , line in enumerate(section_2):
            prompt += line + "\n"
            if i == (len(section_2) - (counter * 2)):
                break
        # response = ollama.generate(model=model , system=system_prompt_target_populations, prompt=prompt, options = {"num_predict": 350})
        response = generate_gpt_max_token(prompt , system_prompt_target_populations , 350)
        try:
            target_populations_array = ast.literal_eval(response)
            break
        except:
            if counter == 10:
                print("Error in getting target populations")
                target_populations_array = []
                break
            counter += 1
            print("Error in getting target populations trying with smaller context")
    return target_populations_array
    

def get_flavor(section_6):
    prompt = ""
    for line in section_6:
        prompt += line + "\n"
    # response = ollama.generate(model=model , system=system_pormpt_flavor, prompt=prompt, options = {"num_predict": 20})
    response = generate_gpt_max_token(prompt , system_pormpt_flavor , 20)
    try:
      flavor = ast.literal_eval(response)
    except:
        print("Error in getting flavor")
        flavor = []
        return
    return flavor


def get_extra_parts(sections):
    if len(sections) < 7:
        print("sectioning error not enough sections")
        return
    section_1 = sections[0]
    section_2 = sections[1]
    section_6 = sections[5]
    intended_uses = get_intended_uses(section_1)
    print(intended_uses)
    target_populations = get_target_populations(section_1 , section_2)
    print(target_populations)
    flavor = get_flavor(section_6)
    print(flavor)
    extra_parts = {
        "intended_uses" : intended_uses,
        "target_populations" : target_populations,
        "flavor" : flavor
    }
    print(extra_parts)
    return extra_parts
