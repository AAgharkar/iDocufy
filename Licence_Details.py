import re
from flask import render_template

# def get_licence_details(text):
#     try:
#         #print(text)
#         get_licence_id=re.findall(r'\d{12}|\w*[A-Z]?\d{8,9}|\w*[A-Z]\d{4}\s\d{5}\s\d{5}|\d{2,3}\s\d{3}\s\d{3}',text)
#         #print(get_licence_id[0])
#         birth_date_val,date_val,date,actual_date=[],[],[],[]
#
#         val=re.findall(r'(((\w*?0?[1-9]|\w*?[12][0-9]|\w*?3[01])\s?[- /.]?\s?(0?[1-9]|\w*?1[012])|\w*?(0?[1-9]'
#                        r'|\w*?1[012])\s?[- /.]?\s?(0[1-9]|\w*?[12][0-9]|\w*?3[01]))\s?[- /.]?\s?\d{4}\w*?)\b',text)
#         for item in val:
#             date_val.append(" ".join(item))
#         data_value=" ".join(map(str,date_val))
#         #print("Value", data_value)
#         get_birth_date=re.findall(r'(\d{1,2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}(19|20|21|22|23|24)\d\d)'
#                                   r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]'
#                                   r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d)\b',data_value)
#         # get_birth_date=re.findall(r'(\d{1,2}\s?[. /-]\d{2}[. /-]\d{4})|(\d{2}[. /-]\d{2}\d{4})|(\d{2}\d{2}[. /-]\d{4})|\d{2}[. /-]\d{2}\s[. /-]\d{4}|(([0-9]|0[0-9]|1[0-9])[. /-]([0-9][0-9]|[0-9])[. /-][0-9]{4})\b',data_value)
#         # #print("Value1", get_birth_date)
#         for item in get_birth_date:
#             birth_date_val.append(" ".join(item))
#         #print("Value1", birth_date_val)
#         for dob in birth_date_val:
#             if "/" in dob:
#                 dob = dob.replace(" ", "")
#                 dob = dob.replace("/", "")
#                 #print("hey",dob)
#             if "-" in dob:
#                 dob = dob.replace(" ", "")
#                 dob = dob.replace("-", "")
#             if "." in dob:
#                 dob = dob.replace(" ", "")
#                 dob = dob.replace(".", "")
#             dob = dob[0:2] + '/' + dob[2:4]+'/'+dob[4:8]
#             # dob = dob[3:5] + '/' + dob[5:]
#             date.append(dob)
#
#         for value in date[:3]:
#             import datetime
#             actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
#         max_date = max(actual_date)
#         min_date = min(actual_date)
#         for date in actual_date:
#             if date > min_date and date < max_date:
#                 iss_date = date
#         # #print(date)
#         max_date=datetime.datetime.strptime(max_date, '%Y/%m/%d').strftime('%m/%d/%Y')
#         min_date=datetime.datetime.strptime(min_date, '%Y/%m/%d').strftime('%m/%d/%Y')
#         iss_date=datetime.datetime.strptime(iss_date, '%Y/%m/%d').strftime('%m/%d/%Y')
#
#         return get_licence_id[0],max_date,min_date,iss_date
#     except Exception as E:
#         error = "Details not Detected properly"
#         return render_template('Index.html', error=error)
def get_licence_details1(text):
    get_licence_id=get_id(text)
    max_date, min_date, iss_date=get_date(text)
    address=get_address(text)
    return get_licence_id,max_date,min_date,iss_date,address
def find_between_r(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
def get_id(text):
    try:
        get_licence_id = re.findall(
            r'\w*[A-Za-z]\d{4}\s\d{10}|\d{12}|\w*[A-Za-z]?\d{8,9}|\w{1}\d{4}\s\d{5}\s\d{4,5}|\d{2,3}\s\d{3}\s\d{3}', text)
        return get_licence_id[0]
    except Exception as E:
        print(E)
        error = "Unable to detect licence id"
        return render_template('Index.html', error=error)
def get_date(text):
    try:
        date_val, date, actual_date = [], [], []
        val = re.findall(
            r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
            r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
            r'|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}(19|20|21|22|23|24)\d\d)'
            r'|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)'
            r'|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)'
            r'|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d)\b', text)
        #print(val)
        date_val1 = []
        for item in val:
            date_val1.append(" ".join(item))
        #print("Date", date_val1)
        string_date = " ".join(map(str, date_val1))
        date_val = re.findall(r'\d{2}[./-]\d{2}[./-]\d{2,4}', string_date)
        #print("Date1", date_val)
        for dob in date_val:
            if 'o' in dob:
                dob = dob.replace("o", "0")
            if ' ' in dob:
                dob = dob.replace(" ", "")
            if "/" in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace("/", "")
            if "-" in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace("-", "")
            if "." in dob:
                dob = dob.replace(" ", "")
                dob = dob.replace(".", "")

            dob = dob[0:2] + '/' + dob[2:4] + '/' + dob[4:8]
            # dob = dob[3:5] + '/' + dob[5:]
            date.append(dob)
        data_value = " ".join(map(str, date))
        #print("Value", data_value)
        # get_birth_date=re.findall(r'(((\w*?0?[1-9]|\w*?[12][0-9]|\w*?3[01])\s?[-/.]?\s?(0?[1-9]|\w*?1[012])|\w*?(0?[1-9]'
        #                r'|\w*?1[012])\s?[-/.]?\s?(0[1-9]|\w*?[12][0-9]|\w*?3[01]))\s?[- /.]?\s?\d{4}\w*?)\b',data_value)
        # for item in get_birth_date:
        #     birth_date_val.append(" ".join(item))
        # #print("Value1", birth_date_val)
        # birth_date_val1=" ".join(map(str,birth_date_val))
        # #print(birth_date_val1)
        # val = re.findall(
        #     r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
        #     r'|(\d{2}[./-]\d{2}(19|20|21|22|23|24)\d\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)'
        #     r'|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d)\b',
        #     birth_date_val1)
        # for item in val:
        #     date.append(" ".join(item))
        # #print(date)
        for value in date[:3]:
            import datetime
            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
            else:
                actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
        data = " ".join(map(str, actual_date))
        #print(data)
        if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
            min_date = max(actual_date)
            iss_date = min(actual_date)
            for date in actual_date:
                if date > iss_date and date < min_date:
                    max_date = date
            max_date = datetime.datetime.strptime(max_date, '%y/%m/%d').strftime('%m/%d/%y')
            min_date = datetime.datetime.strptime(min_date, '%y/%m/%d').strftime('%m/%d/%y')
            iss_date = datetime.datetime.strptime(iss_date, '%y/%m/%d').strftime('%m/%d/%y')
        else:
            max_date = max(actual_date)
            min_date = min(actual_date)
            for date in actual_date:
                if date > min_date and date < max_date:
                    iss_date = date
            max_date = datetime.datetime.strptime(max_date, '%Y/%m/%d').strftime('%m/%d/%Y')
            min_date = datetime.datetime.strptime(min_date, '%Y/%m/%d').strftime('%m/%d/%Y')
            iss_date = datetime.datetime.strptime(iss_date, '%Y/%m/%d').strftime('%m/%d/%Y')
        return max_date,min_date,iss_date
    except Exception as E:
        print(E)
        error = "Unable to detect date"
        return render_template('Index.html', error=error)
def get_address(value):
    try:
        text = ''.join(map(str, value))
        print(text)
        all_number = re.findall(
            r"\s\d{3}\w?\s\w*\,?|\s\d{3}\s\d{1}|\s\d{4}\s|\w*\s\d{5}\s\w*|\w*\s\d{5}-\d{4}|\w*\s\d{5}"
            r"|\d{2}\s\w*|\w{2}\s\d{3}\s\d{2}|\w*\s\d{3}\s\d{1}\s\d{1}"
            r"|\w*\s\d{4}-\d{4}|\w*\s\d{2,5}\s\d{2,3}-\d{4}|\w*\s\d{2,5}\s\d{2,3}",
            text)
        number_val=' '.join(map(str, all_number))
        print("Number_Value",number_val)
        data = re.findall(
            r"((?=AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|"
            r"NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
            r"(\d{5}(?:-\d{4})?|\d{4}(?:-\d{4})?|\d{3}(?:\s\d{2})|\d{3}(?:\s\d{1}\s\d{1})"
            r"|\d{2,5}(?:\s\d{2,5})(?:-\d{4})?)",number_val)
        for item in data:
            zip_code="".join(item)
        for i in range(len(zip_code)):
            if re.search(r"\d{2,3}\s\w*,",number_val):
                street=''.join(map(str, number_val.split(zip_code, 1)[0].split()[-4]))
            else:
                street=''.join(map(str, number_val.split(zip_code, 1)[0].split()[-2]))
        address=find_between_r(text,street,zip_code)
        print(street +address +zip_code)
        full_address=street +address +zip_code
        return full_address
    except Exception as E:
        print(E)


