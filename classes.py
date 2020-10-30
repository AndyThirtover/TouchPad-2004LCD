# Classes for the TouchPad
import uasyncio
import time
from machine import Timer
from math import ceil

RED = (128,0,0)
GREEN = (0,32,0)
BLUE = (0,0,32)
segment_wait = const(30)
trigger_margin = const(40)
lcd_timeout = const(40)
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

global_counter = 0

t0 = Timer(0)
t0.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:t_increment(1))


class TouchUI():
	def __init__ (self, touch_pad, line_number, no_touch, np, start_pixel, lcd, action):
		self.touch_pad = touch_pad
		self.line_number = line_number
		self.no_touch = no_touch
		self.trigger = no_touch - trigger_margin
		self.np = np
		self.start_pixel = start_pixel
		self.lcd = lcd
		self.action = action
		self.circuit_state = None
		self.state = False
		self.av_array = [1000,1000,1000,1000,1000]  # for a crude running average
		print("TouchUI {}, Calibrate: {}  Trigger: {} Start: {}".format(self.line_number, self.no_touch, self.trigger, self.start_pixel))

	def trace(self,ind):
		print("Trace from: {}".format(ind))

	def do_np(self, show_state):
		print("Display: {}".format(True))
		for i in range(12):
			if show_state:
				self.np[self.start_pixel+i] = RED
			else:
				self.np[self.start_pixel+i] = GREEN
			self.np.write()
			await uasyncio.sleep_ms(segment_wait)

	def show_circuit(self):
		return self.circuit_state

	def toggle_circuit(self):
		if self.circuit_state == None:
			self.circuit_state = False
		else:
			self.circuit_state = not(self.circuit_state)

	async def run(self):
		global global_counter
		# Initial State
		for i in range(12):
			self.np[self.start_pixel+i] = GREEN
		self.np.write()

		while True:
			self.av_array.pop(0)
			self.av_array.append(self.touch_pad.read())
			current = 0
			for v in self.av_array:
				current += v
			current = int(current/5)
			#self.lcd.puts(current,4,self.line_number)  # hardware debug only
			if current < self.trigger:
				if self.state == False:
					self.state = True
					self.lcd.backlight(True)
					global_counter = 0
					for i in range(12):
						self.np[self.start_pixel+i] = RED
						self.np.write()
						await uasyncio.sleep_ms(segment_wait)
					self.lcd.puts("Last Event: {} {:02}:{:02}".format(self.line_number, time.localtime()[3], time.localtime()[4]),0,3)
					self.toggle_circuit()
					show_circuit(self,self.line_number,self.lcd)
					self.action("Called from: {} at {}".format(self.line_number, current))
			else:
				if self.state == True:
					self.state = False
					for i in range(12):
						self.np[self.start_pixel+i] = GREEN
						self.np.write()
						await uasyncio.sleep_ms(segment_wait)
			await uasyncio.sleep_ms(10)



async def show_time(lcd,np):
	global global_counter
	while True:
		t = time.localtime()
		timestr = "{} {} {:02}:{:02}".format(t[2],months[t[1]-1],t[3],t[4])
		lcd.puts(timestr,4,1)
		if global_counter > lcd_timeout:
			lcd.backlight(False)
			dim_leds(np)
		await uasyncio.sleep_ms(30000)

def show_circuit(tu,line_number,lcd):
	if tu.show_circuit() == False:
		msg = "Off"
	else:
		msg = "On "
	lcd.puts(msg,line_number*5,2)


def t_increment(val):
	global global_counter
	global_counter += val

def show_global_counter():
	global global_counter
	return global_counter

def dim_leds(np):
	divsor = 1.2
	for p in range(np.n):  # .n for standard, ._n for SPI version -- actually Nicko van Someren fixed this 29.10.2020 
		cp = np[p]
		newc = (ceil(cp[0]/divsor),ceil(cp[1]/divsor),ceil(cp[2]/divsor))
		np[p] = newc
	np.write()