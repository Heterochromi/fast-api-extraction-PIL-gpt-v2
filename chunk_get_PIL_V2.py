from semantic import semantic_similarity

from parse_html import get_parsed_html


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
    
    highest_similarity = 0.0
    for i , line in enumerate(pdf_lines):
        similarity_ratio = semantic_similarity(line['text'], find_line , lang=lang)
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

    return header_content , what_is_in_this_leaflet_content , all_sections



# "code": "43678-2",
# "display": "DOSAGE FORMS & STRENGTHS SECTION"
#       "section-code": "34067-9",
#       "display-value": "INDICATIONS & USAGE",
#       "PIL_section": "1. What is {invented name} and what it is used for"
# class="page"
## most important part
def addDivSeperationTags(all_sections):
    for i , section in enumerate(sections):
        n_section = all_sections[i]
        n_section[0]['fullElement'] = f""" <div code="{section['section-code']}" display="{section['display-value']}" title="{section['PIL_section']}">""" + str(n_section[0]['fullElement'])
        n_section[-1]['fullElement'] = str(n_section[-1]['fullElement']) + "</div>"









def splitHtml(content : str , lang = "en"):
    parsed , fullHtml = get_parsed_html(content)
    header_content , what_is_in_this_leaflet_content , all_sections = splitLeaflet(parsed , lang)
    print(header_content)
    print(what_is_in_this_leaflet_content)
    print(all_sections)
    addDivSeperationTags(all_sections)

    with open('resultSections.txt' , 'w' , encoding='utf-8') as file:
     file.write(f"{all_sections}")
    return




html_content= """
<meta charset="UTF-8">
<title></title>
<meta name="generator" content="Docling HTML Serializer">
<style type="text/css">html {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }
    body {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    h1 {
        font-size: 2em;
        border-bottom: 1px solid #eee;
        padding-bottom: 0.3em;
    }
    table {
        border-collapse: collapse;
        margin: 1em 0;
        width: 100%;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    figure {
        margin: 1.5em 0;
        text-align: center;
    }
    figcaption {
        color: #666;
        font-style: italic;
        margin-top: 0.5em;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    pre {
        background-color: #f6f8fa;
        border-radius: 3px;
        padding: 1em;
        overflow: auto;
    }
    code {
        font-family: monospace;
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    .formula {
        text-align: center;
        padding: 0.5em;
        margin: 1em 0;
        background-color: #f9f9f9;
    }
    .formula-not-decoded {
        text-align: center;
        padding: 0.5em;
        margin: 1em 0;
        background: repeating-linear-gradient(
            45deg,
            #f0f0f0,
            #f0f0f0 10px,
            #f9f9f9 10px,
            #f9f9f9 20px
        );
    }
    .page-break {
        page-break-after: always;
        border-top: 1px dashed #ccc;
        margin: 2em 0;
    }
    .key-value-region {
        background-color: #f9f9f9;
        padding: 1em;
        border-radius: 4px;
        margin: 1em 0;
    }
    .key-value-region dt {
        font-weight: bold;
    }
    .key-value-region dd {
        margin-left: 1em;
        margin-bottom: 0.5em;
    }
    .form-container {
        border: 1px solid #ddd;
        padding: 1em;
        border-radius: 4px;
        margin: 1em 0;
    }
    .form-item {
        margin-bottom: 0.5em;
    }
    .image-classification {
        font-size: 0.9em;
        color: #666;
        margin-top: 0.5em;
    }
</style>
<div class="page">
<h2>Motility&reg;</h2>

<h2>Prucalopride</h2>

<p>Read all of this leaflet carefully before you start taking this medicine because it contains important information for you . &middot; Keep this leaflet . You may need to read it again .</p>

<ul>
	<li>If you have any further questions about your illness or your medicine , ask your doctor , nurse or pharmacist .</li>
	<li>This medicine has been prescribed for you . Do not pass it on to others . It may harm them , even if their symptoms are the same as yours .</li>
	<li>If any of the side effects get serious , or if you notice any side effects not listed in this leaflet please tell your doctor , nurse or pharmacist .</li>
</ul>

<h2>What is in this leaflet ;</h2>

<ul>
	<li>What Motility&reg; is and what it is used for</li>
	<li>What you need to know before you take Motility&reg;</li>
	<li>How to take Motility&reg;</li>
	<li>Possible side effects</li>
	<li>How to store Motility&reg;</li>
	<li>Other information</li>
</ul>

<h2>1. What Motility&reg; is and what it is used for</h2>

<p>Motility&reg; contains the active substance prucalopride .</p>

<p>MotilityⓇ belongs to a group of gut motility enhancing medicines ( gastrointestinal prokinetics ) . It acts on the muscle wall of the gut , helping to restore the normal functioning of the bowel . Motility&reg; is used for the treatment of chronic constipation in adults in whom laxatives do not work well enough .</p>

<p>Not for use in children and adolescents younger than 18 years .</p>

<h2>2. What you need to know before you take Motility&reg;</h2>

<h2>Do not take MotilityⓇ if you have :</h2>

<ul>
	<li>If you are allergic to prucalopride or any of the other ingredients of this medicine ( listed in section 6 ) .</li>
	<li>If you are on renal dialysis .</li>
	<li>If you suffer from perforation or obstruction of the gut wall , severe inflammation of the intestinal tract , such as Crohn&#39;s disease , ulcerative colitis or toxic megacolon / megarectum .</li>
</ul>

<p>Warnings and precautions</p>

<p>Talk to your doctor before taking MotilityⓇ</p>

<p>Take special care with Motility and tell your doctor if you :</p>

<ul>
	<li>Suffer from severe kidney disease .</li>
	<li>Suffer from severe liver disease .</li>
	<li>Are currently under supervision by a doctor for a serious medical problem such as lung or heart disease , nervous system or mental health problems , cancer , AIDS or a hormonal disorder .</li>
</ul>

<p>If you have very bad diarrhea , the contraceptive pill may not work properly and the use of an extra method of contraception is recommended . See the instructions in the patient leaflet of the contraceptive pill you are taking .</p>

<h2>Other medicines and Motility&reg;</h2>

<p>Tell your doctor if you are taking , or have recently taken , or might take any other medicines .</p>

<p>MotilityⓇ with food and drink</p>

<p>MotilityⓇ can be taken with or without food and drinks , at any time of the day .</p>

<h2>Pregnancy and breast -feeding</h2>

<p>Motility is not recommended for use during pregnancy .</p>

<ul>
	<li>Tell your doctor if you are pregnant or planning to become pregnant .</li>
	<li>Use a reliable method of contraception while you&#39;re taking Motility , to prevent pregnancy .</li>
</ul>

<p>-If you become pregnant during treatment with Motility&reg; , tell your doctor .</p>

<p>When breast -feeding , prucalopride can pass into breast milk . Breastfeeding is not recommended during treatment with Motility&reg; . Talk to your doctor about this .</p>

<p>Ask your doctor for advice before taking any medicine .</p>

<h2>Driving and using machines</h2>

<p>Motility&reg; is unlikely to affect your ability to drive or use machines . However , sometimes MotilityⓇ may cause dizziness and tiredness , especially on the first day of treatment , and this may have an effect on driving and use of machines .</p>

<h2>Motility&reg; contains lactose</h2>

<p>If you have been told by your doctor that you have an intolerance to some sugars , contact your doctor before taking this medicine .</p>

<h2>3. How to take Motility&reg;</h2>

<p>Always take this medicine exactly as described in this leaflet or as your doctor has told you . Check with your doctor or pharmacist if you are not sure . Take MotilityⓇ every day for as long as your</p>

<h2>doctor prescribes it .</h2>

<p>The doctor may want to reassess your condition and the benefit of continued treatment after the first 4 weeks and thereafter at regular intervals .</p>

<p>The usual dose of Motility&reg; for most patients is one 2 mg tablet once a day .</p>

<p>If you are older than 65 years or have severe liver disease , the starting dose is one 1 mg tablet once a day , which your doctor may increase to 2 mg once a day if needed .</p>

<p>Your doctor may also recommend a lower dose of one 1 mg tablet daily if you have severe kidney disease .</p>

<p>Taking a higher dose than recommended will not make the product work better .</p>

<p>Motility&reg; is only for adults and should not be taken by children and adolescents up to 18 years .</p>

<h2>If you take more MotilityⓇ than you should</h2>

<p>It is important to keep to the dose as prescribed by your doctor . If you have taken more Motility than you should , it is possible that you will get diarrhea , headache and / or nausea . In case of diarrhea make sure that you drink enough water .</p>

<h2>If you forget to take Motility&reg;</h2>

<p>Do not take a double dose to make up for a forgotten tablet . Just take your next dose at the usual time .</p>

<h2>If you stop taking Motility&reg;</h2>

<p>If you stop taking MotilityⓇ your constipation symptoms may come back again .</p>

<p>If you have any further questions on the use of this medicine , ask your doctor or pharmacist .</p>

<h2>4. Possible side effects</h2>

<p>Like all medicines , this medicine can cause side effects , although not everybody gets them . The side effects mostly occur at the start of treatment and usually disappear within a few days with continued treatment .</p>

<p>The following side effects have been reported very commonly ( may affect more than 1 in 10 people ) : headache , feeling sick , diarrhea and abdominal pain .</p>

<p>The following side effects have been reported commonly ( may affect up to 1 in 10 people ) : decreased appetite , dizziness , vomiting , disturbed digestion ( dyspepsia ) , windiness , abnormal bowel sounds , tiredness .</p>

<p>,</p>

<p>The following uncommon side effects have also been seen ( may affect up to 1 in 100 people ) : tremors , pounding heart , rectal bleeding , increase in frequency of passing urine ( pollakiuria ) , fever and feeling unwell . If pounding heart occurs , please tell your doctor .</p>

<h2>5. How to store Motility&reg;</h2>

<p>Keep out of the sight and reach of children .</p>

<ul>
	<li>Do not store above 30 &deg; C .</li>
	<li>Do not use this medicine after the expiry date which is stated on the blister and carton after &quot; Exp &quot; . The expiry date refers to the last day of that month .</li>
	<li>Do not throw away any medicines via wastewater or household waste . Ask your pharmacist how to throw away medicines you no longer use . These measures will help protect the environment .</li>
</ul>

<p>6.</p>

<h2>Other information :</h2>

<p>The active ingredient : is Prucalopride .</p>

<p>MotilityⓇ1mg F.C Tablets : Each Film coated tablet contains Prucalopride succinate equivalent to 1 mg Prucalopride . Motility 2mg F.C Tablets : Each Film coated tablet contains Prucalopride succinate equivalent to 2 mg Prucalopride . Other ingredients :</p>

<p>MotilityⓇ1mg F.C Tablets : Lactose monohydrate , Cellulose microcrystalline , Silica colloidal anhydrous , Magnesium stearate , Instacoat universal .</p>

<p>MotilityⓇ2mg F.C Tablets : Lactose monohydrate , Cellulose microcrystalline , Silica colloidal anhydrous , Magnesium stearate , Instacoat universal , Red iron oxide .</p>

<p>What Motility looks like and contents of the pack</p>

<p>MotilityⓇ1mg F.C Tablets : White to off -white round biconvex plain tablets .</p>

<p>MotilityⓇ2mg F.C Tablets : Pink round biconvex tablets , plain on both sides .</p>

<p>Motility Tablets are packed in Alu / Alu -Foil blisters of 30 Tablets ( 10 Tablets / blister , 3 blisters / Pack ) in a carton box with folded leaflet</p>

<p>.</p>

<p>Revision Date 07/2024</p>

<p>For any information about this medicinal product , please contact the Email :</p>

<h2>Pv@miskpharma.com</h2>

<h2>To report any side effect ( s ) :</h2>

<p>Jordan Food &amp; Drug Administration :</p>

<p>&bull; Email : jpc@jfda.jo</p>

<p>Website :</p>

<p>https://primaryreporting.who-umc.org/jo : + 962-6-5632000</p>

<p>&bull; Phone No</p>

<p>⚫QR Code :</p>

<figure><img src="/Users/abed/epi-repo/storage/app/leaflets/bundle-f35af27d-9737-4ad9-9eb2-ca30fb83aca9_artifacts/image_000000_919dd853007a3d6063b767c233d90effbf11545c91c0b25c31a63fe78993b43a.png" /></figure>

<h2>This is a medicament</h2>

<p>&middot; Medicament is a product which affects your health , and its consumption contrary to instructions is dangerous for you . &middot; Follow strictly the doctor&#39;s prescription , the method of use and the instructions of the pharmacist who sold the medicament .</p>

<ul>
	<li>The doctor and the pharmacist are experts in medicine , its benefits and risks .</li>
	<li>Do not by yourself interrupt the period of treatment prescribed for you .</li>
	<li>Do not repeat the same prescription without consulting your doctor .</li>
</ul>

<p>&middot; Keep medicament out of the reach of children .</p>

<p>COUNCIL OF ARAB HEALTH MINISTERS UNION OF ARAB PHARMACISTS</p>

<figure><img src="/Users/abed/epi-repo/storage/app/leaflets/bundle-f35af27d-9737-4ad9-9eb2-ca30fb83aca9_artifacts/image_000001_a0a8f1ebffc3c31ad9cfa622d579b36844a08be5d5feed62fd8cb210e4bc7bbb.png" /></figure>

<p>Misk Pharmaceutical Industries Co.</p>

<p>Mobes -Amman -Jordan</p>

<p>L34R01</p>

<p>300 X138mm</p>

<p>Pharma</p>
</div>

"""


splitHtml(html_content)