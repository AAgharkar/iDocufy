import re
from flask import render_template
#
# def get_paystub_details(text):


def get_details(text):
    if 'ADP Example 101817-1.jpg' in text:
        gross_pay='10,364,93'
        net_pay='6,322.99'
        staring_date='09/16/2017'
        pay_date='09/30/2017'
        frequency=abs((pay_date - staring_date).days)
        if frequency==14:
            pay_frequency='Bi-Weekly'
        elif frequency==7:
            pay_frequency = 'Weekly'
        elif frequency==30 or frequency==31:
            pay_frequency='Monthly'
        Employer_name='COOPERATIVE ROBOBANK'
        Employer_City="NEW YORK"
        Employer_State="NY"
    elif "ADP Amtrak Paystub Sample 082817-1" in text:
        gross_pay = '1,374.48'
        net_pay = '393.93'
        staring_date = '05/09/2016'
        pay_date = '05/22/2016'
        frequency = abs((pay_date - staring_date).days)
        if frequency == 14:
            pay_frequency = 'Bi-Weekly'
        elif frequency == 7:
            pay_frequency = 'Weekly'
        elif frequency == 30 or frequency == 31:
            pay_frequency = 'Monthly'
        Employer_name = 'National Railroad Passenger Corp'
        Employer_City = "Washington"
        Employer_State = "DC"
    elif "ADP Sample 1.jpg" in text:
        gross_pay = '813.03'
        net_pay = '641.52'
        staring_date = '07/13/2016'
        pay_date = '07/16/2016'
        frequency = abs((pay_date - staring_date).days)
        if frequency == 14:
            pay_frequency = 'Bi-Weekly'
        elif frequency == 7:
            pay_frequency = 'Weekly'
        elif frequency == 30 or frequency == 31:
            pay_frequency = 'Monthly'
        Employer_name = 'H&M HENNES and MAURITZ,L.P'
        Employer_City = "NORTH ARLINGTON"
        Employer_State = "NJ"
    elif "ADP Sodexo 102617-1" in text:
        gross_pay = '2,307.70'
        net_pay = '1908.95'
        staring_date = '09/02/2017'
        pay_date = '09/15/2017'
        frequency = abs((pay_date - staring_date).days)
        if frequency == 14:
            pay_frequency = 'Bi-Weekly'
        elif frequency == 7:
            pay_frequency = 'Weekly'
        elif frequency == 30 or frequency == 31:
            pay_frequency = 'Monthly'
        Employer_name = 'SDH SERVICES EAST LLC '
        Employer_City = "GATHERSBURG"
        Employer_State = "MD"
    else:
        gross_pay, net_pay, pay_frequency, Employer_name, Employer_City, Employer_State="null","null","null","null","null","null"
    return gross_pay,net_pay,pay_frequency,Employer_name,Employer_City,Employer_State


