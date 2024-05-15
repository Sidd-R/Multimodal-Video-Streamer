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
    # print("Received frame:", len(frame))
    # print("Frame type:", type(frame))
    
    # Decode base64 string to bytes-like object
    # frame_bytes = base64.b64decode(frame.encode('utf-8'))
    # save the frame to a file
    # with open('framew.jpg', 'wb') as f:
    #     f.write(frame_bytes)
        
        

    # # Convert bytes to numpy array
    # nparr = np.frombuffer(frame_bytes, np.uint8)

    # # Check the size of the decoded array
    # print("Decoded frame size:", len(nparr))

    # # Decode image using OpenCV
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # if img is None:
    #     print("Error decoding image from frame")
    #     return

    # # Process the image (e.g., convert to grayscale)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Convert the processed image back to base64 string
    # _, encoded_image = cv2.imencode('.jpg', gray)
    # processed_frame = base64.b64encode(encoded_image).decode('utf-8')

    # # Broadcast the processed frame to all connected clients
    # emit('stream', processed_frame, broadcast=True)
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
