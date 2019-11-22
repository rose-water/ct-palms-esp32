import network
import time
import machine
import network
import ujson
import ssd1306

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

# Pots
adc1 = machine.ADC(machine.Pin(34))
adc1.atten(machine.ADC.ATTN_11DB)

# Touch pins
touchPin = machine.TouchPad(machine.Pin(15))

# OLED Display
i2c      = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23), freq = 100000)
oled     = ssd1306.SSD1306_I2C(128, 32, i2c)

# MQTT
client = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)

# DO NOT DELETE
# Might need if we move interface to OLED
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
  initDisplay()
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(bytes(adafruitFeed,'utf-8'))

  while True:
    # Not sure if we need potentiometer
    # print("pot: " + str(adc1.read()))

    print(touchPin.read())

    if touchPin.read() <= 300:
      initNewConversation()
    else:
      print("no touch happening")

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
  location = str(msg,'utf-8')
  # print((topic, location))
  respondToLocation(location)


# ---------------------------------------------------------------
def initDisplay():
  print("Initializing display.")
  oled.init_display()
  oled.fill(0)
  oled.text("Hello! To chat", 0, 0)
  oled.text("with me, give", 0, 10)
  oled.text("me a hug.", 0, 20)
  oled.show()


# ---------------------------------------------------------------
def initNewConversation():
  print("Starting new conversation.")
  oled.fill(0)
  oled.text("Hi there! I'm an", 0, 0)
  oled.text("LA palm tree ", 0, 10)
  oled.text("from Brazil...", 0, 20)
  oled.show()

  time.sleep(4)
  oled.fill(0)
  oled.text("Tell me where", 0, 0)
  oled.text("you're from!", 0, 10)
  oled.text("<url here>", 0, 20)
  oled.show()


# ---------------------------------------------------------------
def respondToLocation(location):
  print("Responding to location...")
  oled.fill(0)
  oled.text("Nice to meet", 0, 0)
  oled.text("someone from", 0, 10)
  oled.text(location + ("!"), 0, 20)
  oled.show()


# ---------------------------------------------------------------
init()