import sys
import Adafruit_DHT
import sched
import time
import mail
import sendmail() from mail
import csvwrite
import csvwriter() from csvwrite
import csvrewriter() from csvwrite
#Pin Setup
sensor = Adafruit_DHT.DHT11
pin = 4

#clean csv file before logging starts
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
