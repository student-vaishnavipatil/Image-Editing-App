from flask import Flask,render_template,request
import cv2

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'GrayScale', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def proceesImage(filename,operation):
   print(f"Filename is {filename} and operation is{operation}")
   img=cv2.imread(f"uploads/{filename}")
   match operation:
        case "cgray":
           newfilename=f"static/{filename}"
           imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
           cv2.imwrite(newfilename,imgProcessed)
           return  newfilename
        case "cwebp":
           newfilename=f"static/{filename.split('.')[0]}.webp"
           cv2.imwrite(newfilename,img)
           return newfilename               
        case "cpng":
           newfilename=f"static/{filename.split('.')[0]}.png"
           cv2.imwrite(newfilename,img)
           return newfilename
        case "cjpg":
           newfilename=f"static/{filename.split('.')[0]}.jpg"
           cv2.imwrite(newfilename,img)
           return newfilename
pass

@app.route("/")
def home():
    return render_template('index.html');

@app.route("/about")
def about():
    return render_template('about.html');

@app.route("/contact")
def contact():
    return render_template('contact.html');

@app.route("/documentation")
def documentation():
    return render_template('documentation.html');

@app.route("/edit",methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:

            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=proceesImage(filename, operation)
            flash(f"Your image has been processed and available <a href='/{new} 'target='_blank'>here</a>")
            return render_template("index.html")
        

    return render_template('index.html');

app.run(debug=True,port=5001)