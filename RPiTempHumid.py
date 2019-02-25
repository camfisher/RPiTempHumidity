import Adafruit_DHT
import csv

sensor = Adafruit_DHT.DHT_11
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
