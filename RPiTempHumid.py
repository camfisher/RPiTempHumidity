import Adafruit_DHT
import csv
import sched
import time
import datetime
import smtplib
import ssl
import email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Email Setup
port = 465 #For SSL
pasword = "password"
#gmail only
email = "My@gmail.com"
destemail = "Dest@gmail.com"
subject = "Your Temperature and Humidity Data"
body = "Temperature and Humidity CSV"

#Create SSL Context
context = ssl.create_default_context()

#Pin Setup
sensor = Adafruit_DHT.DHT_11
pin = 4

#Setup csv Editor with h as Humidity Input and t as Temperature Input Then Compute Time in Hours
def csvwriter(h, t)
    with open('TemperatureHumidity.csv', mode='w') as TemperatureHumidity:
        TemperatureHumidity_Writer = csv.writer(TemperatureHumidity, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        now = datetime.datetime.now()
        timeh = now.hour + (now.minute / 60)
        TemperatureHumidity_Writer.writerow([timeh, h, t])
    return;

#Setup Scheduler to Run Logger Every 300 Seconds or Five Minutes
itr = 0
s = sched.scheduler(time.time, time.sleep)
def logtemphumid(sc):
    print "Logging Temperature and Humidity"
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #Write data
    csvwriter(humidity, temperature)
    #Create and Send Email
    if itr == 48 #48 Iterations Being 24 Hours
    
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, password)
    itr+=1
    s.enter(1800, 1, logtemphumid, (sc,))

#Run Logger
s.enter(1800, 1, logtemphumid, (s,))
s.run()
