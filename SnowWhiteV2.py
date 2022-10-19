import time
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c, address=0x42)

pca.frequency = 50

witch = servo.Servo(pca.channels[0]) # start 60, 120, 2
doc = servo.Servo(pca.channels[1]) # 40, 130, 2
happy = servo.Servo(pca.channels[2]) # 75 brush up, 100 brush down, 2
dopey = servo.Servo(pca.channels[3])# 80, 105, 2
sleepy = servo.Servo(pca.channels[4])# 65, 90, 2 or 3
grumpy = servo.ContinuousServo(pca.channels[5], min_pulse=750, max_pulse=2250)
sneezy = servo.Servo(pca.channels[6])# 80 down, 100 up, 2
bashful = servo.Servo(pca.channels[7])# 70down, 90up, 2
snow = servo.Servo(pca.channels[8]) # 60, 120, 1

def moveServo(start,stop,delta):
    incMove = (stop-start)/100.0
    incTime = delta/100.0
    #using start angle(first value in moveServo) plus incremental moves(incMove) to rotate servo to stop angle in time(delta) increments(incTime) specified
    for x in range(100):
        witch.angle = start + x*incMove 
        doc.angle = stop+10 - x*(incMove + .3) # 0.3 to account for incTime and incMove to keep servo in line with start/stop values,
                                               # otherwise servo will jump at endpoints. stop used in this line to rotate servo opposite direction
        happy.angle = start+15 + x*(incMove - .35)
        dopey.angle = start+20 + x*(incMove - .35)
        sleepy.angle = start+5 + x*(incMove - .35)
        grumpy.throttle = -.125 # minus is a forward rotation, positive is a backwards rotatoin. 1 and -1 are full throttle in either direction
        sneezy.angle = start+20 + x*(incMove - .30)#the .3 adjustment here makes him lunge forward like he is sneezing / .4 for smooth operation
        bashful.angle = stop-30 - x*(incMove - .40)
        snow.angle = start + x*incMove
        time.sleep(incTime)
    #grumpy.throttle = 0 #This will br used if we want to change the direction of rotation.
    for x in range(100):
        witch.angle = stop - x*incMove
        doc.angle = start-20 + x*(incMove + .3)
        happy.angle = stop-20 - x*(incMove - .35)
        dopey.angle = stop-15 - x*(incMove - .35)
        sleepy.angle = stop-30 - x*(incMove - .35)
        #grumpy.throttle = .125  This will be used if we want to change the direction of rotation.
        sneezy.angle = stop-30 - x*(incMove - .40)
        bashful.angle = start+10 + x*(incMove - .40)
        snow.angle = stop - x*incMove
        time.sleep(incTime)
        
 
playing = True
while playing:
    moveServo(60,120,2)
#grumpy.throttle = 0    

pca.deinit()
pca.reset()