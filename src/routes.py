from flask import render_template, request, jsonify
from src import app
from src import find_faces_in_picture_cnn
import face_recognition
import numpy
from PIL import Image




@app.route('/')
@app.route('/home')
def home():
    picture_of_me = face_recognition.load_image_file("pictures/pic1.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    unknown_picture = face_recognition.load_image_file("pictures/pic2.jpg")
    encodings = face_recognition.face_encodings(unknown_picture)
    print(encodings)
    unknown_face_encoding = encodings[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")
    return "toto"

@app.route("/toto")
def toto():
    find_faces_in_picture_cnn.find_faces("pic2.jpg")
    return "yolo"


@app.route("/import_picture_page")
def import_picture_page():
    return render_template(
        'import_picture.html'
    )

@app.route('/submit_picture' , methods=['POST'])
def submit_picture():



    picture = request.files['file']



    if 'file' not in request.files:
        return "No file uploaded"

    if 'username' not in request.form:
        return "Need to give username"

    username = request.form['username']
    filename = picture.filename
    splitted = filename.split('.')

    if len(splitted) == 0:
        return "Problem with filename"

    extension = splitted[len(splitted) - 1]


    picture.save(username + '_tmp.' + extension)

    find_faces_in_picture_cnn.find_faces(username + '.' + extension, username + '_tmp.' + extension)



    return "OK"