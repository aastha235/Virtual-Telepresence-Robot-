from flask import Flask, render_template, request, redirect, url_for, make_response, Response
import time
import RPi.GPIO as GPIO
import picamera
import socket
from math import pi



mA1 = 17
mA2 = 27
mB1 = 24
mB2 = 25

 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(mA1, GPIO.OUT)
GPIO.setup(mA2, GPIO.OUT)
GPIO.setup(mB1, GPIO.OUT)
GPIO.setup(mB2, GPIO.OUT)
GPIO.output(mA1, 0)
GPIO.output(mA2, 0)
GPIO.output(mB1, 0)
GPIO.output(mB2, 0)


app = Flask(__name__)  # set up Flask server
#camera = picamera.PiCamera()
 
 
# when the root IP is selected, return index.html page
@app.route('/')
def index():
    return render_template('index.html')
 
#def video_stream():
#    while True:
#        time.sleep(0.1)
#        frame = camera.capture_continuous(
#           format = 'jpeg', use_video_port = True, quality = 90
#        )
#        yield(b'--frame\r\n'
#              b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')
        
#@app.route('/video_feed')
#def video_feed():
#    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
# receive which pin to change from the button press on index.html
# each button returns a number that triggers a command in this function
#
# Uses methods from motors.py to send commands to the GPIO to operate the motors
@app.route('/<direction>', methods=['GET'])
def move(direction):  
    if direction == 'left_side':
        print("Left")
        GPIO.output(mA1, 0)
        GPIO.output(mA2, 1)
        GPIO.output(mB1, 1)
        GPIO.output(mB2, 0)
    elif direction == 'up_side':
        print("Forward")
        GPIO.output(mA1, 1)
        GPIO.output(mA2, 0)
        GPIO.output(mB1, 1)
        GPIO.output(mB2, 0)
    elif direction == 'right_side':
        print("Right")
        GPIO.output(mA1, 1)
        GPIO.output(mA2, 0)
        GPIO.output(mB1, 0)
        GPIO.output(mB2, 1)
    elif direction == 'down_side':
        print("Reverse")
        GPIO.output(mA1, 0)
        GPIO.output(mA2, 1)
        GPIO.output(mB1, 0)
        GPIO.output(mB2, 1)
    else:
        GPIO.output(mA1, 0)
        GPIO.output(mA2, 0)
        GPIO.output(mB1, 0)
        GPIO.output(mB2, 0)
 
    response = make_response(redirect(url_for('index')))
    return response
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    


