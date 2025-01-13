import json
from semantic import semantic_similarity


def get_section_codes():
    with open('smpc/sectionCodes.json', 'r') as json_file:
      data = json.load(json_file)
    return data["sections"]




# {
#   "content": [
    # {
    #   "section_title": "",
    #   "section_string": ""
    # },
#     {
#       "section_title": "",
#       "section_string": ""
#     }
#   ]
# }





def splitAndGetCode(titles,content):
    code_sections = get_section_codes()
    result = []
    indexes = []
    last_index = 0
    for i, current_section in enumerate(titles):
        index = 0
        highest_similarity = 0.0
        for j , line in enumerate(content):
            if last_index > j:
                continue
            similarity_ratio = semantic_similarity(current_section, line , lang="en")
            print(current_section, line , similarity_ratio , highest_similarity)
            if similarity_ratio > highest_similarity or similarity_ratio >= 0.95:
                if similarity_ratio > highest_similarity:
                 last_index = index

                highest_similarity = similarity_ratio
                index = j
            if similarity_ratio >= 0.95:
                break
        indexes.append(index)
    print(indexes)
    for i , index in enumerate(indexes):
        
        if i == len(indexes) - 1:
            result.append({"title": titles[i], "content": content[index:], "code": ""  , "display":"", "semantic_similarity": 0.0})	
        else:
            result.append({"title": titles[i], "content": content[index:indexes[i+1]] , "code": "","display":"", "semantic_similarity": 0.0})
        
    for i , res in enumerate(result):
        section_title = res["title"]
        found = False
        for db_section in code_sections:
            if section_title.lower() == db_section["Display"].lower():
                result[i]["code"] = db_section["Code"]
                found = True
                break

        if found:
            continue
        highest_similarity = 0
        section_code = ""
        display = ""
        for db_section in code_sections:
             simlarity = semantic_similarity(section_title , db_section["Display"])
             if simlarity > highest_similarity: 
                    highest_similarity = simlarity
                    section_code = db_section["Code"]
                    display = db_section["Display"]
        if highest_similarity >= 0.8:
         result[i]["code"] = section_code
         result[i]["display"] = display
         result[i]["semantic_similarity"] = highest_similarity
        else:
            result[i]["code"] = "Not Found"
            result[i]["semantic_similarity"] = 0.0
    return result




def get_smpc(titles,content):
    sections = []
    result = {}
    try:
        sections = splitAndGetCode(titles,content)
    except Exception as e:  
        print(e , "error could not split sections and get codes , please make sure the order of the sections titles is correct")
        return {"error": "error could not split sections and get codes , please make sure the order of the sections titles is correct"}
    
    # result = {"sections": sections , "header": "" , "atc_code": "" , "routes":"", "MAH_details": ""}
    
