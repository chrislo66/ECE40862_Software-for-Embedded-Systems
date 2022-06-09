import machine, network, ntptime, esp32, socket
from machine import Pin, RTC, Timer

# Global variables
# temp  # measure temperature sensor data
# hall  # measure hall sensor data
# red_led_state # string, check state of red led, ON or OFF
# green_led_state # string, check state of green led, ON or OFF
# switch_state # string, check state of switch, ON or OFF

switch = Pin(14, Pin.IN)
grnLed = Pin(32, Pin.OUT)
redLed = Pin(15, Pin.OUT)

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state, green_led_state
    """
    #temp = esp32.raw_temperature()
    #hall = esp32.hall_sensor()
    
    if grnLed.value() == 1:
        green_led_state = "ON"
    else:
        green_led_state = "OFF"
    
    if redLed.value() == 1:
        red_led_state = "ON"
    else:
        red_led_state = "OFF"
        
    if switch.value() == 1:
        switch_state = "ON"
    else:
        switch_state = "OFF"
    
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    <p>
    SWITCH Current State: <strong>""" + switch_state + """</strong>
    </p>
    </body>
    </html>"""
    return html_webpage

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

# Socket 
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr) 
s.listen(4)  
print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    
    # The recv() method receives the data from the client socket
    # The argument of the recv() method specifies the maximum data that can be received at once.
    request = str(cl.recv(1024))
    #print('Content = %s' % str(request))
    
    # Led logic
    grnLed_on = request.find('/?green_led=on')
    grnLed_off = request.find('/?green_led=off')
    redLed_on = request.find('/?red_led=on')
    redLed_off = request.find('/?red_led=off')

    if grnLed_on == 6:
        grnLed.value(1)        
    if grnLed_off == 6:
        grnLed.value(0)
    if redLed_on == 6:
        redLed.value(1)
    if redLed_off == 6:
        redLed.value(0)
        
    # Measure temp and hall
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    
    response = web_page()
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send('Connection: close\n\n')
    cl.send(response)
    cl.close()