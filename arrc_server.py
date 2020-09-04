import RPi.GPIO as GPIO
from flask import Response
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
from flask import Flask
import datetime
from flask import render_template
from flask_cors import CORS
from flask import request
import cv2
import threading
from flask import send_file
import time

#globals
outputFrame = None
app = Flask(__name__)
CORS(app) # This will enable CORS for all routes
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()
angle = 90

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(7.5)

time.sleep(1)


def SetAngle(angle):
    global p , servoPIN
    duty = angle / 18 + 2.5
    #GPIO.output(servoPIN, True)
    p.ChangeDutyCycle(duty)
    time.sleep(0.01)
    #GPIO.output(servoPIN, False)

def generate_frame():
    global outputFrame, fps
	# loop over frames from the output stream
    while fps._numFrames%300==0:
        outputFrame = vs.read()
        outputFrame = imutils.resize(outputFrame, width=400)
        #timestamp = datetime.datetime.now()
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ar")
def ar():
    return render_template("interior_stereo_eyes_background_andr.html")

@app.route("/video_socket")
def video_socket():
    return Response(generate_frame(),mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/servo_socket")
def servo_socket():
    global p, angle
    curangle = 180.0 - request.args.get('angle', default = 90, type = int)
    if curangle != angle:
        SetAngle(curangle)
        angle = curangle
    return "angle is set to: " + str(angle)


if __name__ == '__main__':
    SetAngle(90)
    app.run(host="10.42.0.1", port="5000", ssl_context=('./certs/server.crt', './certs/server.key'), debug=False, use_reloader=False)

fps.stop()
vs.stop()
p.stop()
GPIO.cleanup()