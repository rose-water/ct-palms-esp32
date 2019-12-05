# ---------------------------------------------------------------
# brazil-palm-01
# ---------------------------------------------------------------
import network
import time
import machine
import network
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

# Touch pins
touchPin = machine.TouchPad(machine.Pin(15))

# Solenoid pin
solenoidPin33 = machine.Pin(33, machine.Pin.OUT)

# OLED Display
i2c      = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23), freq = 100000)
oled     = ssd1306.SSD1306_I2C(128, 32, i2c)

# MQTT
client = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)

# ---------------------------------------------------------------
def init():
  connectToWifi()
  initDisplay()
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(bytes(adafruitFeed,'utf-8'))

  isConversationHappening = False

  while True:
    
    if touchPin.read() <= 300 and isConversationHappening == False:
      initNewConversation()
      isConversationHappening = True

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
def initDisplay():
  print("Initializing display.")
  oled.init_display()
  oled.fill(0)
  oled.text("........", 0, 0)
  oled.text("Shake my hand!", 0, 10)
  oled.show()


# ---------------------------------------------------------------
def initNewConversation():
  print("Starting new conversation.")
  oled.fill(0)
  oled.text("10.60.6.140:3000", 0, 0)
  oled.text("/chat?palmId=", 0, 10)
  oled.text("brazil-palm-01", 0, 20)
  oled.show()


# ------------------------------------------------------------
# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def translate(value, leftMin, leftMax, rightMin, rightMax):
  # Figure out how 'wide' each range is
  leftSpan = leftMax - leftMin
  rightSpan = rightMax - rightMin

  # Convert the left range into a 0-1 range (float)
  valueScaled = float(value - leftMin) / float(leftSpan)

  # Convert the 0-1 range into a value in the right range.
  return rightMin + int(valueScaled * rightSpan)


# ---------------------------------------------------------------
init()