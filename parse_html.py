

from bs4 import BeautifulSoup



def get_parsed_html(html_content : str):
    soup = BeautifulSoup(html_content, 'html.parser')

    extracted_texts = []

    for element in soup.find_all(True): # Find all tags
    # Process direct text within the tag, excluding script/style content
        if element.name not in ['script', 'style']:
            # Iterate over all NavigableString children (text nodes)
            for text_node in element.find_all(string=True, recursive=False):
                stripped_text = text_node.strip()
                if stripped_text:
                # .sourceline gives the line number of the opening tag in the original parsed document
                    line_number = text_node.parent.sourceline
                    tag = element
                    extracted_texts.append({"line": line_number, "text": stripped_text , "fullElement" : element})

# To handle cases where text might be split across multiple lines within a tag or
# if a more precise line number for the actual text is needed,
# we can refine by searching the text in the read lines.
# For this iteration, parent.sourceline is a good starting point.

# Remove duplicate entries that might arise from nested structures if text is reported multiple times
    html_parsed = []
    seen_texts_at_lines = set()

    for item in extracted_texts:
        identifier = (item["line"], item["text"])
        if identifier not in seen_texts_at_lines:
            html_parsed.append(item)
            seen_texts_at_lines.add(identifier)

# Sort by line number
    html_parsed.sort(key=lambda x: x["line"])
    return html_parsed , soup



def replace_page_content(newContent , fullHtml):
    page_div = fullHtml.find('div', attrs={'class': 'page'})
    if page_div:
        new_soup = BeautifulSoup(newContent, 'html.parser')
        page_div.clear()

        if new_soup.body:
            for child_element in list(new_soup.body.contents):
                page_div.append(child_element.extract())
        else:
            for element in list(new_soup.contents): 
                page_div.append(element.extract())
    
