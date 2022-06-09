from machine import RTC, Timer, ADC, PWM, Pin
from time import sleep


switch = Pin(14, Pin.IN)

# Questions for users to input before program starts
year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))

# Real time clock
rtc = RTC()
rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))

# Timer Interrupt/Callback
def DisplayTime(timer):
        print("Date: " + str(rtc.datetime()[1]) + "/" + str(rtc.datetime()[2]) + "/" + str(rtc.datetime()[0]))
        print("Time: " + str(rtc.datetime()[4]) + ":" + str(rtc.datetime()[5]) + ":" + str(rtc.datetime()[6]))

tim0 = Timer(0)
tim0.init(period=30000, mode=Timer.PERIODIC, callback=DisplayTime) #t:print(rtc.datetime()))

tim1 = Timer(1)
tim1.init(period=100, mode=Timer.PERIODIC, callback=lambda t:print(adc.read())) 

# ADC (pot reading)
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)

# PWM
pwmR = PWM(Pin(15), freq=10, duty=256)

press_count = 0
#current_freq = pwmR.freq()
#current_duty = pwmR.duty()

while True:
    #sleep(0.2)
    if switch.value() == 1:
        press_count += 1
        print(press_count)
        
    # Odd: Change frequency only, NOT duty cycle
    if press_count > 0 and (press_count %2) == 1:
        pwmR.freq(int(adc.read()/150))
        #current_freq = pwmR.freq()
        #stay_duty = pwmR.duty(current_duty)
        sleep(0.5)
        
    # Even: Change duty cycle only, NOT frequency
    elif press_count > 0 and (press_count %2) == 0:
        pwmR.duty(int(adc.read()/10))
        #current_duty = pwmR.duty()
        #stay_freq = pwmR.freq(current_freq)
        sleep(0.5)
        
       
        






