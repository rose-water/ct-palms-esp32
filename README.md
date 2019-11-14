# Creative Technology I: LA Embedded Device
### Rachel Rose Waterhouse
### Tingyi Li

-----
#### LA Palms + People Provenance
Brief goes here

-----
### I. Credentials
This project uses the [Adafruit IO MQTT API](https://io.adafruit.com/api/docs/mqtt.html#adafruit-io-mqtt-api).

You will need to create a `env.py` file with your adafruit.io username,  password, WiFi SSID, and WiFi password. 

```
# env.py
ADAFRUIT_USERNAME = "<Your AdafruitIO Username>"
ADAFRUIT_PW       = "<Your AdafruitIO Key>"
WIFI_SSID         = "<Your WiFi SSID>"
WIFI_PW           = "<Your WiFi PW>"
```

`boot.py` imports these variables from that file. 

---
### II. Prerequisites
Plug in your board and start the REPL:

`screen /dev/tty.SLAB\_USBtoUART 115200`

Install the mqtt module for ESP32:

```
>>> import upip
>>> upip.install("micropython-umqtt.simple")
```

---
### III. Run
`cd` into the code directory and use `ampy`[](https://github.com/scientifichackers/ampy) to upload `boot.py` and `env.py` to your board (make sure you exit the REPL first):

```
ampy -p /dev/tty.SLAB_USBtoUART put boot.py
ampy -p /dev/tty.SLAB_USBtoUART put env.py
```

Finally, start the REPL again. You may need to use `control + D` to reboot the device.


For more information on setting up ESP32 with Adafruit IO, go [here](https://github.com/pvanallen/esp32-getstarted/blob/master/docs/io-adafruit.md).


---
### IV. Documentation
#### TBD