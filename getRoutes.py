import ollama
import ast
from extractUtils import check_similarity
from peewee import *
import os
from dotenv import load_dotenv
from clientgpt import generate_schema_strict
from pydantic import BaseModel

class Schema(BaseModel):
    routes: list[str]
load_dotenv()
model = os.getenv("model")
db_name = os.getenv("db_name")
user = os.getenv("db_user")
password = os.getenv("db_password")
host = os.getenv("db_host")
port = os.getenv("db_port")
print(db_name)
db = PostgresqlDatabase(db_name, user=user, password=password, host=host, port=port)
class routes(Model):
    code = CharField()
    display = CharField()
    class Meta:
        database = db

system_routes = """
user will give information about how to take a specific medical product determine which of the possible administration route this medication uses and only answer with the correct medication route.
in your answer only respond with the correct route names exactly as it is written in the list.

use the provided format to answer:

Possible administration routes list:
1. Topical 
2. Otic 
3. Intra-articular 
4. Per vagina
5. Oral 
6. Subcutaneous 
7. Per rectum
8. Intraluminal 
9. Sublingual 
10. Intraperitoneal 
11. Transdermal 
12. Nasal 
13. Intravenous 
14. Buccal 
15. Ophthalmic 
16. Intra-arterial 
17. Intramedullary 
18. Intrauterine 
19. Intrathecal 
20. Intramuscular 
21. Urethral 
22. Gastrostomy 
23. Jejunostomy 
24. Nasogastric 
25. Dental 
26. Endocervical 
27. Endosinusial 
28. Endotracheopulmonary 
29. Extra-amniotic 
30. Gastroenteral 
31. Gingival 
32. Intraamniotic 
33. Intrabursal 
34. Intracardiac 
35. Intracavernous 
36. Intracervical 
37. Intracoronary 
38. Intradermal 
39. Intradiscal 
40. Intralesional 
41. Intralymphatic 
42. Intraocular 
43. Intrapleural 
44. Intrasternal 
45. Intravesical 
46. Ocular 
47. Oromucosal 
48. Periarticular 
49. Perineural 
50. Subconjunctival 
51. Transmucosal 
52. Intratracheal 
53. Intrabiliary 
54. Epidural 
55. Suborbital 
56. Caudal 
57. Intraosseous 
58. Intrathoracic 
59. Enteral 
60. Intraductal 
61. Intratympanic 
62. Intravenous central 
63. Intramyometrial 
64. Gastro-intestinal stoma 
65. Colostomy 
66. Periurethral 
67. Intracoronal 
68. Retrobulbar 
69. Intracartilaginous 
70. Intravitreal 
71. Intraspinal 
72. Orogastric 
73. Transurethral 
74. Intratendinous 
75. Intracorneal 
76. Oropharyngeal 
77. Peribulbar 
78. Nasojejunal 
79. Fistula 
80. Surgical drain 
81. Intracameral 
82. Paracervical 
83. Intrasynovial 
84. Intraduodenal 
85. Intracisternal 
86. Intratesticular 
87. Intracranial 
88. Tumour cavity 
89. Paravertebral 
90. Intrasinal 
91. Transcervical 
92. Subtendinous 
93. Intraabdominal 
94. Subgingival 
95. Intraovarian 
96. Ureteral 
97. Peritendinous 
98. Intrabronchial 
99. Intraprostatic 
100. Submucosal 
101. Surgical cavity 
102. Ileostomy 
103. Intravenous peripheral 
104. Periosteal 
105. Esophagostomy 
106. Urostomy 
107. Laryngeal 
108. Intrapulmonary 
109. Mucous fistula 
110. Nasoduodenal 
111. Body cavity 
112. Intraventricular  - cardiac
113. Intracerebroventricular 
114. Percutaneous 
115. Interstitial 
116. Intraesophageal 
117. Intragingival 
118. Intravascular 
119. Intradural 
120. Intrameningeal 
121. Intragastric 
122. Intrapericardial 
123. Intralingual 
124. Intrahepatic 
125. Conjunctival 
126. Intraepicardial 
127. Transendocardial 
128. Transplacental 
129. Intracerebral 
130. Intraileal 
131. Periodontal 
132. Peridural 
133. Lower respiratory tract 
134. Intramammary 
135. Intratumor 
136. Transtympanic 
137. Transtracheal 
138. Respiratory tract 
139. Digestive tract 
140. Intraepidermal 
141. Intrajejunal 
142. Intracolonic 
143. Cutaneous 
144. Arteriovenous fistula 
145. Intraneural 
146. Intramural 
147. Extracorporeal 
148. Infiltration 
149. Epilesional 
150. Extracorporeal hemodialysis 
151. Intradialytic 
152. Intracatheter instillation 
153. Suprachoroidal 
154. Intracorporus cavernosum 
155. Sublesional 
156. Intestinal 
157. Intraglandular 
158. Intracholangiopancreatic 
159. Intraportal 
160. Peritumoral 
161. Posterior juxtascleral 
162. Subretinal 
163. Sublabial 
"""

def get_adminstration_routes_array(section_3):
   #  response = ollama.generate(model=model , system=system_routes, prompt=prompt_routes , options = {"num_predict": 20})
   for section_line in section_3:
      prompt += section_line

   response = generate_schema_strict( prompt , system_routes , schema=Schema)

   routes_array = response["routes"]

   for i,route in enumerate(routes_array):
      if route.strip().lower().endswith("ly"):
         routes_array[i] = route[:-2]
      biggest_similarity = 0
   for route_code in routes.select().where(routes.display.contains(route.lower())):
    check_similarity_ratio = check_similarity(route.lower(), route_code.display)
    if check_similarity_ratio > biggest_similarity:
      biggest_similarity = check_similarity_ratio
      routes_array[i] = {"code": route_code.code , "display": route_code.display}
   return routes_array
     

