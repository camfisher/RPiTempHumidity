import Adafruit_DHT
import csv
import sched
import time
import datetime

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
s = sched.scheduler(time.time, time.sleep)
def logtemphumid(sc):
    print "Logging Temperature and Humidity"
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #Write data
    csvwriter(humidity, temperature)
    s.enter(300, 1, logtemphumid, (sc,))
    return;

#Run Logger
s.enter(300, 1, logtemphumid, (s,))
s.run()
