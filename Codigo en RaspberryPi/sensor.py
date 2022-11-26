import board
import busio
import time
import adafruit_bmp280
import json
import RPi.GPIO as GPIO
from time import sleep

def sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

    sensor.sea_level_pressure=1013.25

    temp = round(sensor.temperature, 2)
    press = round(sensor.pressure, 2)
    alt = round(sensor.altitude, 2)
    print("Temperature: "+ str(temp) + "°C  "+"Pressure: "+str(press)+"   Altitude: " + str(alt))
    return [temp,press,alt]




def flama():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN)
    
    return GPIO.input(23)

def led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22,GPIO.OUT)
    for i in range(5):
        GPIO.output(22,GPIO.HIGH)
        sleep(1)
        
    
    
def clean():
    GPIO.cleanup()
    
def ledFin():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22,GPIO.OUT)
    for i in range(5):
        GPIO.output(22,GPIO.LOW)
        sleep(1)
    

    

