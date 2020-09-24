from machine import TouchPad, I2C, Pin
from neopixel import NeoPixel
from lcd2004 import LCD2004
import uasyncio
from micropython import const

neo_pin = 23
touch_pins = [14,27,32,33]
tp = [None,None,None,None]
calibrate = [1000,1000,1000,1000] # init value - will be lower
margin = const(-30) # margin between no touch and touch
LEDS = const(48)
segment_wait = const(30)
last_state = [None,None,None,None]
rings=[{0,11},{12,23},{24,35},{36,47}]
RED = (128,0,0)
GREEN = (0,32,0)
BLUE = (0,0,32)


np = NeoPixel(Pin(neo_pin),LEDS)
for i in range(4):
	tp[i] = TouchPad(Pin(touch_pins[i]))

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = LCD2004(i2c, addr=39)

# take many readings to get an average of no touch readings
def do_calibrate(t_channel,np):
	cycles = 48
	cul = 0
	for i in range(cycles):
		cul += t_channel.read()
		if i < LEDS:
			np[i] = BLUE
			np.write()
			uasyncio.sleep_ms(segment_wait)
	uasyncio.sleep_ms(800)  # just so wee can see all the LEDs lit up
	return int(cul/cycles)



async def coro_display(np,ring,state,last_state):
	if state != last_state:
		print ("State Change:{}".format(state))
		for i in range(12):
			if state:
				np[ring+i] = RED
			else:
				np[ring+i] = GREEN
			np.write()
			await uasyncio.sleep_ms(segment_wait)
	return state


async def update_display(lcd,s,x,y):
	lcd.puts(s,x,y)

for i in range(4):
	calibrate[i] = margin + do_calibrate(tp[i],np)
	print (calibrate[i])
	uasyncio.run(update_display(lcd,calibrate[i],0,i))

while True:
	for i in range(4):
		level = tp[i].read()

		if level > calibrate[i]:
			uasyncio.run(coro_display(np,i*12,False,last_state[i]))
			last_state[i] = False
		if level < calibrate[i]:
			uasyncio.run(coro_display(np,i*12,True,last_state[i]))
			last_state[i] = True
		uasyncio.run(update_display(lcd,level,4,i))
