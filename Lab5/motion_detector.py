import machine, network, ntptime, esp32, struct
import urequests as requests
from machine import Pin, I2C, Timer

def accelerometer():
    xyz = i2c.readfrom_mem(acc_addr, 0x32, 6) # read 6 bytes of all xyz from memory
    ax = struct.unpack('hhh', xyz)[0]/256
    ay = struct.unpack('hhh', xyz)[1]/256
    az = struct.unpack('hhh', xyz)[2]/256
    # print("x:" + str(ax))
    # print("y:" + str(ay))
    # print("z:" + str(az))
    return (ax, ay, az)

## Calculating Offset
# totalx = 0
# totaly = 0
# totalz = 0
# for i in range(15):
#     acc = accelerometer()
#     ax = acc[0]
#     ay = acc[1]
#     az = acc[2]
#     print("detect: ", ax, ay, az)
#     totalx += acc[0]
#     totaly += acc[1]
#     totalz += acc[2]
#     
# avgx = totalx / 15
# avgy = totaly / 15
# avgz = totalz / 15
# print(avgx, avgy, avgz)
# print(avgx.to_bytes(1))
# print(avgy.to_bytes(1))
# print(avgz.to_bytes(1))
    
    
activationFlag = False
# Detect motion
def detect_motion(timer):
    # global activationFlag
    # print(activationFlag)
    if activationFlag == True:
        acc = accelerometer()
        ax = acc[0]
        ay = acc[1]
        az = acc[2]
        # print("detect: ", ax, ay, az)
        if ax >= 0.06 or ax <= -0.06 or ay >= 0.06 or ay <= -0.06 or az >= 1.1 or az <= -1.1:
            redLed(1)
            loop(ax,ay,az)
        else:
            redLed(0)
    
# Using ESP32 to read data from ThingSpeak to check activation
def activation_detection(timer):
    if wlan.isconnected():
        res = requests.get(url= 'https://api.thingspeak.com/channels/1600761/fields/1.json?api_key=11VBP5OAVWLRZICZ&results=2')
        data = res.json()
        activation = data["feeds"][-1]["field1"]
        print(activation) 
        
        global activationFlag
        if activation == "activate":
            grnLed(1) # system is in armed state
            activationFlag = True
        else:
            grnLed(0) # system is in disarmed state
            redLed(0)
            activationFlag = False
            
    res.close()
          
# Send notifications to IFTTT
def loop(ax, ay, az):
    server = "https://maker.ifttt.com/trigger/Motion_Detected/with/key/GtY7tG4hI-5u9m9k6Gm1H" # Webhooks server
    res = requests.post(url= "https://maker.ifttt.com/trigger/Motion_Detected/with/key/GtY7tG4hI-5u9m9k6Gm1H", json= {"value1" : str(ax), "value2" : str(ay), "value3" : str(az)})
    # print(res.json())
    res.close()
    
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


# Connect Led to GPIO outputs
grnLed = Pin(32, Pin.OUT)
redLed = Pin(15, Pin.OUT)
grnLed(0)
redLed(0)

# Initialize accelerometer
# Initialize access to I2C bus
i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000) 
i2c.scan() # [72,83] # scan for any devices connected to it and return their address.
acc_addr = 83 # I2C device addr of accelerometer: 83
    
# Check I2C Device address
if len(i2c.scan()) == 0:
    print("Error! No device detected!")
elif (83 not in i2c.scan()):
    print("Error! Incorrect device address!")
else:
    print("Correct device address!")
    
# Initialize Accelerometer
i2c.writeto_mem(acc_addr, 0x31, b'\x00') # Set to 10-bit full-resolution mode and Set range to ±2g
i2c.writeto_mem(acc_addr, 0x2C, b'\x0C') # Set output data rate (ODR) to 400 Hz
i2c.writeto_mem(acc_addr, 0x2D, b'\x08') # Turn on measure mode
    
# Calibrate Accelerometer (!! no need offset since (running 15 times) the avg of x and y is really close to 0 and the average of z is really close to 1)
i2c.writeto_mem(acc_addr, 0x1E, b'\x00') # x offset
i2c.writeto_mem(acc_addr, 0x1F, b'\x00') # y offset
i2c.writeto_mem(acc_addr, 0x20, b'\x00') # z offset
print("Accelerometer Calibrated!")

# Timers for checking activation and detecting motions
Timer0 = Timer(0)
Timer0.init(period=30000, mode=Timer.PERIODIC, callback=activation_detection) #t:print(rtc.datetime()))

Timer1 = Timer(1)
Timer1.init(period=3000, mode=Timer.PERIODIC, callback=detect_motion) #t:print(rtc.datetime()))


