from flask import Flask, render_template, Response,request
import cv2
import sys
import json
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import time
import tensorflow as tf

import winsound

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


def get_frame(tfnet,colors):

    frequency = 2500
    duration = 100

    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture('TestingVdo/2.mp4')
    #capture = cv2.VideoCapture('TestingVdo/2.mp4')
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

    i=1
    while True:
        stime = time.time()
        retval, im = camera.read()
        if retval:
            results = tfnet.return_predict(im)
            for color, result in zip(colors, results):
                tl = (result['topleft']['x'], result['topleft']['y'])
                br = (result['bottomright']['x'], result['bottomright']['y'])
                label = result['label']
                confidence = result['confidence']
                text = '{}: {:.0f}%'.format(label, confidence * 100)
                im = cv2.rectangle(im, tl, br, color, 5)
                im = cv2.putText(im, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                winsound.Beep(frequency, duration)
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
    del(camera)

@app.route('/calc')
def calc():
    run_opts = tf.RunOptions(report_tensor_allocations_upon_oom = True)
    options = {'model': 'cfg/medicalobjectdetection.cfg','load':5125,'threshold': 0.13,'gpu':1.0}
    tfnet = TFNet(options)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
    return Response(get_frame(tfnet,colors),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Model.html')
def Model():
    return render_template('Model.html')

@app.route('/Predict.html')
def Predict():
    return render_template('Predict.html')

if __name__ == "__main__":
    app.run(port=5000,debug =True)