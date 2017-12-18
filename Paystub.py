import re

from datetime import datetime as dt
import datetime

def gross_net(text):
    data,data1=[],[]

    value=re.findall(r'((=?Gross Pay|Brose Pay|Amount|Gross Earnings|Net Pay)|\s?\$?\d{1,3}\s?\,?\s?\d+\.?\d+?)\b',text)
    for item in value:
        data.append("".join(item))
    string_date=" ".join(map(str,data))
    if re.match('(=?Gross Earnings|Net Pay)\b',string_date):
        gross_value=''.join(map(str, string_date.split('Gross Earnings', 1)[0].split()[-2]))
    else:

        if re.search('(\w+\s\w+\s?\s?\$\d{1,3}\s?\,?\s?\d+\.?(\d+)?)',string_date) is not None:
            get_value = re.findall(r'(=?(Gross Pay|Brose Pay|Amount|Gross Earnings|Net Pay)|\s?\s?\$\d{1,3}\s?\,?\s?\d+\.?\d+?)\b',string_date)
        else:
            get_value = re.findall(r'(=?(Gross Pay|Brose Pay|Amount|Gross Earnings|Net Pay)\s?\s?\d{1,3}\s?\,?\s?\d+\.?\d+?)\b', string_date)


        for item in get_value:
            data1.append("".join(item))
        get_gn_value="".join(map(str,data1))
        print(get_gn_value)
        gross_net_value=re.findall(r'((=?Gross Pay|Brose Pay|Amount|Gross Earnings|Net Pay)\s?\s?\$?\d{1,3}\s?\,?\s?\d+\.?(\d+)?)',get_gn_value)

        value2=[]

        for item in gross_net_value:
            value2.append("".join(item))
        string_date1=" ".join(map(str,value2))


        gross_net_value=re.findall(r'(\s?\$?\d{1,3}\s?\,?\s?\d+\.?(\d+)?)',string_date1)
        print(gross_net_value)
        return gross_net_value[0][0].replace(" ",""),gross_net_value[2][0].replace(" ","")

def address(value):
    try:
        zip_code=[]
        text = ''.join(map(str, value))
        all_number = re.findall(
            r"\s?\d{2,3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\s\d{4}\s|\w*\s\d{5}\s\w*|\w*\s\d{5}-\d{4}|\w*\s\d{5}"
            r"|\d{2}\s\w*|\w{2}\s\d{3}\s\d{2}|\w*\s\d{3}\s\d{1}\s\d{1}"
            r"|\w*\s\d{4}-\d{4}|\w*\s\d{2,5}\s\d{2,3}-\d{4}|\w*\s\d{2,5}\s\d{2,3}",
            text)
        number_val=' '.join(map(str, all_number))
        print("street",number_val)
        data = re.findall(
            r"\b((?=AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI"
            r"|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN"
            r"|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])(\d{5}(?:-\d{4})?|\d{4}(?:-\d{4})?)",number_val)
        for item in data:
            zip_code.append("".join(item))
        print(zip_code)
        if zip_code!=[]:
            if re.search(r'\w*\s(?=ID\s\d)',number_val):
                code=zip_code[1]
            else:
                code=zip_code[0]
            if re.match(r"\d{2,3}\s\w+\,",number_val):
                street=''.join(map(str, number_val.split(code, 1)[0].split()[-4]))
            else:
                street=''.join(map(str, number_val.split(code, 1)[0].split()[-2]))
            address=find_between_r(text,street,zip_code[0])

            full_address=street +address +zip_code[0]
            state,zipcode,city=get_address_zipcode(full_address,zip_code[0])
            full_address=find_between_r(full_address,street,city)
            return street,state,zipcode,city
    except Exception as E:
        full_address,street=None,None
        return full_address, street
def get_name(value,street):
    try:
        print("value",value)
        print("street", street)
        name = ' '.join(map(str, value.split(street, 1)[0].split()[-6:]))
        print("name",name)
        name_regex=re.findall(r'[A-Za-z]\w*\b',name)
        actual_name=" ".join(map(str,name_regex))
        actual_name = actual_name.replace('Expires', "")
        actual_name = actual_name.replace('Name', "")
        actual_name = actual_name.replace('DENONE', "")
        actual_name = actual_name.replace('NONE', "")
        actual_name = actual_name.replace('Address', "")
        actual_name = actual_name.replace('CLASS D', "")
        actual_name = actual_name.replace('CLASSE', "")
        actual_name = actual_name.replace('CLASEXP', "")
        actual_name = actual_name.replace('EXP', "")
        actual_name = actual_name.replace('CLASS', "")
        actual_name = actual_name.replace('ISS', "")
        actual_name = actual_name.replace('SExr', "")
        actual_name = actual_name.replace('EXL', "GU")
        actual_name = actual_name.replace('Payroll', "")
        actual_name = actual_name.replace('Attn', "")
        actual_name = actual_name.replace('GEXP', "")

        return actual_name
    except Exception as e:
        full_name='null'
        return full_name
def get_date(text):
    try:

        date_val, date, actual_date = [], [], []
        val = re.findall(
            r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
            r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)'
            r'|(\d{2}[./-]\d{2}\s?(19|20|21|22|23|24)\d\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
            r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)'
            r'|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]'
            r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
        ##print(val)
        date_val1 = []
        for item in val:
            date_val1.append(" ".join(item))
        ##print("Date", date_val1)
        string_date = " ".join(map(str, date_val1))
        date_val = re.findall(r'\d{2}\s?[./-]?\d{2}\s?[./-]?\d{2,4}', string_date)
        ##print("Date1", date_val)
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
            date.append(dob)
        data_value = " ".join(map(str, date))
        for value in date[:2]:

            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
            else:
                actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
        data = " ".join(map(str, actual_date))
        if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
            ending_date = max(actual_date)
            starting_date = min(actual_date)
            if ending_date != "" and starting_date != "" :
                ending_date = datetime.datetime.strptime(ending_date, '%y/%m/%d').strftime('%m/%d/%y')
                starting_date = datetime.datetime.strptime(starting_date, '%y/%m/%d').strftime('%m/%d/%y')
                employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                pay_date = dt.strptime(starting_date, "%m/%d/%Y")
        else:
            ending_date = max(actual_date)
            starting_date = min(actual_date)
            if ending_date!=None and starting_date!=None:
                ending_date = datetime.datetime.strptime(ending_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                starting_date = datetime.datetime.strptime(starting_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                pay_date = dt.strptime(starting_date, "%m/%d/%Y")
        frequency = abs((pay_date - employment_Start_date).days)
        if frequency == 14 or frequency == 13:
            pay_frequency = 'Bi-Weekly'
        elif frequency == 7 or frequency == 6:
            pay_frequency = 'Weekly'
        elif frequency == 30 or frequency == 31:
            pay_frequency = 'Monthly'
        return employment_Start_date.date(),pay_frequency
    except Exception as E:
        print(E)
        employment_Start_date, pay_frequency= "null", "null"
        return employment_Start_date,pay_frequency
def get_address_zipcode(full_address,zipcode):
    try:
        code=zipcode.split()
        city=''.join(map(str, full_address.split(code[0], 1)[0].split()[-1]))
        return code[0],code[1],city
    except Exception as e:
        print(e)
def find_between_r(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
# def get_details(text):
#     pay_frequency=""
#     if 'Example' in text:
#         gross_pay='10,364,93'
#         net_pay='6,322.99'
#         staring_date="09/16/2017"
#         employment_Start_date = datetime.strptime('09/16/2017', "%m/%d/%Y")
#         pay_date = datetime.strptime('09/30/2017', "%m/%d/%Y")
#         frequency=abs((pay_date - employment_Start_date).days)
#         if frequency==14:
#             pay_frequency='Bi-Weekly'
#         elif frequency==7:
#             pay_frequency = 'Weekly'
#         elif frequency==30 or frequency==31:
#             pay_frequency='Monthly'
#         Employer_name='COOPERATIVE ROBOBANK'
#         Employer_City="NEW YORK"
#         Employer_State="NY"
#     elif "Amtrak" in text:
#         gross_pay = '1,374.48'
#         net_pay = '876.45'
#         staring_date="05/09/2016"
#         employment_Start_date = datetime.strptime('05/09/2016', "%m/%d/%Y")
#         pay_date = datetime.strptime('05/22/2016', "%m/%d/%Y")
#         frequency = abs((pay_date - employment_Start_date).days)
#         if frequency == 14:
#             pay_frequency = 'Bi-Weekly'
#         elif frequency == 7:
#             pay_frequency = 'Weekly'
#         elif frequency == 30 or frequency == 31:
#             pay_frequency = 'Monthly'
#         Employer_name = 'National Railroad Passenger Corp'
#         Employer_City = "Washington"
#         Employer_State = "DC"
#     elif "Sample" in text:
#         gross_pay = '813.03'
#         net_pay = '641.52'
#         staring_date="07/13/2016"
#         employment_Start_date = datetime.strptime('07/13/2016', "%m/%d/%Y")
#         pay_date = datetime.strptime('07/16/2016', "%m/%d/%Y")
#         frequency = abs((pay_date - employment_Start_date).days)
#         if frequency == 14:
#             pay_frequency = 'Bi-Weekly'
#         elif frequency == 7:
#             pay_frequency = 'Weekly'
#         elif frequency == 30 or frequency == 31:
#             pay_frequency = 'Monthly'
#         Employer_name = 'H&M HENNES and MAURITZ,L.P'
#         Employer_City = "NORTH ARLINGTON"
#         Employer_State = "NJ"
#     elif "Sodexo" in text:
#         gross_pay = '2,307.70'
#         net_pay = '1908.95'
#         staring_date='09/02/2017'
#         employment_Start_date= datetime.strptime('09/02/2017', "%m/%d/%Y")
#         pay_date = datetime.strptime('09/15/2017', "%m/%d/%Y")
#         frequency = abs((pay_date - employment_Start_date).days)
#         if frequency == 14:
#             pay_frequency = 'Bi-Weekly'
#         elif frequency == 7:
#             pay_frequency = 'Weekly'
#         elif frequency == 30 or frequency == 31:
#             pay_frequency = 'Monthly'
#         Employer_name = 'SDH SERVICES EAST LLC '
#         Employer_City = "GATHERSBURG"
#         Employer_State = "MD"
#     else:
#         gross_pay, net_pay, pay_frequency, Employer_name, Employer_City, Employer_State,staring_date="null","null","null","null","null","null","null"
#     return gross_pay,net_pay,pay_frequency,Employer_name,Employer_City,Employer_State,staring_date
#
#
def main(text):
    employment_Start_date, pay_frequency=get_date(text)
    street, state, zipcode, city=address(text)
    full_name=get_name(text,street)
    gross_pay,net_pay=gross_net(text)
    print("fullname",full_name)
    print(employment_Start_date, pay_frequency, street, state, zipcode, city,full_name,gross_pay,net_pay)

# main("""Statement WYPOSna 14407 B6 AMTRAK National Railroad Passenger Corp. Attn: Payroll 10 G St. NE Washington DC 20002 Period Beg/End: Advice Date: Advice Number: Batch Number: Page 001 of 001 05/09/2016 - 05/22/2016 06/03/2016 8144070151 000000000183 Tax Authority Federal New York Pennsylvania Exempt AddtlS/01 S/01 S/00 MALCOLM CLAY II 7023 SOUDER STREET PHILADELPHIA PA 19149 For inquiries on this statement please call: 866–247-2915 Rate of Pay 19.09 Hours 72.00 Earnings Regular Earn Holiday sick Vacation Pers Hol Payout Unifrm Allownce Unpaid Hours Brose Pay Current 1,374.480.00 0.00 0.00 0.00 0.00 Y-T-D 14, 386.62719.04 878.32 898.80 179.76 37.50 Deductions *Med Pre Tax Union Dues Uniform EotDeductions Current 104.600.000.00 380460 Y-T-D 1,150.60438.35 150.26 * denotes pre-tax deductions 24.00 1,37448 7,300. OA Net Bay 876876.45.  3 61352 Quota Accrued PersHol8.00 SickLeav40.00 Vacation40.00 Used LumpSum Balance 0.008.00 40.000.00 40.000.00 Taxes Federal Withholding Tax Federal Railroad Rtmt Tieri Federal Railroad Rtmt Tier2 Federal Railroad Medicare New York withholding Tax Pennsylvania Withholding Tax Philadelphia withholding Tax Total taxes Current 136.30 78.73 62.23 18.41 48.110.00 49.65 39343 Y-T-D 1, 607.14986.54 779.69 230.72 154.18 366.86622.18 A, 747.31 Wages-Current1,269.88 1,269.88 1,269.88 1,269.88 1,269.880.00 1,269.88 Wages-YTD 15, 911.94 15, 911.94 15, 911.94 15, 911.943,962.36 11,949.58 15, 911.94 O Autat cu AMTRAK Corp. Advice Number: 8144070151 National Railroad Passenger 60 Massachusetts Ave. NE Washington DC 20002 Advice Date: 06/03/2016 866-247-2915 Deposited to the account of MALCOLM CLAY II Account Number XXXX9101 Transit ABA 236084285 Amount 876.45 THIS IS NOT ACHECK""")
# main("""co, FILE DEPT. CLOCK VCHR. NO. 020 JTD 004098 0111050000390064 AP COOPERATIVE RABOBANK 245 PARK AVENUE NEW YORK, NY 10167-0062 CO PH NUMBER 212-916-7800 Earnings Statement Period Beginning:09/16/2017 Period Ending:09/30/2017 Pay Date:09/29/2017 Rabobank Single Taxable Marital Status: Exemptions/Allowances:Federal: NY: New York Cit: VINEET GUMASTA 27 BARKER AVENUE APARTMENT 821 WHITE PLAINS, NY 10601 rate 10364.38 hours 75.83 Earnings Regular Dependent Gt| Bonus Deferral Bonus this period 10,364.380.55 year to date 185,351.32 56,422.00 52,253.00 294 ,032.37 Gross Pay $10,364.93 Your federal taxable wages this period are$9,705.57 Other Benefits and Informationthis periodtotal to date Mctswa10,364.38 W2Grp22.40274.50 401K Elig Wages10,364.38241,773.32 401K Match310.93 7,253.20 401K Safe Harbo310.93 Deductions -2,479.55 -150.08-93.14 -657.96-1.30 56,757.83 3,466.72351.75 16,667.9123.40 7,886.40 Statutory Federal Income Tax Medicare Tax Medicare Surtax NY State Income Tax NY SUI/SDI Tax Social Security Tax Other Dependent Gt| Fsa-Medical 401K Trip Commuter Net Pay Savings Net Check -0.55 -37.50* -621.86* 6.05 675.00 14,506.36 2,295.00 $6, 322.99 -6, 322.99$0.00 *Excluded from federal taxable wages O 2000 ADP. uc Advice number: Pay date: 00000390064 09/29/2017 COOPERATIVE RABOBANK 245 PARK AVENUE NEW YORK, NY 10167-0062 CO PH NUMBER 212-916-7800 Rabobank Deposited to the account of VINEET GUMASTA * A second rounder andere der seine Faccount number XXXXX6407 transit ABA XXXX XXXX amount $6,322.99 NON-NEGOTIABLE THIS IS NOT A CHECK""")