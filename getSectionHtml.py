import json
from extractUtils import clean_xml_html , extract_div_contents
import os
from dotenv import load_dotenv
from clientgpt import generate_gpt
load_dotenv()
def get_section_codes():
    with open('sectionCodes.json', 'r') as json_file:
      data = json.load(json_file)
    return data["sections"]


system_prompt = """
You will fill the text provided by the user in the HTML format(every quote should be converted as html entities).
Make sure to use lists using <ul> and <li> tags where appropriate otherwise do not use a lists only fill in the statements in <p> tags, add <b> tag for titles/sub titles, also make sure to copy the text exactly as provided when filling into the html without changing or adding word/statement.
Make sure to never leave any statement or word from the original text, always add every word into the html.
ONLY RESPOND WITH THE HTML, DO NOT ADD ANYTHING ELSE.

format:
<div xmlns="http://www.w3.org/1999/xhtml"><p><b>{(Number).Entire section title this is usually just the very first line}</b></p><p><b>{sub heading title}</b></p><ul><li>{sub heading information 1}</li><li>{sub heading information 2}</li><li>{sub heading information 3}</li></ul><p><b>{another sub heading title}</b></p><p>{sub heading information 1.}<p><p>{sub heading information 2.}<p></div>

"""



def get_sections_html(sections , section_titles):
    section_codes = get_section_codes()
    sections_html = []
    original_section = []
    for section in sections:
        prompt = ""
        for line in section:
            if line.strip() == "":
                continue
            prompt += line + "\n"
        original_section.append(prompt)
        # response = ollama.generate(model=model , system=system_prompt, prompt=prompt)
        response = generate_gpt(prompt , system_prompt)
        # response = response['response']
        sections_html.append(response)
    for i ,text in enumerate(sections_html):
        section_title = section_titles[i]
        code = section_codes[i]["section-code"]
        display = section_codes[i]["display-value"]
        html = extract_div_contents(text.strip())
        if html == None:
            html = "error could not generate html"
        html = clean_xml_html(text)
        sections_html[i] = {"html" : html,"display":display,"section_title":section_title, "code":code , "system" : "http://loinc.org" ,"original": original_section[i]}
    return sections_html
 