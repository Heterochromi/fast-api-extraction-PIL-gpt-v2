# import fitz  # PyMuPDF

# def find_emphasized_value(pdf_path, target_value):
#     doc = fitz.open(pdf_path)
    
#     for page_num in range(len(doc)):
#         page = doc[page_num]
        
#         # Extract text with style information
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             if "lines" in block:
#                 for line in block["lines"]:
#                     for span in line["spans"]:
#                         if target_value.lower() in span["text"].lower():
#                             # Check if the font is bold
#                             if "bold" in span["font"].lower():
#                                 print(f"Found bolded '{target_value}' on page {page_num + 1}")
#                                 return True
    
#     print(f"'{target_value}' found in the document, but not emphasized")
#     return False

# # Usage
# pdf_path = "chunking/ZITHROMAX.pdf"
# target_value = "Zanaflex may cause drowsiness or dizziness"
# print(find_emphasized_value(pdf_path, target_value))

# tables = camelot.read_pdf('chunking/Baclofen.pdf')
import tabula

# dfs = tabula.read_pdf("chunking/Baclofen.pdf", pages='all')
# tabula.convert_into("chunking/Baclofen.pdf", "output.json", output_format="json", pages='all')
# print(dfs)
dfs = tabula.read_pdf("chunking/Baclofen.pdf", pages='all')
# Convert each DataFrame to a JSON object
json_data = [df.to_json(orient='records') for df in dfs]

# Save the JSON data to a file (e.g., "output.json")
with open("output.json", "w") as json_file:
    for record in json_data:
        json_file.write(record + '\n')