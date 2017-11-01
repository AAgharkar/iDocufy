import re

from flask import render_template


def get_licence_details(text):
    try:
        print(text)
        get_licence_id=re.findall(r'\d{12}|\w*[A-Z]?\d{8,9}|\w*[A-Z]\d{4}\s\d{5}\s\d{5}|\d{2,3}\s\d{3}\s\d{3}',text)
        print(get_licence_id[0])
        birth_date_val,date_val,date,actual_date=[],[],[],[]

        val=re.findall(r'(((\w*?0?[1-9]|\w*?[12][0-9]|\w*?3[01])\s?[- /.]?\s?(0?[1-9]|\w*?1[012])|\w*?(0?[1-9]'
                       r'|\w*?1[012])\s?[- /.]?\s?(0[1-9]|\w*?[12][0-9]|\w*?3[01]))\s?[- /.]?\s?\d{4}\w*?)\b',text)
        for item in val:
            date_val.append(" ".join(item))
        data_value=" ".join(map(str,date_val))
        print("Value", data_value)
        get_birth_date=re.findall(r'(\d{1,2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}(19|20|21|22|23|24)\d\d)'
                                  r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]'
                                  r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d)\b',data_value)
        # get_birth_date=re.findall(r'(\d{1,2}\s?[. /-]\d{2}[. /-]\d{4})|(\d{2}[. /-]\d{2}\d{4})|(\d{2}\d{2}[. /-]\d{4})|\d{2}[. /-]\d{2}\s[. /-]\d{4}|(([0-9]|0[0-9]|1[0-9])[. /-]([0-9][0-9]|[0-9])[. /-][0-9]{4})\b',data_value)
        # print("Value1", get_birth_date)
        for item in get_birth_date:
            birth_date_val.append(" ".join(item))
        print("Value1", birth_date_val)
        for dob in birth_date_val:
            if "/" in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace("/", "")
                print("hey",dob)
            if "-" in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace("-", "")
            if "." in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace(".", "")
            dob = dob[0:2] + '/' + dob[2:4]+'/'+dob[4:8]
            # dob = dob[3:5] + '/' + dob[5:]
            date.append(dob)

        for value in date[:3]:
            import datetime
            actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
        max_date = max(actual_date)
        min_date = min(actual_date)
        for date in actual_date:
            if date > min_date and date < max_date:
                iss_date = date
        # print(date)
        max_date=datetime.datetime.strptime(max_date, '%Y/%m/%d').strftime('%m/%d/%Y')
        min_date=datetime.datetime.strptime(min_date, '%Y/%m/%d').strftime('%m/%d/%Y')
        iss_date=datetime.datetime.strptime(iss_date, '%Y/%m/%d').strftime('%m/%d/%Y')

        return get_licence_id[0],max_date,min_date,iss_date
    except Exception as E:
        error = "Details not Detected properly"
        return render_template('Index.html', error=error)

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
# get_licence_details("""Class D . DL CUBADRIVER LICENSE NOT FOR FEDERAL IDENTIFICATION 9 Class:D 12 Restr:NONE on Endors:NONE15Sex: M # 157217830 as slic 16Ht 72 in3 DOB : 03-03-1982 18Eyes: BRO 4b Expires: 03 -03-2020 and 1 VERRELLI 2MICHAEL JAY 2100 LORDSHIP RD STRATFORD CT 066154a Issued:02-15-2014""")