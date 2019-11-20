import network
import time
import machine
import network
import ujson

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
myMqttClient     = "brazil-palm-01"
adafruitUsername = ADAFRUIT_USERNAME
adafruitAioKey   = ADAFRUIT_PW
adafruitFeed     = adafruitUsername + "/feeds/brazil-palm-01"
adafruitIoUrl    = "io.adafruit.com"

# MQTT
client = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)

# Countries/Cities
# This is an ugly way to do this

# locations = [
#                "Philippines" : [
#                                  { "name" : "Manila",
#                                    "lat" : "<some latitude>" 
#                                    "long" : "<some longitude>"
#                                  },
#                                  ...
#                                 ],
#                ...
#              ] 

# locations = ["Philippines", "Japan", "India", "Spain", "Germany"]
# locations[0] = 
# locations[1] = {}
# locations[2] = {}
# locations[3] = {}

# ---------------------------------------------------------------
def init():
  connectToWifi()
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(bytes(adafruitFeed,'utf-8'))

  while True:
    # Non-blocking wait for message
    client.check_msg()
    time.sleep(1)
  
  client.disconnect()


# ---------------------------------------------------------------
def connectToWifi():
  sta_if = network.WLAN(network.STA_IF)
  
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(yourWifiSSID, yourWifiPassword)

  print("Connected to WiFi.")
  print('Network config:', sta_if.ifconfig())


# ---------------------------------------------------------------
# Callback for received messages on subbed topic
def sub_cb(topic, msg):
  # value = str(msg,'utf-8')
  print((topic, msg))


# ---------------------------------------------------------------
init()