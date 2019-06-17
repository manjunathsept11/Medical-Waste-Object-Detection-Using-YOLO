from flask import Flask, render_template, Response,request
import cv2
import sys
import numpy
import json

from darkflow.net.build import TFNet
import matplotlib.pyplot as plt


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

def get_frame(tfnet):
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port)  
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  
    i=1
    while True:
        retval, im = camera.read()
        if i%25 == 0:
            result = tfnet.return_predict(im)
            if len(result) == 0:
                pass
            else :
                print("Non Empty")
                tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
                br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
                label = result[0]['label']
                im = cv2.rectangle(im, tl, br, (0, 255, 0), 7)
                im = cv2.putText(im, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
    del(camera)

@app.route('/calc')
def calc():
    options = {'model': 'cfg/yolo.cfg','load': 'bin/yolov2.weights','threshold': 0.6,'gpu':1.0}
    tfnet = TFNet(options)
    return Response(get_frame(tfnet),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Model.html')
def Model():
    return render_template('Model.html')

@app.route('/Predict.html')
def Predict():
    return render_template('Predict.html')

if __name__ == "__main__":
    app.run(port=5000,debug =True)