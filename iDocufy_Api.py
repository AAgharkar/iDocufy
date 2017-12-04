import threading

import os
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

        content = request.json
        print(content['file_path'])
        doc_name=content['doc_id']
        image_on_web= urlopen("http://192.168.9.81:5011/uploads/"+content['file_path'])
        url="http://192.168.9.81:5011/uploads/"+content['file_path']
        filename = os.path.basename(url)
        print(filename)
        # pieces = url.split("/")
        # length = len(pieces)
        # filename = pieces[length - 1:length]
        buf = image_on_web.read()
        print(buf)
        with open("Upload_Image/"+filename, "wb") as downloaded_image:
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        if doc_name=='4':
            image_path = noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            print(image_path)
            thread = threading.Thread(target=get_doc, args=(image_path,))
            thread.start()
            text = output_doc.get()
            thread = threading.Thread(target=get_details, args=(text,))
            thread.start()
            (licence_id, max_date, min_date, iss_date, address, name) = details.get()
            response={
                "name":name,
                "licence_id":licence_id,
                "date_of_birth":min_date,
                "issue_date":iss_date,
                "expire_date":max_date,
                "address":address
            }

        elif doc_name=='2':
            image_path = ssn_noise_reduction.image_conversion_smooth("Upload_Image/"+filename)
            thread = threading.Thread(target=get_doc, args=(image_path,))
            thread.start()
            text = output_doc.get()
            thread = threading.Thread(target=get_ssn_details, args=(text,))
            thread.start()
            (SSN_Number, name)=details.get()
            response = {
                "name": name,
                "SSN":SSN_Number
            }
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host='192.168.9.120',port=5013, debug=True)

