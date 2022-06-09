import machine
from machine import Pin, RTC, Timer, TouchPad, deepsleep, wake_reason
import network, ntptime, esp32

def DisplayTime(time):
    print("Date: " + str(rtc.datetime()[1]) + "/" + str(rtc.datetime()[2]) + "/" + str(rtc.datetime()[0]))
    print("Time: " + str(rtc.datetime()[4]) + ":" + str(rtc.datetime()[5]) + ":" + str(rtc.datetime()[6]) + " HRS")

def GrnLedTouchSensor(time):
    if touch.read() < 200:
        grnLed.value(1)
    else:
        grnLed.value(0)

def DeepSleep(time):
    print("I am going to sleep for 1 minute.")
    redLed.value(0)
    deepsleep(60000) # put the device to sleep for 1 min
    
def WakeReason():
    if wake_reason() == 2:
        print("Woke up due to External wakeup mode 0.")
    elif wake_reason() == 4:
        print("Woke up due to Timer.")
        
WakeReason()      
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

# Display Current Date and Time using Network Time Protocol (NTP)
rtc = RTC()
ntptime.settime() # set the rtc datetime from the remote server
year, month, day, weekday, hour, minute, second, microsecond = rtc.datetime()
rtc.datetime((year, month, day, weekday, hour-4, minute, second, microsecond)) # manually adjust the RTC to convert UTC to local time

dateTime = Timer(0)
dateTime.init(period=15000, mode=Timer.PERIODIC, callback=DisplayTime) #t:print(rtc.datetime()))

# Green LED Control by Touch Input
touch = TouchPad(Pin(12))
grnLed = Pin(32, Pin.OUT)

touchTimer = Timer(1)
touchTimer.init(period=50, mode=Timer.PERIODIC, callback=GrnLedTouchSensor)

# Red LED, Deep Sleep and Different Wake Up Sources
redLed = Pin(15, Pin.OUT)
button = Pin(33, Pin.IN)

redLed.value(1)

esp32.wake_on_ext0(button, esp32.WAKEUP_ANY_HIGH) # Wake up by using button

redLedTimer = Timer(2)
redLedTimer.init(period=30000, mode=Timer.PERIODIC, callback=DeepSleep) # Wake up by timer


    








