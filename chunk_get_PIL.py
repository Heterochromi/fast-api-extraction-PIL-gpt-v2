import PyPDF2
from extractUtils import check_similarity , getValidJson , check_similarity_with_match_word_length_in_sentence , remove_extra_spaces
from getHeaderUsingLLM import get_header_LLM
from getRoutes import get_adminstration_routes_array
from getMahSection import get_MAH_Details_LLM
from getAtcCode import get_final_codes
from determineStatusOfSupply import determineStatusOfSupply
from getExtraParts import get_extra_parts
from getSectionHtml import get_sections_html
from getHeaderHtmlSection import get_header_html_section , get_what_is_in_this_leaflet_html_section
from semantic import semantic_similarity
import json
import time





translations = {
    "Package leaflet: Information for the user": "نشرة العبوة : معلومات المريض" ,
    "What is in this leaflet" : "في هذه النشرة",

}

def pdf_to_array(pdf_path):
    lines = []
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Iterate through all pages
        for page in pdf_reader.pages:
            # Extract text from the page
            text = page.extract_text()
            # text = remove_extra_spaces(text)
            
            # Split the text into lines and add to the array
            lines.extend(text.split('\n'))
    for i , line in enumerate(lines):
        lines[i] = remove_extra_spaces(line)

    return lines

def get_section_codes():
    with open('sectionCodes.json', 'r') as json_file:
      data = json.load(json_file)
    return data["sections"]

def get_drug_info(pdf_lines , lang):
    if lang == "en":
        find_line = "Package leaflet: Information for the user"
    else:
        find_line = translations["Package leaflet: Information for the user"]

    biggest = 0
    drugInfo = ""
    for i ,line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line, find_line)
        if similarity_ratio > biggest:
            biggest = similarity_ratio
            index = i
    print(biggest)
    if biggest < 0.65:
     for i in range(50):
        drugInfo += pdf_lines[i] + "\n"
     return drugInfo

    for i in range(15):
        drugInfo += pdf_lines[index + i] + "\n"
    return drugInfo
    
        
def getWhatIsInLeafLetSection(pdf_lines , lang):
    if lang == "en":
        find_line = "Package leaflet: Information for the user"
    else:
        find_line = translations["Package leaflet: Information for the user"]
    biggest = 0
    whatIsInLeafLetSection = []
    startToEnd = (0 , 0)
    for i ,line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line, find_line)
        if similarity_ratio > biggest:
            biggest = similarity_ratio
            index = i
        if similarity_ratio >= 0.9:
            break
    counter = 0
    first_section_index = 0
    for i , line in enumerate(pdf_lines):
        if i < index:
         continue
        line = line.strip()
        if line[:1] == "1":
            first_section_index = i
            break
    for i , line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line, pdf_lines[first_section_index])
        if similarity_ratio > 0.85:
            counter += 1
        if counter == 2:
            startToEnd = (first_section_index, i)
            break
    for i in range(startToEnd[0], startToEnd[1]):
        whatIsInLeafLetSection.append(pdf_lines[i])
    finalLines = []
    for i , line in enumerate(whatIsInLeafLetSection):
        if str.isdigit(line[:1]):
            finalLines.append(line)
        else:
            try:
                finalLines[i - 1] += line
            except:
                print("Error adding line to what is a leaflet section")
    whatIsInLeafLetSection = finalLines
    return whatIsInLeafLetSection , startToEnd[1]

def chunkLeafLetSectionsIndexes(sections , sections_contnet):
    extactFromIndexes = []
    excractedChunks = []
    # ("line" , "original Index in chunks[]")
    for i_Extracted_chunk , line in enumerate(sections_contnet):
        excractedChunks.append((line , i_Extracted_chunk))
    for i , line in enumerate(sections):
        for i_Extracted_chunk , extracted_chunk in enumerate(excractedChunks):
            stripped = extracted_chunk[0].strip()
            if stripped[:1].isdigit() == False:
                continue
            if (stripped[:1] != line[:1]) or len(line) < 12 or len(stripped) < 12:
                continue
            similarity_ratio = semantic_similarity(line, extracted_chunk[0])
            print(line , extracted_chunk[0] , similarity_ratio)
            if similarity_ratio >= 0.7:
                extactFromIndexes.append(extracted_chunk[1])
                excractedChunks = excractedChunks[i_Extracted_chunk:]
                break
    return extactFromIndexes


def getLeafLetSections(indexes , sections_contnet):
    leafLetSections = []
    for i , line in enumerate(indexes):
        if i == len(indexes) - 1:
            leafLetSections.append(sections_contnet[line : ])
            break
        leafLetSections.append(sections_contnet[line : indexes[i + 1]])
    return leafLetSections


# def createJsonFile(leafLetSectionsReady , header , routes ,legal_supply_status, MAH_details,header_section_txt,extra_parts, output_file):
#     my_data = {}
#     section_codes= get_section_codes()
#     for i , section in enumerate(leafLetSectionsReady):
#         if i > 5:
#           my_data.update({f"section{i + 1}": {"content":section, "code": "N/A", "display": "N/A"}})
#         else:
#           print(section_codes[i]["section-code"])
#           my_data.update({f"section{i + 1}": {"content":section, "code": section_codes[i]["section-code"], "display": section_codes[i]["display-value"]}})
#     my_data.update({"header": header})
#     my_data.update({"routes": routes})
#     my_data.update({"header_section": {"content":header_section_txt , "code":"68498-5" , "display": "PATIENT MEDICATION INFORMATION SECTION"}})
#     my_data.update(extra_parts)
#     my_data.update({"MAH_details": MAH_details})
#     my_data.update({"legalSupplyStatus": legal_supply_status})
#     json_string = json.dumps(my_data)
#     filename = f"{output_file}.json"
#     with open(filename, "w") as json_file:
#       json_file.write(json_string)
# pdf_file_path = 'amoxicillin.pdf'


# def main(pdf_path):
#     pdf_lines = pdf_to_array(pdf_path)
#     drug_chunk = get_drug_info(pdf_lines)
#     header = get_header_LLM(drug_chunk)
#     print(header)
#     whatIsInLeafLetSection , end = getWhatIsInLeafLetSection(pdf_lines)
#     header_section_txt = get_header_section(pdf_lines , whatIsInLeafLetSection)
#     leagal_supply_status = determineStatusOfSupply(pdf_lines)
#     sections_contnet = pdf_lines[end:]
#     leafLetSectionsIndexes = chunkLeafLetSectionsIndexes(whatIsInLeafLetSection , sections_contnet)
#     leafLetSections = getLeafLetSections(leafLetSectionsIndexes , sections_contnet)
#     last_section = leafLetSections[-1]
#     first_section = leafLetSections[0]
#     active_substance = header.get("active_substances")
#     time.sleep(0.3)
#     if len(active_substance) == 1:
#         atc_codes = get_final_codes(first_section , active_substance[0])
#         if len(atc_codes) > 0:
#           header.update({"atc_code": atc_codes})
#     print(last_section)
#     last_section_part ,MAH_part , MAH_details = get_MAH_Details_LLM(last_section)
#     MAH_details = getValidJson(MAH_details)
#     leafLetSections[-1] = last_section_part
#     leafLetSections.append(MAH_part)
#     routes = get_adminstration_routes_array(header.get("Invented name") , leafLetSections)
#     extra_parts = get_extra_parts(leafLetSections)
#     createJsonFile(leafLetSections , header , routes , leagal_supply_status,MAH_details , header_section_txt,extra_parts,pdf_file_path)

# main(pdf_file_path)
# pdf_lines = pdf_to_array(pdf_file_path)
# for i , line in enumerate(pdf_lines):
#     print(i , line)
#     time.sleep(0.5)
# print(get_header_section(pdf_lines))
# print(pdf_lines)
# print(getWhatIsInLeafLetSection(pdf_lines))
# print(pdf_lines)
# drug_chunk = get_drug_info(pdf_lines)
# print(drug_chunk)
# header = getValidJson(get_header_LLM(drug_chunk))
# print(header)

def end_result_JSON(html_sections , header , routes ,legal_supply_status, MAH_details,header_section,what_is_in_this_leaflet_html_section,extra_parts):
    my_data = {}
    my_data.update({"sections": html_sections ,"header": header , "routes": routes , "legalSupplyStatus": legal_supply_status , "MAH_details": MAH_details , "header_section": header_section , "what_is_in_this_leaflet_section": what_is_in_this_leaflet_html_section , "extra_parts": extra_parts})
    # my_data.update({"header": header})
    # my_data.update({"routes": routes})
    # my_data.update({"header_section": header_section})
    # my_data.update({"what_is_in_this_leaflet_section": what_is_in_this_leaflet_html_section})
    # my_data.update(extra_parts)
    # my_data.update({"MAH_details": MAH_details})
    # my_data.update({"legalSupplyStatus": legal_supply_status})
    return my_data


def get_PIL(pdf_lines  , lang):
    drug_chunk = get_drug_info(pdf_lines , lang)
    header = get_header_LLM(drug_chunk)
    print(header)
    whatIsInLeafLetSection , end = getWhatIsInLeafLetSection(pdf_lines , lang)
    leagal_supply_status = determineStatusOfSupply(pdf_lines)
    header_section = get_header_html_section(pdf_lines , leagal_supply_status)
    what_is_in_this_leaflet_html_section =get_what_is_in_this_leaflet_html_section(whatIsInLeafLetSection)
    sections_contnet = pdf_lines[end:]
    leafLetSectionsIndexes = chunkLeafLetSectionsIndexes(whatIsInLeafLetSection , sections_contnet)
    leafLetSections = getLeafLetSections(leafLetSectionsIndexes , sections_contnet)
    last_section = leafLetSections[-1]
    first_section = leafLetSections[0]
    active_substance = header.get("active_substances")
    if bool(active_substance) and len(active_substance) == 1:
        atc_codes = get_final_codes(first_section , active_substance[0])
        if bool(atc_codes) and len(atc_codes) > 0:
          header.update({"atc_code": atc_codes})
        if bool(atc_codes) and len(atc_codes) == 0:
         header.update({"atc_code": [""]})
        else:
         header.update({"atc_code": [""]})
 
    last_section_part ,MAH_part , MAH_details = get_MAH_Details_LLM(last_section)
    MAH_details = getValidJson(MAH_details)
    leafLetSections[-1] = last_section_part
    leafLetSections.append(MAH_part)
    html_sections , mah_section = get_sections_html(leafLetSections , whatIsInLeafLetSection)
    routes = get_adminstration_routes_array(header.get("Invented name") , leafLetSections)
    extra_parts = get_extra_parts(leafLetSections)
    result = end_result_JSON(html_sections , header , routes , leagal_supply_status,MAH_details , header_section,what_is_in_this_leaflet_html_section,extra_parts)
    return result




