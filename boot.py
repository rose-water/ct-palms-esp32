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
myMqttClient     = "brazil-palm-01"
adafruitUsername = ADAFRUIT_USERNAME
adafruitAioKey   = ADAFRUIT_PW
adafruitFeed     = adafruitUsername + "/feeds/testTopic"
adafruitIoUrl    = "io.adafruit.com"

# MQTT
client = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)

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