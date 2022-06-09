from machine import Pin
from time import sleep

# Onboard RED LED is connected to IO_X
# Find out X from schematics and datasheet
led_board = Pin(13, Pin.OUT)

# Toggle LED 5 times
for i in range(10):
    # Change pin value from its current value, value can be 1/0
    led_board.value(not led_board.value())
    sleep(0.5)
    
print("Led blinked 5 times")
