import socket
from math import pi
import RPi.GPIO as GPIO
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('172.26.216.164', 2055)
server_socket.bind(server_address)
# GPIO pin number (change it according to your setup)
servo_pin1 = 18
servo_pin2 = 23

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for the servo
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)


# Create a PWM instance
pwm1 = GPIO.PWM(servo_pin1, 50)
pwm2 = GPIO.PWM(servo_pin2, 50) # 50 Hz (change it according to your servo specifications)
  # 50 Hz (change it according to your servo specifications)


# Start the PWM signal with a duty cycle of 0 (servo at 0 degrees)
pwm1.start(0)
pwm2.start(0)


# Function to set the servo angle
def set_angle(angle):
    duty_cycle = 2 + (angle / 18)  # Map angle (0 to 180) to duty cycle (2 to 12)
    pwm1.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)
    
def setangle(angle):
    duty_cycle = 2 + (angle / 18)  # Map angle (0 to 180) to duty cycle (2 to 12)
    pwm2.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)


samplingRate = 0.025

def processTheta(ServoAngle,theta):
    # theta is in degree
    theta = list(map(round,theta))
    ServoAngle = list(map(round,ServoAngle))
    ServoAngle[0] = -ServoAngle[0]+90
    ServoAngle[1] = -ServoAngle[1]+90
    ServoAngle[2] = -ServoAngle[2]+90

    print(ServoAngle)

    if ServoAngle[1] > 10 :
         set_angle(ServoAngle[1])
         
    if ServoAngle[0] > 10 :
         setangle(ServoAngle[0])
    

   

ServoAngle = [0,0,0]

print('Server listening on {}:{}'.format(*server_address))
i = 1
x = []
y = []
z = []
theta = []
while True:
    data, client_address = server_socket.recvfrom(1024)
    decodeData = data.decode('utf-8')
    decodeData = decodeData.removesuffix('#')
    try:
        decodeData = list(map(float,decodeData.split(',')))
    except:
        continue
    #print(decodeData[0],decodeData[1],decodeData[2])
    x.append(decodeData[0])
    y.append(decodeData[1])
    z.append(decodeData[2])
    if i % int(1 / samplingRate) == 0:
        theta = [samplingRate * (180 / pi) * sum(x),
                 samplingRate * (180 / pi) * sum(y),
                 samplingRate * (180 / pi) * sum(z)]

        ServoAngle[0] += theta[0]
        ServoAngle[1] += theta[1]
        ServoAngle[2] += theta[2]
        processTheta(ServoAngle,theta)
        x = []
        y = []
        z = []
        theta = []
    i += 1
