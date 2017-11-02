import threading

import os
from flask import Flask, request, render_template,flash
import werkzeug
from flask_session import Session
from multiprocessing import Queue
import Img_to_Text,crop_img,Licence_Details

UPLOAD_FOLDER = 'Upload_Image\\'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','JPG','PNG','PDF','JPEG','bmp','BMP'])
app = Flask(__name__,static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess=Session()
output_doc = Queue()

def get_doc(path):
    text = Img_to_Text.detect_document(path)
    output_doc.put(text)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    field=['abc','abc','abc','abc','abc','abc','abc','abc','abc','abc','abc']
    return render_template('Index.html',field=field)

@app.route("/show", methods=['POST'])
def show():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = werkzeug.secure_filename(file.filename)
                filename = str(filename).lower()
                file.save(app.config['UPLOAD_FOLDER']+filename)
                image = app.config['UPLOAD_FOLDER']+filename
                image_path=crop_img.get_cropped_image(image)
                print(image_path)
                head, tail = os.path.split(image_path)
                thread = threading.Thread(target=get_doc, args=(image_path,))
                thread.start()
                text= output_doc.get()
                licence_id,max_date,min_date,iss_date=Licence_Details.get_licence_details(text)

            else:
                error = "Please Upload jpg or png image"
                return render_template('Index.html', error=error)
            # return render_template('Show.html', text=text,image=tail)
            return render_template('Show.html', text=text,image=tail,licence_id=licence_id,max_date=max_date,min_date=min_date,iss_date=iss_date)
    except Exception as E:
        error = "Licence ID not Detected"
        return render_template('Index.html', error=error)

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    sess.init_app(app)
    # app.run(host='localhost', port=5004, debug=True, threaded=True)
    app.run(host='192.168.0.224', port=1234, debug=True,threaded=True)