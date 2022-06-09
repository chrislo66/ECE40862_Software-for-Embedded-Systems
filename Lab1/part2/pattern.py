from machine import Pin
from time import sleep

# Two push bottom switches (GPIO inputs)
switch1 = Pin(14, Pin.IN)
switch2 = Pin(32, Pin.IN)

# Two external LEDs (red, green)
led_red = Pin(15, Pin.OUT)
led_grn = Pin(33, Pin.OUT)

count_red = 0
count_grn = 0

while(True):
    sleep(0.3)
    if switch1.value() == 0 and switch2.value() == 0:
        led_red.value(0)
        led_grn.value(0)
    elif switch1.value() == 0 and switch2.value() == 1:
        count_grn += 1
        led_red.value(0)
        led_grn.value(1)        
    elif switch1.value() == 1 and switch2.value() == 0:
        count_red += 1
        led_red.value(1)
        led_grn.value(0)
    elif switch1.value() == 1 and switch2.value() == 1:
        count_red += 1
        count_grn += 1  
        led_red.value(0)
        led_grn.value(0)


    if count_red >= 10 or count_grn >= 10:
        while(True):
            led_red.value(not led_red.value())
            led_grn.value(not led_grn.value())
            sleep(0.5)
            if (count_red >= 10 and switch2.value() == 1) or (count_grn >= 10 and switch1.value() == 1):
                led_red.value(0)
                led_grn.value(0)
                print('You have successfully implemented LAB1 DEMO!!!')
                break
        break
               

    
