import threading
import os
import requests
from flask import Flask, request, json
from multiprocessing import Queue
from urllib.request import urlopen
import Img_to_Text
import Licence_Details
import SSN_Details
import noise_reduction
import ssn_noise_reduction
import Paystub

app = Flask(__name__,static_folder='static')
output_doc = Queue()
details = Queue()

def get_doc(path,doc_type):
    text = Img_to_Text.detect_document(path)
    if 'License' in doc_type:
        licence_id, max_date, min_date, iss_date, address, name,state,zipcode,city = Licence_Details.get_licence_details1(text)
        output_doc.put((text,licence_id, max_date, min_date, iss_date, address, name,state,zipcode,city))
    elif 'SSN' in doc_type:
        SSN_Number, name = SSN_Details.get_SSN_details1(text)
        output_doc.put((text,SSN_Number, name))

@app.route("/", methods=['GET'])
def index1():
    return "hello"

@app.route("/api/ocr", methods=['POST'])
def index():

        response={}
        text=''
        name_value = []
        content = request.json
        print(content)
        doc_id = int(content['doc_id'])
        url = "http://192.168.9.81:5011" + content['file_path']
        print(url.replace(" ","%20"))
        url=url.replace(" ","%20")
        image_on_web = urlopen(url)
        filename = os.path.basename(url)
        r = requests.post('http://192.168.9.81:5011/getAllDocumentsMaster')
        resp_dict=json.loads(json.dumps(r.json()))
        value=resp_dict.get('records')
        json_val=dict([(value[i]['id'],value[i]['name'])  for i in range(len(value))])
        # print(data[2][1])

        # pieces = url.split("/")
        # length = len(pieces)
        # filename = pieces[length - 1:length]
        print(json_val[doc_id])
        buf = image_on_web.read()
        with open("Upload_Image/"+filename, "wb") as downloaded_image:
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        if 'License' in json_val[doc_id]:
            print("hello")
            image_path = noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            print(image_path)
            thread = threading.Thread(target=get_doc, args=(image_path,json_val[doc_id],))
            thread.start()
            (text,licence_id, exp_date, dob, iss_date, address, name,state,zipcode,city) = output_doc.get()
            print("name",name)
            if licence_id =='null' and exp_date =='null' and dob =='null' and iss_date =='null' and address =='null' and name=='null'and state=='null'and zipcode=='null' and city=='null':
                response = {'error_msg': "Invalid image"}
            else:
                if name=='null':
                    name_value=[]
                    name_value.append('-')
                    name_value.append('-')
                    name_value.append('-')
                else:
                    name_value=name.split()
                    print("name_value",name_value)
                if len(name_value)>2:
                    add = {'first_name': name_value[1], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date, 'last_name': name_value[0], 'address': address, 'license_id': licence_id,\
                           "middle_name":name_value[2],"state":state,"postal_code":zipcode,"city":city}
                else:
                    add = {'first_name': name_value[0], 'dob': dob, 'issue_date': iss_date,
                           'expiration_date': exp_date, 'last_name': name_value[1], 'address': address,
                           'license_id': licence_id,"middle_name":'-',"state":state,"postal_code":zipcode,"city":city}
                actual_value = list(add.keys())
                actual_value=sorted(actual_value)
                print("actual",actual_value)
                for i in range(len(content['fields'])):
                    for j in range(len(actual_value)):
                        if content['fields'][i]['name']==actual_value[j]:
                            content['fields'][i]['field_value_original']=add[actual_value[j]]
                            pass
                response = content
                response['error_msg'] = 'null'
        elif 'SSN' in json_val[doc_id]:
            image_path = ssn_noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            thread = threading.Thread(target=get_doc, args=(image_path,json_val[doc_id],))
            thread.start()
            (text,SSN_Number, name) = output_doc.get()
            print("in main",SSN_Number)
            print("in main", name)
            if SSN_Number =='null' and name =='null':
                response={'error_msg':"Invalid image"}
            else:
                if name=='null':
                    name_value.append('-')
                    name_value.append('-')
                    name_value.append('-')
                else:
                    name_value = name.split()
                    print(name_value)
                if len(name_value) > 2:
                    add = {"ssn_number":SSN_Number,"first_name":name_value[0],"last_name":name_value[2],"middle_name":name_value[1]}
                else:
                    add = {"ssn_number": SSN_Number, "first_name": name_value[0], "last_name": name_value[1],"middle_name":"-"
                           }
                actual_value = list(add.keys())
                for i in range(len(content['fields'])):
                    for j in range(len(actual_value)):
                        if content['fields'][i]['name']==actual_value[j]:
                            content['fields'][i]['field_value_original']=add[actual_value[j]]
                            pass

                response = content
                response['error_msg'] = 'null'
        elif "Paystub" in json_val[doc_id]:
            gross_pay, net_pay, pay_frequency, Employer_name, Employer_City, Employer_State=Paystub.get_details(filename)
            if gross_pay =='null' and net_pay =='null' and pay_frequency =='null' and Employer_name =='null' and Employer_City =='null' and Employer_State=='null':
                response = {'error_msg': "Invalid image"}
            else:
                add = {'gross_pay': gross_pay, 'net_pay': net_pay, 'pay_frequency':pay_frequency , 'employer_name': Employer_name,
                       'employer_city': Employer_City, 'employer_state': Employer_State}
                actual_value = list(add.keys())
                actual_value = sorted(actual_value)
                print("actual", actual_value)
                for i in range(len(content['fields'])):
                    for j in range(len(actual_value)):
                        if content['fields'][i]['name'] == actual_value[j]:
                            content['fields'][i]['field_value_original'] = add[actual_value[j]]
                            pass
                response = content
                response['error_msg'] = 'null'
        image_on_web.close()
        print(response)
        response['raw_data']=text
        print("all response",response)
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host='192.168.9.120',port=5013,debug=True)

