from time import sleep
import RPi.GPIO as GPIO
import random
import time
import picamera
import Adafruit_LSM303

camera = picamera.PiCamera()    # Setting up the camera
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)
acceleration = Adafruit_LSM303.LSM303()


def beginRecording():
    camera.start_recording(fileName() +'.h264') # Video will be saved at desktop

def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)

def getAcceleration():
   accel, mag = acceleration.read()
   accel_x, accel_y, accel_z = accel
   mag_x, mag_y, mag_z = mag
   return accel_x, accel_y, accel_z
    #return random.randint(1, 10000)

def fileName():
    name=time.asctime()
    return name

beginRecording()
sleep(2) #delay between recording start and release
setAngle(35) #release 
file1 = open(r"accelerationinfo.txt","a+")
file1.write(fileName()+"\n")
for x in range(300):
	accelx,accely,accelz = getAcceleration()
	accelx = str(accelx)
	accely = str(accely)
	accelz = str(accelz)
	file1.write("X Axis: " + accelx + "  Y Axis: " + accely + "  Z Axis: " + accelz + "\n")
	sleep(.03)
	file1.write("\n")
camera.stop_recording()
pwm.stop()
GPIO.cleanup()
