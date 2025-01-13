from peewee import *
import ollama
import os
from clientgpt import generate_gpt_max_token
from dotenv import load_dotenv
load_dotenv()
db_name = os.getenv("db_name")
user = os.getenv("db_user")
password = os.getenv("db_password")
host = os.getenv("db_host")
port = os.getenv("db_port")
db = PostgresqlDatabase(db_name, user=user, password=password, host=host, port=port)
class Medicine(Model):
    atc_code = CharField()
    atc_name = CharField()
    class Meta:
        database = db
A = "A.Alimentary tract and metabolism"
B = "B.Blood and blood forming organs"
C = "C.Cardiovascular system"
D = "D.Dermatologicals"
G = "G.Genito-urinary system and sex hormones"
H = "H.Systemic hormonal preparations,excluding sex hormones and insulins"
J = "J.Anti-Infectives for systemic use"
L = "L.Antineoplastic and immunomodulating agents"
M = "M.Musculo-Skeletal system"
N = "N.Nervous system"
P = "P.Anti parasitic products,insecticides and repellents"
Q = "Q.Verterinary Drugs"
R = "R.Respiratory system"
S = "S.Sensory organs"
V = "V.Various"
firstLevel = [("A", A) , ("B", B), ("C", C), ("D", D), ("G", G), ("H", H), ("J", J), ("L", L), ("M", M), ("N", N), ("P", P), ("Q", Q), ("R", R), ("S", S), ("V", V)]
list_salts_that_dont_affect_atc = ["sodium" , "maleate" , "hydrochloride"]
model = os.getenv("model")
def get_possible_atc_codes(atc_name):
    ## check if the salt is in the list of salts that dont affect the atc code and remove it from atc_name for better search
    atc_name_array = atc_name.lower().split()
    for salt in list_salts_that_dont_affect_atc:
     if len(atc_name_array) == 2 and atc_name_array[1] == salt:
      atc_name = atc_name_array[0]
    codes = []

    for med in Medicine.select().where(Medicine.atc_name == atc_name.lower()):
      codes.append((med.atc_code,med.atc_name))
    possible_codes = []
    for drug in codes:
      char = drug[0][0][0]
      for level in firstLevel:
        if char == level[0]:
            possible_codes.append(level[1])
            break
    return possible_codes , codes

def check_codes_one(codes):
    if len(codes) == 1:
     return [codes[0][0]]
    return None
    
def get_final_codes(firstSection , atc_drug_name):
  prompt = ""
  categories = ""
  for section in firstSection:
    prompt += section
  possible_categories , codes = get_possible_atc_codes(atc_drug_name)
  for category in possible_categories:
    categories += f"{category}\n"
  code = check_codes_one(codes)
  if code:
    return code
  system = f"""
    User will provide what a specific medical product is used for you will determine which category it falls under depending on its therapeutic effect.
    Only respond with the character of the category you determined.
    The possible categories are:
    {categories}"""
  # response = ollama.generate(model=model , system=system, prompt=prompt , options = {"num_predict": 1})
  response = generate_gpt_max_token(prompt , system , 1)
  print("letter code atc" , response)
  final_codes =[]
  for code in codes:
    print("code" , code[0][0])
    if code[0][0] == response:
      final_codes.append(code[0])
  print("final codes" , final_codes)
  return final_codes



