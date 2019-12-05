# ---------------------------------------------------------------
# mexican-palm-06
# ---------------------------------------------------------------
import network
import time
import machine
import network

from umqtt.simple import MQTTClient

from env import ADAFRUIT_USERNAME
from env import ADAFRUIT_PW
from env import WIFI_SSID
from env import WIFI_PW

# ---------------------------------------------------------------
# WIFI
yourWifiSSID     = WIFI_SSID
yourWifiPassword = WIFI_PW

# Adafruit
myMqttClient     = "mexican-palm-06"
adafruitUsername = ADAFRUIT_USERNAME
adafruitAioKey   = ADAFRUIT_PW
adafruitFeed     = adafruitUsername + "/feeds/mexican-palm-06"
adafruitIoUrl    = "io.adafruit.com"

# Solenoid pin
solenoidPin33 = machine.Pin(33, machine.Pin.OUT)

# MQTT
client = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)

# ---------------------------------------------------------------
def init():
  print("Initializing mexican-palm-06")
  connectToWifi()
  
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(bytes(adafruitFeed,'utf-8'))

  while True:
  
    # Non-blocking wait for message
    try:
      client.check_msg()

    finally:
      time.sleep(1)
  
  client.disconnect()


# ---------------------------------------------------------------
def connectToWifi():
  sta_if = network.WLAN(network.STA_IF)
  
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(yourWifiSSID, yourWifiPassword)

    # could hang the device if run with connect() on boot
    while not sta_if.isconnected():
      pass

  print("Connected to WiFi.")
  print('Network config:', sta_if.ifconfig())


# ---------------------------------------------------------------
# Callback for received messages on subbed topic
def sub_cb(topic, msg):
  print(topic, msg)
  value = str(msg,'utf-8')

  if value == "hello_behavior":
    print("value is hello_behavior")

    for i in range(6):
      solenoidPin33.value(1)
      time.sleep(0.2)
      solenoidPin33.value(0)
      time.sleep(0.2)
  
  else: 
    print("value is some other thing")
    
# ---------------------------------------------------------------
init()