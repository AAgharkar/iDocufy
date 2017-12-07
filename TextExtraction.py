import threading

import os
from flask import Flask, request, render_template,flash
import werkzeug
from flask_session import Session
from multiprocessing import Queue
import Img_to_Text,crop_img,Licence_Details,trail_ssn,SSN_Details,Paystub,noise_reduction

UPLOAD_FOLDER = 'Upload_Image\\'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','JPG','PNG','PDF','JPEG','bmp','BMP'])
app = Flask(__name__,static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess=Session()
output_doc = Queue()
details = Queue()

def get_doc(path):
    text = Img_to_Text.detect_document(path)
    output_doc.put(text)
def get_details(text):
    print(text)
    licence_id, max_date, min_date, iss_date, address,name = Licence_Details.get_licence_details1(text)
    details.put((licence_id, max_date, min_date, iss_date, address,name))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('Index.html')

@app.route("/show", methods=['POST'])
def show():
    try:
        licence_id,max_date, min_date, iss_date,address,SSN_Number,name=None,None,None,None,None,None,None
        if request.method == 'POST':
            file = request.files['file']
            options = request.form['Text_Val']
            if file and allowed_file(file.filename):
                filename = werkzeug.secure_filename(file.filename)
                filename = str(filename).lower()
                file.save(app.config['UPLOAD_FOLDER']+filename)
                image = app.config['UPLOAD_FOLDER']+filename
                # image_path = app.config['UPLOAD_FOLDER']+filename
                if options == 'Licence':
                    image_path=crop_img.get_cropped_image(image)
                    print(image_path)
                    head, tail = os.path.split(image_path)
                    thread = threading.Thread(target=get_doc, args=(image_path,))
                    thread.start()
                    text= output_doc.get()
                    thread = threading.Thread(target=get_details, args=(text,))
                    thread.start()
                    (licence_id, max_date, min_date, iss_date, address,name)=details.get()
                elif options == 'SSN':
                    image_path = trail_ssn.image_conversion_smooth(image)
                    head, tail = os.path.split(image_path)
                    thread = threading.Thread(target=get_doc, args=(image_path,))
                    thread.start()
                    text = output_doc.get()
                    SSN_Number,name=SSN_Details.get_SSN_details1(text)
                # elif options == 'Paystub':
                #     image_path = noise_reduction.image_conversion_smooth(image)
                #     text = Img_to_Text.detect_document(image_path)
                #     # thread = threading.Thread(target=get_doc, args=(image_path,))
                #     # thread.start()
                #     # text = output_doc.get()
                #     # thread = threading.Thread(target=get_details, args=(text,))
                #     # thread.start()
                #     # text = output_doc.get()
                #     text=Paystub.get_paystub_details(text)



            else:
                error = "Please Upload jpg or png image"
                return render_template('Index.html', error=error)

            return render_template('Show.html', text=text,image=tail,licence_id=licence_id,max_date=max_date,min_date=min_date,iss_date=iss_date,address=address,SSN_Number=SSN_Number,name=name)
    except Exception as E:
        print(E)
        error = "Unable to detect"
        return render_template('Index.html', error=error)



if __name__ == "__main__":
    app.secret_key = 'super secret key'

    sess.init_app(app)
    # app.run(host='localhost', port=5004, debug=True, threaded=True)
    app.run(host='192.168.9.120', port=5004, debug=True,threaded=True)