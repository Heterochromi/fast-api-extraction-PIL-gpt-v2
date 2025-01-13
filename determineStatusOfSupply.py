#offical ="This medicine has been prescribed for you. Do not pass it on to others. It may harm them, even if their symptoms are the same as yours."
offical_prescription_statement_word_list = ["prescribed for you" , "prescribed to you" , "prescribed by your doctor" , "do not pass it on to others" , "never give yourself this medicine" , "وصفھ" , "وُصف" ,"لا تعط", "ضرر" ,"نفس الاعراض" ,"وصف","علامات مرض"]
supply_status_codes = [{"code" :'100000072076' , "display" :"Medicinal product not subject to medical prescription"} , {"code" :'100000072084' , "display" :"Medicinal product subject to medical prescription"}]

def determineStatusOfSupply(header_section):
    for word in offical_prescription_statement_word_list:
        for line in header_section:
            if word in line.lower():
                return supply_status_codes[1]
    return supply_status_codes[0]

