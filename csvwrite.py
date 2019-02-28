import csv
import datetime

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
