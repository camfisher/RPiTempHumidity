import sys

import Adafruit_DHT
import csv
import sched
import time
import datetime
import smtplib
import mail

from mail import sendemail
#Pin Setup
sensor = Adafruit_DHT.DHT11
pin = 4
#Setup csv Editor with h as Humidity Input and t as Temperature Input Then Compute Time in Hours
def csvwriter(h, t):
    with open('TemperatureHumidity.csv', mode='a') as TemperatureHumidity:
        TemperatureHumidity_Writer = csv.writer(TemperatureHumidity, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        now = datetime.datetime.now()
        timeh = now.hour + (now.minute / 60)
        TemperatureHumidity_Writer.writerow([timeh, h, t])
    return;

print ("Logging Temperature and Humidity")
#Setup Scheduler to Run Logger Every 300 Seconds or Five Minutes
itr = 0
s = sched.scheduler(time.time, time.sleep)
def logtemphumid(sc):
    print ("Logging Temperature and Humidity")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #Write data
    csvwriter(humidity, temperature)
    #Create and Send Email
    if (itr >= 47): #47 Iterations Being 24 Hours with zero being the first
        sendemail()
        itr = 0
    itr+=1
    s.enter(1800, 1, logtemphumid, (sc,))

#Run Logger
s.enter(1800, 1, logtemphumid, (s,))
s.run()
