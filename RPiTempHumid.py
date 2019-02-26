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
        TemperatureHumidity_Writer.writerow(["%.2f" % round(timeh,2), "%.2f" % round(h,2), "%.2f" % round(t,2)])

#csv Rewriter to reset the csv file at the end of the day
def csvrewriter():
    with open('TemperatureHumidity.csv', mode='w') as TemperatureHumidity:
        TemperatureHumidity_Writer = csv.writer(TemperatureHumidity, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        TemperatureHumidity_Writer.writerow(["Time", "Humidity%", "Temperature"])
        
#clean csv file before loging starts
csvrewriter()
#Setup Scheduler to Run Logger Every 1800 Seconds or Thirty Minutes
itr = 0
s = sched.scheduler(time.time, time.sleep)
def logtemphumid(sc):
    global itr
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
    if (itr >= 47): #47 Iterations Being 24 Hours with zero being the first
        sendemail()
        csvrewriter()
        itr = 0
        
    itr+=1
    s.enter(2, 1, logtemphumid, (sc,))

#Run Logger
s.enter(2, 1, logtemphumid, (s,))
s.run()
