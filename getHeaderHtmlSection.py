from extractUtils import clean_xml_html
from semantic import semantic_similarity

translations = {
    "Package leaflet: Information for the user": "نشرة العبوة : معلومات المريض" ,
    "What is in this leaflet" : "محتويات هذه النشرة",
    "Read all of this leaflet carefully before you start taking this medicine." : "إقرأ كامل النشرة بعنایة قبل البدء باستخدام ھذا الدواء.",
    

}


def get_header_html_section(header_section,lang = "en" or "ar"):
    if lang == "ar":
        header_title = translations["Read all of this leaflet carefully before you start taking this medicine."]
    else:
        header_title = "Read all of this leaflet carefully before you start taking this medicine." 
    highest_similarity = 0
    found_index = 0
    for i , line in enumerate(header_section):
     simalirity = semantic_similarity(line, header_title, lang)
     if simalirity > highest_similarity or simalirity >= 0.95:
        highest_similarity = simalirity
        found_index = i
        if simalirity >= 0.95:
            break
    lines = ""
    for i , line in enumerate(header_section[found_index + 1:]):
        lines += f"<li>{line}</li>" 
    print(lines)

    html = f"""
  <div xmlns="http://www.w3.org/1999/xhtml"><p>{header_title}</p><ul>{lines}</ul></div>
"""
    for i , line in enumerate(header_section):
        if i != found_index:
            html += f"<p>{line}</p>"
    html = clean_xml_html(html.strip())
    result = {"html":html,"code":"68498-5","title":header_title ,"system": "http://loinc.org","display":"PATIENT MEDICATION INFORMATION"}
    return result


def get_what_is_in_this_leaflet_html_section(what_is_in_this_leaflet , lang = "en" or "ar"):
    if lang == "ar":
        insert_translation = translations["What is in this leaflet"]
    else:
        insert_translation = "What is in this leaflet" 
    formatted_html_list = ""
    for line in what_is_in_this_leaflet:
        line = line[2:].strip()
        formatted_html_list += f"<li>{line}</li>"
    html = f"""<div xmlns="http://www.w3.org/1999/xhtml"><p><b>{insert_translation}</b></p><ol>{formatted_html_list}</ol></div>"""
    html = clean_xml_html(html.strip())
    result = {"html":html ,"title": insert_translation}
    return result
        
