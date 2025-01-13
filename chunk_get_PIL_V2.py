from semantic import semantic_similarity
from getSectionHtml import get_sections_html
from getHeaderHtmlSection import get_what_is_in_this_leaflet_html_section ,get_header_html_section
from determineStatusOfSupply import determineStatusOfSupply 
from getHeaderUsingLLM import get_header_LLM
from getMahSection import get_MAH_Details_LLM
from getRoutes import get_adminstration_routes_array
from getAtcCode import get_final_codes


translations = {
    "Package leaflet: Information for the user": "نشرة العبوة : معلومات المريض" ,
    "What is in this leaflet" : "في هذه النشرة",

}

def splitLeaflet(pdf_lines , lang = "en" or "ar"):
    if lang == "en":
        find_line = "What is in this leaflet"
    else:
        find_line = translations["What is in this leaflet"]


    #split the lines to header_content,what_is_in_this_leaflet_content,main_content
    
    highest_similarity = 0.0
    for i , line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line, find_line , lang=lang)
        if (similarity_ratio > highest_similarity) or (similarity_ratio >= 0.95):
            highest_similarity = similarity_ratio
            start = i
        if similarity_ratio >= 0.95:
            break
        

    #here is the everything before the "What is in this leaflet" section
    header_content = pdf_lines[:start]



    #find the first line after "What is in this leaflet" and then find where it replicates to determine where this section ends
    line_after_what_is_in_this_leaflet = pdf_lines[start + 1]
    highest_similarity = 0.0
    linesZ_after_what_is_in_this_leaflet = pdf_lines[start+2:]
    for i , line in enumerate(linesZ_after_what_is_in_this_leaflet):
        similarity_ratio = semantic_similarity(line, line_after_what_is_in_this_leaflet , lang=lang)
        if (similarity_ratio > highest_similarity) or (similarity_ratio >= 0.95):
            highest_similarity = similarity_ratio
            end = i
        if similarity_ratio >= 0.95:
           break

    what_is_in_this_leaflet_content = linesZ_after_what_is_in_this_leaflet[:end]

    what_is_in_this_leaflet_content.insert(0,line_after_what_is_in_this_leaflet)

    main_content = linesZ_after_what_is_in_this_leaflet[end:]




    #find the all the indexes of the sections in the main content
    indexes = []
    last_index = 0
    start = 0
    for i, current_section in enumerate(what_is_in_this_leaflet_content):
        index = None
        highest_similarity = 0.0
        for j , line in enumerate(main_content):
            if j < last_index:
                break
            similarity_ratio = semantic_similarity(current_section, line , lang=lang)
            print(current_section, line , similarity_ratio , highest_similarity)
            if similarity_ratio > highest_similarity or similarity_ratio >= 0.95:
                highest_similarity = similarity_ratio
                index = j
            if similarity_ratio >= 0.95:
                break
        start = index
        indexes.append(index)



    #split the main content to sections
    all_sections = []
    for i , section_index in enumerate(indexes):
        if i == len(indexes) - 1:
            all_sections.append(main_content[section_index:])
        else:
            all_sections.append(main_content[section_index:indexes[i+1]])


    #seperate last section from the manafacturer details if possible
    MAH_section = []
    check_list = ["Marketing Authorisation Holder and Manufacturer","MAH","Marketing Authorisation Holder","HOLDER", "Manufacturer" , "Manufactured" , "Trademark", "المصنع" , "مالك حقوق التسویق" ,"التسويق" , "شركة"]	
    for i , section_line in enumerate(all_sections[-1]):
        for check in check_list:
            if check in section_line:
                MAH_section = all_sections[-1][i:]
                all_sections[-1] = all_sections[-1][:i]
                break

    return header_content , what_is_in_this_leaflet_content , all_sections, MAH_section

def get_PIL(content , lang = "en"):
    result = {}
    try:
      header_content , what_is_in_this_leaflet_content , all_sections, MAH_section = splitLeaflet(content , lang=lang)
    except(Exception) as e:
        print (e)
        return {"error": "error in splitting the leaflet , please check if the content is in the correct PIL format"}
    
    try:
        supply_status = determineStatusOfSupply(header_content)
        result.update({"legalSupplyStatus": supply_status})
        what_is_in_this_leaflet_content_html = get_what_is_in_this_leaflet_html_section(what_is_in_this_leaflet_content , lang=lang)
        result.update({"what_is_in_this_leaflet_section": what_is_in_this_leaflet_content_html})
        header_section = get_header_html_section(header_content , lang=lang)
        result.update({"header_section": header_section})
    except(Exception) as e:
        if bool(what_is_in_this_leaflet_content) == False:
          result.update({"what_is_in_this_leaflet_section": None})
        if bool(header_section) == False:
            result.update({"header_section": None})
        if bool(supply_status) == False:
            result.update({"legalSupplyStatus": None})
        print (e , {"error": "failed to generate header section details"})

    try:
        header = get_header_LLM(header_content)
        result.update({"header": header})
    except(Exception) as e:
        print (e , {"error": "failed to generate header section details"})
        result.update({"header": None})
    
    try:
        active = header.get("active_substances")
        if len(active) > 0:
            ValueError("multiple active substances found , complex PIL or wrongly detected substances")
        atc_code = get_final_codes(all_sections[0] , active[0])
        result.update({"atc_code": atc_code})
    except(Exception) as e:
        result.update({"atc_code": None})
        print (e , {"error": "failed to get ATC code"})

    try:
        routes = get_adminstration_routes_array(all_sections)
        result.update({"routes": routes})
    except(Exception) as e:
        result.update({"routes": None})
        print (e , {"error": "failed to get routes"})
    try:
        if len(MAH_section) > 0:
            MAH_details = get_MAH_Details_LLM(MAH_section)
        else:
            MAH_details= get_MAH_Details_LLM(all_sections[-1])
        result.update({"MAH_details": MAH_details})
    except(Exception) as e:
        result.update({"MAH_details": None})
        print (e , {"error": "failed to get MAH details"})
    
    
    # get the html of the sections
    try:
        html_sections = get_sections_html(all_sections , what_is_in_this_leaflet_content)
        result.update({"sections": html_sections})
    except(Exception) as e:
        result.update({"sections": "failed to geenrate sections"})
        print (e , {"error": "failed to generate HTML"})
    print(result)
    
    # result.update({"sections": html_sections ,"header": header , "routes": routes ,"atc_code": atc_code , "legalSupplyStatus": supply_status , "MAH_details": MAH_details , "header_section": header_section , "what_is_in_this_leaflet_section": what_is_in_this_leaflet_content_html })
    return 


def get_PIL_ar(content , lang = "ar"):
    result = {}
    try:
      header_content , what_is_in_this_leaflet_content , all_sections, MAH_section = splitLeaflet(content , lang=lang)
    except(Exception) as e:
        print (e)
        return {"error": "error in splitting the leaflet , please check if the content is in the correct PIL format"}
    

    try:
        supply_status = determineStatusOfSupply(header_content)
        result.update({"legalSupplyStatus": supply_status})
        what_is_in_this_leaflet_content_html = get_what_is_in_this_leaflet_html_section(what_is_in_this_leaflet_content , lang=lang)
        result.update({"what_is_in_this_leaflet_section": what_is_in_this_leaflet_content_html})
        header_section = get_header_html_section(header_content , lang=lang)
        result.update({"header_section": header_section})
    except(Exception) as e:
        if bool(what_is_in_this_leaflet_content) == False:
          result.update({"what_is_in_this_leaflet_section": None})
        if bool(header_section) == False:
            result.update({"header_section": None})
        if bool(supply_status) == False:
            result.update({"legalSupplyStatus": None})
        print (e , {"error": "failed to generate header section details"})

    try:
        header = get_header_LLM(header_content)
        result.update({"header": header})
    except(Exception) as e:
        print (e , {"error": "failed to generate header section details"})
        result.update({"header": None})
    
    #get the html of the sections
    try:
        html_sections = get_sections_html(all_sections , what_is_in_this_leaflet_content)
        result.update({"sections": html_sections})
    except(Exception) as e:
        result.update({"sections": "failed to geenrate sections"})
        print (e , {"error": "failed to generate HTML"})
    print(result)
    # print(header_html)

    # #all header section details
    result.update({"Mah_deatils":None , "routes":None})

    # result.update({"header": header , "routes": routes , "legalSupplyStatus": supply_status , "MAH_details": MAH_details , "header_section": header_section , "what_is_in_this_leaflet_section": what_is_in_this_leaflet_content_html })








