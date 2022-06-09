import machine, network, ntptime, esp32, socket
from machine import Pin, RTC, Timer

# Connect Led to GPIO outputs
grnLed = Pin(32, Pin.OUT)
redLed = Pin(15, Pin.OUT)

# HTTP Get Request
def http_get(url):
    _, _, host, path = url.split("/", 3)
    # host = api.thingspeak.com
    # path = "update?api_key=VGU63KF2QMO4N4V8&field1=" + str(temp) + "&field2=" + str(hall)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

# Send data from esp32 to thingspeak
def measure_and_send(timer):
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    url = "https://api.thingspeak.com/update?api_key=VGU63KF2QMO4N4V8&field1=" + str(temp) + "&field2=" + str(hall)
    http_get(url)
    print("Temperature(°F): " + str(temp))
    print("Hall Sensor: " + str(hall))

# Connect ESP32 to local WiFi
ssid = "2.4 Aspire-UC212"
password = "CXNK00596FC3"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan() 
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print("Connected to: ", ssid)
print("IP Address: ", wlan.ifconfig()[0])

Timer0 = Timer(0)
Timer0.init(period=16000, mode=Timer.PERIODIC, callback=measure_and_send) #t:print(rtc.datetime()))

