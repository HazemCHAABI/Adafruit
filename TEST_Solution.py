from network import WLAN
from mqtt import MQTTClient
from network import Bluetooth
import time
import pycom

# WiFi settings
WIFI_SSID = 'Your_WiFi_SSID'
WIFI_PASS = 'Your_WiFi_Password'

# Adafruit IO settings
ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'Your_Username'
ADAFRUIT_IO_KEY = 'Your_AIO_Key'
ADAFRUIT_FEED = 'Your_Feed_Name'

# Initialize and connect to WiFi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=5000)
while not wlan.isconnected():
    time.sleep(1)
print("WiFi connected!")

# Function to adjust LED brightness
def adjust_light(value):
    # Scale the value from 0-100 to 0-255 for LED brightness
    brightness = int((int(value) * 255) / 100)
    # Set the RGB LED color (here we use white color with variable brightness)
    pycom.rgbled(0xffffff & (brightness | (brightness << 8) | (brightness << 16)))

# Function to handle messages from Adafruit IO
def sub_cb(topic, msg):
    print("Received:", msg)
    adjust_light(msg)  # Adjust light based on received value
    data_characteristic.value(msg)

# Initialize MQTT client and subscribe to Adafruit IO feed
client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_IO_URL, user=ADAFRUIT_USERNAME, password=ADAFRUIT_IO_KEY, port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(bytes('{}/feeds/{}'.format(ADAFRUIT_USERNAME, ADAFRUIT_FEED), 'utf-8'))

# Initialize Bluetooth
bluetooth = Bluetooth()
bluetooth.set_advertisement(name='PycomSensor', service_uuid=b'1234567890123456')
service = bluetooth.service(uuid=b'1234567890123456', isprimary=True)
data_characteristic = service.characteristic(uuid=b'ab34567890123456', properties=Bluetooth.PROP_READ)

# Main loop
while True:
    client.check_msg()
    bluetooth.advertise(True)
    time.sleep(10)
    bluetooth.advertise(False)
