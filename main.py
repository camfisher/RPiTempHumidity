import sys
import Adafruit_DHT
import sched
import time
import mail
from mail import sendmail
import csvwrite
from csvwrite import csvwriter
from csvwrite import csvrewriter
import configparser

#Get data from config file
Config = configparser.ConfigParser()
Config.read("config.cfg")
cfgsensor = Config.get('MAIN', 'Sensor')
sensor = Adafruit_DHT.DHT11
if (cfgsensor == "DHT11"):
    sensor = Adafruit_DHT.DHT11
elif (cfgsensor == "DHT22"):
    sensor = Adafruit_DHT.DHT22
else:
    print ("Sensor Unknown")

pin = Config.getint('MAIN', 'GPIOpin')
logtime = Config.getint('MAIN', 'Time')
logiterations = Config.getint('MAIN', 'Iterations')

#clean csv file before logging starts
csvrewriter()
#Setup Scheduler to Run Logger Every 1800 Seconds or Thirty Minutes
itr = 0
s = sched.scheduler(time.time, time.sleep)
def logtemphumid(sc):
    global itr
    global logtime
    global logiterations
    print ("Logging Temperature and Humidity")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #Check if Humidity is over 100%
    while (humidity > 100):
        print ("Error: Humidity Exceeded 100%... Correcting")
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        time.sleep(3)
    #Convert Temperature From Celsius to Fahrenheit
    temperature = (temperature*1.8) + 32
    #Write data
    csvwriter(humidity, temperature)
    #Create and Send Email
    if (itr >= logiterations):
        sendemail()
        csvrewriter()
        itr = 0

    itr+=1
    s.enter(logtime, 1, logtemphumid, (sc,))

#Run Logger
s.enter(logtime, 1, logtemphumid, (s,))
s.run()
