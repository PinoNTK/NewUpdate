import cv2 as cv
import os


haarcascade_frontalface = os.path.join(os.path.dirname(__file__),'data/haarcascade_frontalface_default.xml')
def detect_face(path_file):
    face_cascade = cv.CascadeClassifier(haarcascade_frontalface)
    # eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
    img = cv.imread(path_file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces)>0:
        return True
    return False