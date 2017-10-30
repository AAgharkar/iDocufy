import re

def get_licence_details(text):
    get_licence_id=re.findall(r'\d{12}|\w*[A-Z]?\d{8,9}|\w*[A-Z]\d{4}\s\d{5}\s\d{5}|\d{2,3}\s\d{3}\s\d{3}',text)
    print(get_licence_id[0])
    date_val=[]
    # val=re.findall(r'(((\w*?0?[1-9]|\w*?[12][0-9]|\w*?3[01])\s?[- /.]\s?(0?[1-9]|\w*?1[012])|\w*?(0?[1-9]|\w*?1[012])\s?[- /.]\s?(0[1-9]|\w*?[12][0-9]|\w*?3[01]))\s?[- /.]\s?\d{4}\w*?)\b',text)
    # for item in val:
    #     date_val.append(" ".join(item))
    # date_value=" ".join(map(str,date_val))
    get_birth_date=re.findall(r'\d{1,2}\s?[- /.]?\s?\d{2}\s?[- /.]?\s?\d{4}',text)
    print(get_birth_date)

    return get_licence_id[0],get_birth_date
# get_licence_details("""Class D . DL CUBADRIVER LICENSE NOT FOR FEDERAL IDENTIFICATION 9 Class:D 12 Restr:NONE on Endors:NONE15Sex: M # 157217830 as slic 16Ht 72 in3 DOB : 03-03-1982 18Eyes: BRO 4b Expires: 03 -03-2020 and 1 VERRELLI 2MICHAEL JAY 2100 LORDSHIP RD STRATFORD CT 066154a Issued:02-15-2014""")