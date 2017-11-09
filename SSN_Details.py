import re

from flask import render_template

def get_SSN_details1(text):
    data=re.findall(r'\b(((?!000|666)(?:[0-6]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))[-.]+?((?!00)\d{2})[-.]+?(((?!0000)\d{4})))',text)
    print(text)
    return data[0][0]

# get_SSN_details1("-OCIAL SECURITY TWIs ruumiER HAS HELMESTABLISHED FOR * 445 58-8628 Y DEBRA L3A ROGERS IN Ceilte ’RogeSicnamun 04/027ád15E")

