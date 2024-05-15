from flask import Flask, render_template, Response, request , jsonify
import cv2
import random
import json
import numpy as np
import base64
import os , io , sys
from PIL import Image
from flask_socketio import SocketIO, emit
import imutils

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('stream')
def handle_stream(image):
    sbuf = io.StringIO()
    sbuf.write(image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_BGR2GRAY)

    # Process the image frame
    # frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData
    
    print("Emitting frame")

    # emit the frame back
    emit('stream', stringData)

if __name__ == '__main__':
    socketio.run(app, debug=True)
