from semantic import semantic_similarity

from parse_html import get_parsed_html , replace_page_content


translations = {
    "Package leaflet: Information for the user": "نشرة العبوة : معلومات المريض" ,
    "What is in this leaflet" : "في هذه النشرة",

}

sections = [
    {
      "section-code": "34067-9",
      "display-value": "INDICATIONS & USAGE",
      "PIL_section": "1. What is {invented name} and what it is used for"
    },
    {
      "section-code": "34070-3",
      "display-value": "CONTRAINDICATIONS",
      "PIL_section": "2. What you need to know before you take {invented name}"
    },
    {
      "section-code": "34068-7",
      "display-value": "DOSAGE & ADMINISTRATION",
      "PIL_section": "3. How to take {invented name}"
    },
    {
      "section-code": "34084-4",
      "display-value": "ADVERSE REACTIONS",
      "PIL_section": "4. Possible side effects"
    },
    {
      "section-code": "44425-7",
      "display-value": "STORAGE AND HANDLING",
      "PIL_section": "5. How to store {invented name}"
    },
    {
      "section-code": "43678-2",
      "display-value": "DOSAGE FORMS & STRENGTHS",
      "PIL_section": "6. Further information"
    }
  ]


def splitLeaflet(pdf_lines , lang = "en" or "ar"):
    if lang == "en":
        find_line = "What is in this leaflet"
    else:
        find_line = translations["What is in this leaflet"]


    #split the lines to header_content,what_is_in_this_leaflet_content,main_content
    found_what_is_in_this_leaflet_section_start_index = 0
    highest_similarity = 0.0
    for i , line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line['text'], find_line , lang=lang)
        if (similarity_ratio > highest_similarity) or (similarity_ratio >= 0.95):
            highest_similarity = similarity_ratio
            found_what_is_in_this_leaflet_section_start_index = i
        if similarity_ratio >= 0.95:
            break
        

    #here is the everything before the "What is in this leaflet" section
    header_content = pdf_lines[:found_what_is_in_this_leaflet_section_start_index]



    #find the first line after "What is in this leaflet" and then find where it replicates to determine where this section ends
    line_after_what_is_in_this_leaflet = pdf_lines[found_what_is_in_this_leaflet_section_start_index + 1]
    highest_similarity = 0.0
    linesZ_after_what_is_in_this_leaflet = pdf_lines[found_what_is_in_this_leaflet_section_start_index+2:]
    for i , line in enumerate(linesZ_after_what_is_in_this_leaflet):
        similarity_ratio = semantic_similarity(line['text'], line_after_what_is_in_this_leaflet['text'] , lang=lang)
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
            similarity_ratio = semantic_similarity(current_section['text'], line['text'] , lang=lang)
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

    what_is_in_this_leaflet_content.insert(0, pdf_lines[found_what_is_in_this_leaflet_section_start_index])
    return header_content , what_is_in_this_leaflet_content , all_sections




def addDivSeperationTags(all_sections):
    for i , section in enumerate(sections):
        n_section = all_sections[i]
        n_section[0]['fullElement'] = f""" <div code="{section['section-code']}" display="{section['display-value']}" title="{section['PIL_section']}">""" + str(n_section[0]['fullElement'])
        n_section[-1]['fullElement'] = str(n_section[-1]['fullElement']) + "</div>"



    # "section-code": "68498-5",
    # "display-value": "PATIENT MEDICATION INFORMATION",
    # "PIL_section": "header"


def addDivSeperationHeader(header_content , what_is_in_section):
    header_content[0]['fullElement'] = f""" <div code="68498-5" display="PATIENT MEDICATION INFORMATION" title="header">""" + str(header_content[0]['fullElement'])
    header_content[-1]['fullElement'] = str(header_content[-1]['fullElement']) + "</div>"

    what_is_in_section[0]['fullElement'] = f""" <div code="68498-5" display="PATIENT MEDICATION INFORMATION" title="What is in this leaflet">"""  + str(what_is_in_section[0]['fullElement'])
    what_is_in_section[-1]['fullElement'] = str(what_is_in_section[-1]['fullElement']) + "</div>"




def splitHtml(content : str , lang = "en"):
    parsed , fullHtml = get_parsed_html(content)
    header_content , what_is_in_this_leaflet_content , all_sections = splitLeaflet(parsed , lang)
    addDivSeperationHeader(header_content , what_is_in_this_leaflet_content)
    addDivSeperationTags(all_sections)

    collect_final_output = []

    for item in header_content:
      collect_final_output.append(item['fullElement'])

    for item in what_is_in_this_leaflet_content:
        collect_final_output.append(item['fullElement'])

    for list in all_sections:
        for item in list:
            collect_final_output.append(item['fullElement']) 
    final_html_result = "" 
    for element in collect_final_output:
        final_html_result += str(element) + "\n"


    replace_page_content(final_html_result , fullHtml)

    return str(fullHtml)


