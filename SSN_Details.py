import re

from flask import render_template

def get_SSN_details1(text):
    try:
        print(text)
        data=re.findall(r'\b(((?!000|666)(?:[0-6]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))[-.]+?((?!00)\d{2})[-.]+?(((?!0000)\d{4})))',text)
        print("ssn_number",data)
        if data==[]:
            ssn_number="null"
            actual_name="null"
        else:
            ssn_number=data[0][0]
            print(text)
            name=' '.join(map(str, text.split(data[0][0], 1)[1].split()[0:3]))
            print(name)
            name_regex = re.findall(r'[A-Z]{2,}(?:(?!\d))\s?[A-Z]{1,}', name)
            print("name",name_regex)
            if name_regex==[]:
                actual_name="null"
            else:
                actual_name = " ".join(map(str, name_regex))
                actual_name = actual_name.replace('THIS', "")
        return ssn_number,actual_name
    except Exception as E:
        data, actual_name = "null", "null"
        return data, actual_name

# get_SSN_details1("-OCIAL SECURITY TWIs ruumiER HAS HELMESTABLISHED FOR * 445 58-8628 Y DEBRA L3A ROGERS IN Ceilte ’RogeSicnamun 04/027ád15E")

