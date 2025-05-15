from difflib import SequenceMatcher
import re
import json
def extract_div_contents(html_string):
    # Regular expression pattern to match <div>...</div> including nested divs
    pattern = re.compile(r'<div.*?>.*?</div>', re.DOTALL)
    
    # Find all matches in the input string
    div_contents = pattern.findall(html_string)
    if len(div_contents) == 0:
        return None
    return div_contents[0]

def delete_before_value(input_string, value):
    """
    Removes the first occurrence of a specific value and everything before it in the input string.
    
    Parameters:
    - input_string (str): The string to process.
    - value (str): The specific value to find and delete along with everything before it.

    Returns:
    - str: The modified string with the value and everything before it removed.
            If the value is not found, the original string is returned.
    """
    # Find the index of the specific value
    index = input_string.lower().find(value.lower())
    
    # If the value is not found, return the original string
    if index == -1:
        return input_string
    
    # Return the string from the end of the specific value onwards
    return value + input_string.lower()[index + len(value.lower()):]
def truncate_string(input_string, target_value):
    index = input_string.lower().find(target_value.lower())
    if index != -1:
        return input_string[:index]
    else:
        return input_string
    
def truncate_string_second_occurrence(input_string, target_value):
    first_index = input_string.lower().find(target_value.lower())
    if first_index != -1:
        second_index = input_string.lower().find(target_value.lower(), first_index + 1)
        if second_index != -1:
            return input_string[:second_index]
    return input_string
"".find("")

def remove_extra_spaces(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Join the words back together with a single space
    cleaned_sentence = ' '.join(words)

    return cleaned_sentence

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

    
def check_similarity(sentence1, sentence2):
    # Calculate the similarity ratio between the two sentences
    sentence1 = remove_extra_spaces(sentence1).lower()
    sentence2 = remove_extra_spaces(sentence2).lower()
    similarity_ratio = similar(sentence1, sentence2)
    # Return True if the similarity ratio is above a certain threshold, False otherwise
    return similarity_ratio

def check_similarity_with_match_word_length_in_sentence(line_one , line_two):
    line_one = remove_extra_spaces(line_one)
    line_two = remove_extra_spaces(line_two)
    line_one = line_one.lower().split()
    line_two = line_two.lower().split()
    delimeter = " "
    if len(line_one) == len(line_two):
        similarity_ratio = similar(delimeter.join(line_one), delimeter.join(line_two))
        return similarity_ratio
    if len(line_one) > len(line_two):
        similarity_ratio = similar(delimeter.join(line_two), delimeter.join(line_one[:len(line_two)]))
        return similarity_ratio
    else:
        return similar(delimeter.join(line_one), delimeter.join(line_two[:len(line_one)]))
    
def clean_xml_html(xml_string):
    if xml_string is None:
        return
    cleaned_xml = re.sub(r'>[\n\t ]+<', '><', xml_string)
    return cleaned_xml
