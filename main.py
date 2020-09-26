from machine import TouchPad, I2C, Pin
from neopixel import NeoPixel
from lcd2004 import LCD2004
import uasyncio
from micropython import const
from classes import TouchUI, show_time, show_global_counter
import utime
from urandom import randint


neo_pin = 23
touch_pins = [14,27,33,32]
calibrate = [0,0,0,0]
LEDS = const(48)
rings=[0,12,24,36]
BLUE = (0,0,32)


np = NeoPixel(Pin(neo_pin),LEDS)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = LCD2004(i2c, addr=39)

# take many readings to get an average of no touch readings
def do_calibrate(t_channel,np):
	cycles = 48
	cul = 0
	for i in range(cycles):
		cul += t_channel.read()
		if i < LEDS:
			np[i] = (randint(0,255),randint(0,255),randint(0,255))
			np.write()
			utime.sleep_ms(10)
	utime.sleep_ms(800)  # just so we can see all the LEDs lit up
	return int(cul/cycles)


def title():
	utime.sleep_ms(2000)
	lcd.clear()
	lcd.puts(" Thirtover Basement",0,0)


def do_print(message):
	print(message)



event_loop = uasyncio.get_event_loop()

for i in range(4):
	tp = TouchPad(Pin(touch_pins[i]))
	notouch = do_calibrate(tp,np)
	lcd.puts("Pad Calibration {}".format(notouch),0,i)
	tu = TouchUI(tp, i, notouch, np, rings[i], lcd, do_print)
	uasyncio.create_task(tu.run())

title()
uasyncio.create_task(show_time(lcd,np))


event_loop.run_forever()





