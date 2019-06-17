from flask import Flask, render_template, Response,request
import cv2
import sys
import numpy
import json


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Model.html')

def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1

def get_frame():
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port)    
    i=1
    while True:
        retval, im = camera.read()
        im = cv2.rectangle(im,(85, 115) , (550, 462), (0, 255, 0), 7)
        im = cv2.putText(im, 'bicycle', (85, 115), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)


        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
    del(camera)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Model.html')
def Model():
    return render_template('Model.html')

@app.route('/Predict.html')
def Predict():
    return render_template('Predict.html')

if __name__ == "__main__":
    app.run(port=5000,debug =True)