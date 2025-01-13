# from peewee import *
# import ollama
# db = PostgresqlDatabase('railway', user='postgres', password='fnwkaQqTemcpGCXTrUyKqFaqgLFBjrZi', host='http://junction.proxy.rlwy.net', port=30005)

# db.connect()

# class Medicine(Model):
#     atc_code = CharField()
#     atc_name = CharField()
#     class Meta:
#         database = db
# A = "A.Alimentary tract and metabolism"
# B = "B.Blood and blood forming organs"
# C = "C.Cardiovascular system"
# D = "D.Dermatologicals"
# G = "G.Genito-urinary system and sex hormones"
# H = "H.Systemic hormonal preparations,excluding sex hormones and insulins"
# J = "J.Anti-Infectives for systemic use"
# L = "L.Antineoplastic and immunomodulating agents"
# M = "M.Musculo-Skeletal system"
# N = "N.Nervous system"
# P = "P.Anti parasitic products,insecticides and repellents"
# Q = "Q.Verterinary Drugs"
# R = "R.Respiratory system"
# S = "S.Sensory organs"
# V = "V.Various"
# firstLevel = [("A", A) , ("B", B), ("C", C), ("D", D), ("G", G), ("H", H), ("J", J), ("L", L), ("M", M), ("N", N), ("P", P), ("Q", Q), ("R", R), ("S", S), ("V", V)]

# def get_ATC_code():
#     codes = []
#     for med in Medicine.select().where(Medicine.atc_name == 'ketoconazole'):
#       codes.append((med.atc_code,med.atc_name))
#     possible_codes = []
#     for drug in codes:
#       char = drug[0][0][0]
#       for level in firstLevel:
#         if char == level[0]:
#             possible_codes.append(level[1])
#             break
#     print(possible_codes , codes)
#     if len(possible_codes) == 1:
#      print(possible_codes , codes)
#      return
#     system = f"""
#     User will provide what a specific medical product is used for you will determine which category it falls under depending on its theraputic effect.
#     Only respond with the character of the category you determined.
#     The possible categories are:
#     {possible_codes}
#      """
#     prompt = """
#     1. What Ketoconazole HRA is and what it is used for
# Ketoconazole HRA is a medicine that contains the active substance ketoconazole. It is used to treat endogenous
# Cushing’s syndrome (when the body produces an excess of cortisol) in adults and adolescents above the age
# of 12 years.
# Cushing’s syndrome is caused by overproduction of a hormone called cortisol which is produced by the adrenal
# glands. Ketoconazole HRA is able to block the activity of the enzymes responsible for the synthesis of cortisol
# and consequently is able to decrease the over-production of cortisol by your body and to improve the symptoms
# of Cushing’s syndrome. 
#     """
#     return system , prompt
    

# system  , prompt = get_ATC_code()

# def get_header_LLM(prompt):
#       response = ollama.chat(model='llama3.1:8b-instruct-q8_0', messages=[{'role': 'system','content': system,},{'role': 'user','content': prompt}])
#       return response['message']['content']



# response = get_header_LLM(prompt)
# print(response)





# ketoconazole = Medicine.get(Medicine.atc_name == 'ketoconazole')
# print(ketoconazole.atc_code)

# for med in Medicine.select().where(Medicine.atc_name.contains('ketoconazole')):
#     print(med.atc_name)



# atc_name =  "Diclofenac sodium"

# atc_name = atc_name.lower().split()
# if len(atc_name) == 2 and atc_name[1] == "sodium":
#     atc_name = atc_name[0]

# print(atc_name)
    


# sectionsFile=open("programatic-extraction/section.txt","r")
# print(sectionsFile.read())


# import json

# with open('programatic-extraction/sectionCodes.json', 'r') as json_file:
#     data = json.load(json_file)
#     print(len(data["sections"]))  
# from peewee import *
# db = PostgresqlDatabase('postgres', user='admin', password='root', host='localhost', port=5432)
# class Routes(Model):
#     code = CharField()
#     display = CharField()
#     class Meta:
#         database = db
# db.connect()
# for route in Routes.select().where(Routes.display.ilike(f"%{"cardio"}%")):
#   print(route.display , route.code)

# from extractUtils import check_similarity

# check = check_similarity("Eye drops, solvent for reconstitution", "eye drops")

# print(check)

# from extractUtils import getValidJson

# extra_parts = {
#         "intended_uses" : [],
#         "target_populations" : [],
#         "flavor" : []
#     }

# print(getValidJson(extra_parts))

stuff = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
for i, line in enumerate(stuff, start=3):
    print(i , line)
# import json
# import PyPDF2
# from extractUtils import remove_extra_spaces

# def pdf_to_array(pdf_path):
#     lines = []
#     # Open the PDF file
#     with open(pdf_path, 'rb') as file:
#         # Create a PDF reader object
#         pdf_reader = PyPDF2.PdfReader(file)
        
#         # Iterate through all pages
#         for page in pdf_reader.pages:
#             # Extract text from the page
#             text = page.extract_text()
#             # text = remove_extra_spaces(text)
            
#             # Split the text into lines and add to the array
#             lines.extend(text.split('\n'))
#     for i , line in enumerate(lines):
#         lines[i] = remove_extra_spaces(line)

#     return lines

# def createJson(pdf_lines):
#     my_data = {}
#     txt = ""
#     my_data.update({"content": pdf_lines})
#     json_string = json.dumps(my_data, ensure_ascii=False)
#     filename = f"test_apigen.json"
#     with open(filename, "w", encoding="utf-8") as json_file:
#         json_file.write(json_string)

# pdf_lines = pdf_to_array("Apigen.pdf")
# print(pdf_lines)
# pdf_lines = """
# أبیجین٪۰٫۳ قطرة عینیة /أذنیة
#  كبریتات الجنتامیسین
# إقرأ كامل النشرة بعنایة قبل البدء باستخدام ھذا الدواء.
# - احتفظ بالنشرة لأنك قد تحتاجھا مرة أخر.
# - اذا كان لدیك أي أسئلة استشر طبیبك أو الصیدلاني .
# - ھذا المستحضر تم وصفھ لك لذا لا تعطیھ لأشخاص آخرین یعانون من نفس الاعراض لأنھ ممكن أن یؤذیھم .
# - عند تفاقم أي اثار جانبیة أو ظھور أي آثار جانبیة غیر مذكورة في النشرة أخبر طبیبك أو الصیدلي.
# في ھذه النشرة :
# .۱ ما ھو أبیجین و ما ھي استعمالاتھ
# .۲ قبل استعمالك أبیجین
# .۳ كیفیة استعمال أبیجین
# ٤ . الآثار الجانبیة المحتملة
# .٥ كیفیة حفظ أبیجین
# .٦ معلومات إضافیة
# -۱ ما ھو أبیجین و ما ھي استعمالاتھ
# أبیجین قطرة عینیة أذنیة معقمة , محفوظة , محلول سائل یستعمل كقطرة عینیة أذنیة . المادة الفعالة في أبیجین
# ھي مضاد حیوي یستعمل لقتل البكتیریا التي تسبب التھاب . یستعمل لسیطرة التھابات العین و الأذن.
# -۲ قبل استعمالك أبیجین.
# لا تستعمل أبیجین
# ِ -إذا كانت لدیك حساسیة لجنتامیسین, أي مكونات أخرى, أو أي مضادات حیویة من مجموعة أمینوجلایكوسید.
#  -إذا كانت طبلة أذنك مثقوبة.
# خذ احتیاطاتك عند استخدام أبیجینإذا كنت تعاني من الوھن العضلي أو ما شابھ ذلك.
# تجنب الاستعمال لفترة طویلة. یجب أن لا تستخدم قطرات في الأذن في حالة تلف طبلة الأذن بأي شكل من الأشكال.
# طبیبك سیقوم بفحص أذنك قبل أن یصرف القطرة، في حالة الالتھاب الشدید یصبح من الضروري استخدام مضاد حیوي
# فموي بالاضافة الى قطرة أبیجین العینیة الأذنیة ، قد یحدث تلف في الأذن خاصة في الافراد الذین یعانون من مشاكل في
# الكلى أو الكبد و كبار السن. ینصح بتوخي الحذر عند استعمال القطرة مع امینوجلایكوساید اخر یعطى عن طریق الحقن.
# ( لا تستعمل قطرة العین مع العدسات اللاصقة ).
# الاستخدام مع الأدویة أخرى
# أخبر الطبیب قبل استعمال القطرة إذا كنت تأخذ أي أدویة أخرى . بالأخص:
# - السیفالوسبورینات، الأمفوتریسین، السیكلوسبورین، سیسبلاتین والتي قد تزید من خطر الفشل الكلوي.
# - مدرات البول مثل حمض الإیثاكرینیك أو فیوروسیماید التي قد تزید من خطر وقوع أضرار على الأذن
# - الأدویة من نوع الكورار التي تعمل على إرخاء العضلات.
# الحمل والرضاعة
# إسأل الطبیب أو الصیدلاني قبل استعمال أي دواء أخر .
# یجب أن لاتستعمل القطرة خلال فترة الحمل والرضاعة ما لم یصفھ الطبیب لك.
# القیادة و استخدام الآلات
# لا یوجد تقریر یثبت وجود أي تأثیر على القیادة و استخدام الآلات مع ذلك لا تقود أو تستعمل الآلات إذا كنت تعاني
# من عدم وضوح في الرؤیة بعد استعمال القطرة العینیة . انتظر حتى توضح الرؤیة قبل القیادة و استعمال الآلات.
# -۳ ما ھي طریقة استعمال أبیجین/ قطرة عینیة أذنیة
# استعمل أبیجین كما وصفھ لك الطبیب . یجب مراجعة طبیبك أو صیدلي إذا كنت غیر متأكد من استخدامھ .
# الجرعة:
# ً
# العین: (۲-۱) قطرة داخل العین المصابة كل أربع ساعات یومیا
# ً
# الأذن: الأذن یجب أن تكون نظیفة و یقطر من ۲ الى ٤ قطرات من ثلاث الى أربع مرات یومیا
# الأطفال: لا یحتاج لتعدیل الجرعة للأطفال
# تعلیمات الاستعمال
# - أولا قم بغسل یدیك.
#  -لا تدع عینیك( أو أي سطح أخر )یلامس رأس العبوة.
# - أمل رأسك للخلف و أنظر للسقف.
# - اسحب بلطف الجفن السفلي للأسفل حتى یتكون جیب صغیر
# - اقلب العبوة للأسفل واضغط علیھا حتى تخرج قطرة أو قطرتین في كل عین تحتاج للعلاج.
# - أغمض عینیك و اضغظ بإصبعك على زاویة العین( بالجھة المقابلة للأنف) لمدة دقیقة
# - كرر العملیة بالعین الاخرى اذا كانت ھناك ضرورة.
# - أعد الغطاء و أحكم إغلاقھ بعد استعمالھقم بإغلاق العبوة وأحكام اغلاقھا مباشرة بعد الاستعمال.
# كقطرة أذنیة : ُ یجب أن تكون الأذن نظیفة , أمل رأسك جانبا و حرر قطرات بالضغط بلطف. إذا حم ِل المحلول
# العیني بطریقة خاطئة قد یؤدي الى تلوثھا ببكتیریا وقد تسبب التھابات بالعین . في حال وجود تفاقم في وضع
# العین یجب مراجعة الطبیب فورا.
# إذا تجاوزت الجرعة من أبیجین:
# الجرعة الزائدة عند البالغین، بسبب استخدام القطرة العینیة الأذنیة غیر محتملة، بغض النظر اذا استخدمت قطرات
# عدیدة أو تم بلعھا عن طریق الخطأ یجب مراجعة الطبیب.
# إذا نسیت استخدام أبیجین:
# إذا نسیت أخذ الجرعة خذھا عند تذكرھا مباشرة, ما لم یقترب موعد الجرعة التالیة لا تستعمل جرعة مضاعفة
# لتعوض الجرعة المنسیة .و بعدھا استخدم الجرعة التالیة كالمعتاد و استمر على الوضع الطبیعي
# -٤ الاثار الجانبیة.
# كباقي الأدویة أبیجین لھ أثار جانبیة ولكن لا تحدث للجمیع
# الآثار الجانبیة الممكن حدوثھا تتضمن :
# - تلف في الأذن كصعوبة في السمع أو فقدان التوازن.
#  - مشاكل في الكلى كتمریر ماء أقل من المعتاد أو ظھور دم في البول
# - حساسیة موضعیة في العین, تھیج مؤقت في العین, عدم وضوح في الرؤیا, شعور في حرقة أو لسعة, حكة
# - حساسیة موضعیة في الأذن, شعور في حرقة أو لسعة, حكة, التھاب جلدي
# - في حالة حدوث تھیج أو حساسیة أخبر طبیبك حال حدوثھا. یجب وقف العلاج
# - في حال تطور أي من ھذه الآثار الجانبیة أو إذا كنت تلاحظ ظھور أي آثار جانبیة غیر مذكورة في النشرة أخبر
# طبیبك أو الصیدلي
# -٥ كیف تخزن أبیجین.
# - یحفظ بدرجة حرارة لا تتجاوز ۳۰ درجة مئویة
# - تخلص من العبوة بعد أربعة اسابیع من فتحھا
# -٦ معلومات اضافیة.
# على ماذا یحتوي أبیجین؟
# المادة الفعالة: كبریتات الجنتامیسین ٪۰٫۳
# مكونات اخرى : كلورید البنزالكونیوم ,٪۰٫۰۱ كلورید الصودیوم , میتابیسلفات الصودیوم, أحادى فوسفات الصودیوم
# , ثنائي القاعدة فوسفات الصودیوم.
# التعبئة: یتوفر في عبوات بلاستیكیة مزودة بقطارة سعة ۱۰مل.
# ملاحظة: إن ھذا المستحضر المعد للإستعمال للعین یحتوي على المادة الحافظة كلورید البنزالكونیوم والتي یمكن أن
# ً على العدسات اللاصقة اللینة وعلیھ یجب ألا یستعمل ھذا المستحضر أثناء استعمال العدسات اللاصقة
# تحدث ترسبا
# المذكورة. كما یجب نزع العدسات اللاصقة اللینة قبل استخدام ھذا المستحضر مع إمكانیة وضعھا في العین بعد ۱٥
# دقیقة من استعمالھ للعین.
# المصنع ومالك حقوق التسویق:
# شركة عمان للصناعات الدوائیة
# مدینة الملك عبد الله الثاني الصناعیة- سحاب -عمان.
# """
# arr = []

# arr.extend(pdf_lines.split('\n'))
# for i , line in enumerate(arr):
#     arr[i] = remove_extra_spaces(line)
# print(arr)
# createJson(arr)


from clientgpt import generate_schema_strict
from pydantic import BaseModel

class Schema(BaseModel):
    full_name: str
    invented_name: str
    strengths: list[str]
    measurement_unit: str
    pharmaceutical_forms: list[str]
    active_substances: list[str]
    medical_device: str


system = """
format:
Package leaflet: Information for the patient
{(Invented name) (Strength(s)) (Pharmaceutical form)}
{Active substance(s)}

Notes:
1.Pharmacutical form can include a medical device such as a syringe, inhaler, pre-filled pen , patches, etc..., and Strength(s) will include measurement unit.
2.Full name will include the Invented name, Strength(s) and Pharmaceutical(s) form but the Invented name will not include the Strength(s) and Pharmaceutical form(s).
3.Invented name is usually the very first word or two words following the statement package information: for the patient and its just a brand name.
4.Some values may be empty, if so, leave them empty in the response.

Extract the information provided in the schema.
"""

prompt = f"""
Apigen 0.3% Eye/Ear Drops 
Gentamicin Sulphate
Read all of this leaflet carefully before you start taking this medicine.
- Keep this leaflet. You may need to read it again.
- If you have any further questions, ask your doctor or pharmacist.
- This medicine has been prescribed for you. Do not pass it on to others. It may harm them,
even if their symptoms are the same as yours.
- If any of the side effects gets serious, or if you notice any side effects not listed in this
leaflet,please tell your doctor or pharmacist.
"""

response = generate_schema_strict(prompt=prompt, system=system, schema=Schema)



print(response["full_name"])
# from extractUtils import extract_div_contents

# html = """
# something else with that setnece is brlay
# """ 
# print(extract_div_contents(html))

# import os
# from dotenv import load_dotenv
# load_dotenv()
# model = os.getenv("MODEL")

# print(model)