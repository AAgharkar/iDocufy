import threading

import os

import requests
from flask import Flask, request, json
from multiprocessing import Queue
from urllib.request import urlopen
import Img_to_Text
import Licence_Details
import SSN_Details
import crop_img
import noise_reduction
import ssn_noise_reduction

app = Flask(__name__,static_folder='static')
output_doc = Queue()
details = Queue()

def get_doc(path):
    text = Img_to_Text.detect_document(path)
    output_doc.put(text)
def get_details(text):
    print(text)
    licence_id, max_date, min_date, iss_date, address,name = Licence_Details.get_licence_details1(text)
    details.put((licence_id, max_date, min_date, iss_date, address,name))
def get_ssn_details(text):
    SSN_Number, name = SSN_Details.get_SSN_details1(text)
    details.put((SSN_Number, name))
@app.route("/api/ocr", methods=['POST'])
def index():
    if request.method == 'POST':
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
        buf = image_on_web.read()
        with open("Upload_Image/"+filename, "wb") as downloaded_image:
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        val = content['fields']
        field_val=dict([(val[i]['id'],val[i]['name']) for i in range(len(content['fields']))])
        data_value = list(field_val.values())
        # field_val=dict([(val[i]['id'], val[i]['name']) for i in range(len(content['fields']))])
        # print([val[i]['name'] for i in range(len(content['fields']))])
        # print(content['fields'][0]['name'])
        if 'License' in json_val[doc_id]:
            print("hello")
            image_path = noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            print(image_path)
            thread = threading.Thread(target=get_doc, args=(image_path,))
            thread.start()
            text = output_doc.get()
            thread = threading.Thread(target=get_details, args=(text,))
            thread.start()
            (licence_id, exp_date, dob, iss_date, address, name) = details.get()
            if licence_id =='null' and exp_date =='null' and dob =='null' and iss_date =='null' and address =='null' and name=='null':

                response = {'error_msg': "Invalid image"}
            else:
                if name=='null':
                    name_value=[]
                    name_value[0]='null'
                    name_value[1] = 'null'
                    name_value[2] = 'null'
                else:
                    name_value=name.split()
                if len(name_value)>2:
                    add = {'first name': name_value[1], 'dob': dob, 'issue date': iss_date,
                           'expiration date': exp_date, 'last name': name_value[0], 'address': address, 'license id': licence_id,"middle name":name_value[2]}
                else:
                    add = {'first name': name_value[0], 'dob': dob, 'issue date': iss_date,
                           'expiration date': exp_date, 'last name': name_value[1], 'address': address,
                           'license id': licence_id}
                actual_value = list(add.keys())
                for i in range(len(data_value)):
                    if actual_value[i].lower() in map(str.lower, data_value):
                        response=add

                    else:
                        del add[actual_value[i]]
                response['error_msg']="null"
                # for i in range(len(data_value)):
                #     if actual_value[i].lower() in map(str.lower, data_value):
                #         response=actual_value
                #     else:
                #        response=actual_value.pop(actual_value.index(actual_value[i]))
        elif 'SSN' in json_val[doc_id]:
            image_path = ssn_noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            thread = threading.Thread(target=get_doc, args=(image_path,))
            thread.start()
            text = output_doc.get()
            thread = threading.Thread(target=get_ssn_details, args=(text,))
            thread.start()
            (SSN_Number, name)=details.get()
            print("in main",SSN_Number)
            print("in main", name)
            if SSN_Number =='null' and name =='null':
                response={'error_msg':"Invalid image"}
            else:
                if name=='null':
                    name_value.append('null')
                    name_value.append('null')
                    name_value.append('null')
                else:
                    name_value = name.split()
                    print(name_value)
                if len(name_value) > 2:
                    add = {"SSN Number":SSN_Number,"first name":name_value[0],"last name":name_value[2],"middle name":name_value[1]}
                else:
                    add = {"SSN Number": SSN_Number, "first name": name_value[0], "last name": name_value[1]
                           }
                actual_value = list(add.keys())
                print(data_value)
                for i in range(len(actual_value)):
                    if actual_value[i].lower() in map(str.lower, data_value):
                        response=add
                        print("rrr",response)
                    else:
                        del add[actual_value[i]]
                        response=add
                response['error_msg']='null'
        # d={'raw_data':text}
        print(response)
        response['raw_data']=text
        print("all response",response)
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host='192.168.9.120',port=5013, debug=True)

